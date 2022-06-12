from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Result, Filter
from .forms import ResultForm, FilterForm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import base64
import io
from io import BytesIO

from django.views.generic import (
								CreateView,
								UpdateView,
								DetailView,
								DeleteView,
								ListView,
								View
								)


#class DataListView(ListView):
#	template_name = 'bankroll_list.html'
#	queryset = Result.objects.all()
#	queryset = sorted(queryset, key=lambda queryset: queryset.date)



class DataInputView(LoginRequiredMixin, CreateView):
	template_name = 'bankroll_input.html'
	form_class = ResultForm
	success_url = reverse_lazy('data-list')

	def form_valid(self, form):
		bankroll = form.save(commit=False)
		bankroll.user = self.request.user
		bankroll.save()
		return super().form_valid(form)



class DataDetailView(LoginRequiredMixin, DetailView):
	template_name = 'bankroll_detail.html'
	model = Result

	def get_queryset(self):
		queryset = Result.objects.filter(user=self.request.user)
		return queryset


#def DetailView(request):
#	queryset = Result.objects.all()
#	game = queryset.get_game_display()



class DataDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'bankroll_confirm_delete.html'
	model = Result
	success_url = reverse_lazy('data-list')



class DataUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'bankroll_update.html'
	form_class = ResultForm
	success_url = reverse_lazy('data-list')

	def get_queryset(self):
		queryset = Result.objects.filter(user=self.request.user)
		return queryset



def Output_Graph():
	buffer = BytesIO()                   #バイナリI/O(画像や音声データを取り扱う際に利用)
	plt.savefig(buffer, format="png")    #png形式の画像データを取り扱う
	buffer.seek(0)                       #ストリーム先頭のoffset byteに変更
	img   = buffer.getvalue()            #バッファの全内容を含むbytes
	graph = base64.b64encode(img)        #画像ファイルをbase64でエンコード
	graph = graph.decode("utf-8")        #デコードして文字列から画像に変換
	buffer.close()
	return graph


def Plot_Graph(x,y, title):
	fig, ax = plt.subplots()
	ax.plot(x, y, marker='o', markersize=3,  linestyle='solid')
	title = 'win  {:+}  $'.format(title)
	ax.set_title(title, size=24, color='red')
	ax.set_xlabel('')
	ax.set_ylabel('Result')
	ax.grid(which='major', axis='y', alpha=0.5)
	ax.axhline(y=0, color='red', linewidth=0.5)
	# 補助目盛を付ける
	ax.minorticks_on()
	# xの補助目盛は消す
	ax.xaxis.set_tick_params(which='minor', bottom=False)
	# 自動のx軸目盛り
	ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(10))
	fig.tight_layout()
	labels = ax.get_xticklabels()
	fig.subplots_adjust(bottom=0.15)
	plt.setp(labels, rotation=50, fontsize=10)

	graph = Output_Graph()
	return graph


@login_required
def home_view(request):
	lst = []
	bankroll = [0]
	date = []
	queryset = Result.objects.filter(user=request.user)
	queryset_count = Result.objects.filter(user=request.user).count()
	sorted_queryset = sorted(queryset, key=lambda queryset: queryset.date)

	# filterは一度に書く、複数回filterをしても最後のfilterしか反映されない
	# filtered_queryset = Result.objects.filter(rate=1)

	reversed_queryset = sorted(queryset, key=lambda queryset: queryset.date, reverse=True)


	# sorted_querysetからby_in, result, dateを取得
	for query in sorted_queryset:
		by_in = query.by_in
		result = query.result
		lst.append(result - by_in)
		date.append(query.date)

	# brankrollにグラフに出力する収支を代入する
	for n in range(1, len(lst)+1):
		bankroll.append(bankroll[-1] + lst[n-1])
	# bankrollに最初から入っている０を消す(前のデータとの差を使うので必要だった)
	del bankroll[0]

	dates = [d.strftime('%m-%d') for d in date]
	# 日付が被った時に(1),(2)と区別するための加工
	dates = [x + "(" + str(dates[0:i].count(x) + 1) + ")" if dates[0:i].count(x) > 0 else x for i, x in enumerate(dates)]

	if not bankroll:
		graph = Plot_Graph(dates, bankroll, 0)
	else:
		graph = Plot_Graph(dates, bankroll, bankroll[-1])


	context = {
		'object_list': reversed_queryset,
		'graph': graph,
		'queryset_count': queryset_count,
	}
	return render(request, 'bankroll_graph.html', context)


# home_viewとほぼ変わらず（ログインユーザーのデータかどうか）
def sample_home_view(request):
	lst = []
	bankroll = [0]
	date = []
	queryset = Result.objects.all()
	queryset_count = Result.objects.all().count()
	sorted_queryset = sorted(queryset, key=lambda queryset: queryset.date)
	reversed_queryset = sorted(queryset, key=lambda queryset: queryset.date, reverse=True)

	for query in sorted_queryset:
		by_in = query.by_in
		result = query.result
		lst.append(result - by_in)
		date.append(query.date)

	for n in range(1, len(lst)+1):
		bankroll.append(bankroll[-1] + lst[n-1])

	del bankroll[0]

	dates = [d.strftime('%m-%d') for d in date]
	dates = [x + "(" + str(dates[0:i].count(x) + 1) + ")" if dates[0:i].count(x) > 0 else x for i, x in enumerate(dates)]

	graph = Plot_Graph(dates, bankroll, bankroll[-1])

	context = {
		'object_list': reversed_queryset,
		'graph': graph,
		'queryset_count': queryset_count,
	}
	return render(request, 'sample_bankroll_graph.html', context)



def filter_view(request):

	if request.method == 'GET':
		form = FilterForm(data=request.GET or None)

	context = {
		'form': form
	}

	return render(request, 'filter.html', context)



start_date_year = 0
start_date_month = 0
start_date_day = 0
end_date_year = 0
end_date_month = 0
end_date_day = 0
rate = 0


@login_required
def filtered_home_view(request):
	global start_date_year
	global start_date_month
	global start_date_day
	global end_date_year
	global end_date_month
	global end_date_day
	global rate

	if 'start_date_year' in request.GET:
		start_date_year = request.GET['start_date_year']

	if 'start_date_month' in request.GET:
		start_date_month = request.GET['start_date_month']

	if 'start_date_day' in request.GET:
		start_date_day = request.GET['start_date_day']

	if 'end_date_year' in request.GET:
		end_date_year = request.GET['end_date_year']

	if 'end_date_month' in request.GET:
		end_date_month = request.GET['end_date_month']

	if 'end_date_day' in request.GET:
		end_date_day = request.GET['end_date_day']

	if 'rate' in request.GET:
		rate = request.GET['rate']

	start_date = ('{}-{}-{}'.format(start_date_year, start_date_month, start_date_day))
	end_date = ('{}-{}-{}'.format(end_date_year, end_date_month, end_date_day))


	lst = []
	bankroll = [0]
	date = []

	queryset = Result.objects.filter(user=request.user, rate=rate, date__range=[start_date, end_date])
	queryset_count = Result.objects.filter(user=request.user, rate=rate, date__range=[start_date, end_date]).count()

	sorted_queryset = sorted(queryset, key=lambda queryset: queryset.date)
	reversed_queryset = sorted(queryset, key=lambda queryset: queryset.date, reverse=True)

	for query in sorted_queryset:
		by_in = query.by_in
		result = query.result
		lst.append(result - by_in)
		date.append(query.date)

	# brankrollにグラフに出力する収支を代入する
	for n in range(1, len(lst)+1):
		bankroll.append(bankroll[-1] + lst[n-1])
	# bankrollに最初から入っている０を消す(前のデータとの差を使うので必要だった)
	del bankroll[0]

	dates = [d.strftime('%m-%d') for d in date]
	# 日付が被った時に(1),(2)と区別するための加工
	dates = [x + "(" + str(dates[0:i].count(x) + 1) + ")" if dates[0:i].count(x) > 0 else x for i, x in enumerate(dates)]

	if not bankroll:
		graph = Plot_Graph(dates, bankroll, 0)
	else:
		graph = Plot_Graph(dates, bankroll, bankroll[-1])


	context = {
		'object_list': reversed_queryset,
		'graph': graph,
		'queryset_count': queryset_count
	}

	return render(request, 'filtered_data.html', context)




