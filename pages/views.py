from django.shortcuts import render, get_object_or_404

from bankroll.models import Result
from bankroll.forms import ResultForm

# Create your views here.

def home_view(request):
	queryset = Result.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, 'home.html', context)


def about_view(request, *args, **kwargs):

	return render(request, 'about.html', {})

