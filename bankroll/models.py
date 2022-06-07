from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


# Create your models here.
class Result(models.Model):

	user        = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

	game 		= models.CharField(default='', max_length=10)
	by_in 		= models.DecimalField(default=1, decimal_places=2, max_digits=10)
	result      = models.DecimalField(default=1, decimal_places=2, max_digits=10)
	date        = models.DateField()
	rate        = models.CharField(default='', max_length=100)
	kind 		= models.CharField(default='', max_length=100)
	max_players = models.CharField(default='', max_length=10)
	memo 		= models.CharField(max_length=1000)


	def get_absolute_url(self):
		return reverse('data-detail', kwargs={'pk': self.id})


	def win(self):
		win = self.result - self.by_in
		text = ''
		if win >= 0:
			text = 'Win {:+}'.format(win)
		else :
			text = 'Lose {:+}'.format(win)
		return text


class Filter(models.Model):
    start_date = models.DateField()
    end_date   = models.DateField()
    rate       = models.CharField(default='', max_length=100)


