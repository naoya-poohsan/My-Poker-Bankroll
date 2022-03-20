from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Result
from .forms import ResultForm

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


def Plot_Graph(x,y):
	fig, ax = plt.subplots()
	ax.plot(x, y, marker='o', linestyle='solid')
	ax.set_title('Bankroll')
	ax.set_xlabel('')
	ax.set_ylabel('result')
	ax.grid(axis='x', alpha=0.5)
	ax.grid(which='both', axis='y', alpha=0.5)
	ax.axhline(y=0, color='red', linewidth=0.5)
#	ax.set_facecolor('#444444')
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
	sorted_queryset = sorted(queryset, key=lambda queryset: queryset.date)
	reversed_queryset = sorted(queryset, key=lambda queryset:queryset.date, reverse=True)

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
	
	graph = Plot_Graph(dates, bankroll)

	context = {
		'object_list': reversed_queryset,
		'graph': graph,
	}
	return render(request, 'bankroll_graph.html', context)



def sample_home_view(request):
	lst = []
	bankroll = [0]
	date = []
	queryset = Result.objects.all()
	sorted_queryset = sorted(queryset, key=lambda queryset: queryset.date)
	reversed_queryset = sorted(queryset, key=lambda queryset:queryset.date, reverse=True)

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
	
	graph = Plot_Graph(dates, bankroll)

	context = {
		'object_list': reversed_queryset,
		'graph': graph,
	}
	return render(request, 'sample_bankroll_graph.html', context)

