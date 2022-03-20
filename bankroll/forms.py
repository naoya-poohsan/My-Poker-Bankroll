from django import forms
from django.utils import timezone
from .models import Result


class ResultForm(forms.ModelForm):

	game = forms.ChoiceField(choices= (
			(1, "No Limit Hold'em"),
			(2, "Limit Hold'em"),
			(3, "Pot Limit Omaha")
									), initial=1, required=True)

	by_in  = forms.DecimalField(required=True)
	result = forms.DecimalField(required=True)
	date = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(2000, 2101)]), initial=timezone.now(), required=True)

	rate = forms.ChoiceField(choices = (
            (1, '0.01 / 0.02'),
            (2, '0.02 / 0.05'),
            (3, '0.05 / 0.10'),
            (4, '0.08 / 0.16'),
            (5, '0.10 / 0.25'),
            (6, '0.25 / 0.50'),
            (7, '0.50 / 1'),
            (8, '1 / 2')
							        ), required=True)

	kind = forms.ChoiceField(choices = (
            (1, 'cash(zoom)'),
            (2, 'cash(table)'),
            (3, 'tournament'),
            (4, 'spin&go'),
        						), initial=1, required=True)

	max_players = forms.ChoiceField(choices= (
			(1, '6'),
			(2, '9')
								), initial=2, required=True)

	memo = forms.CharField(required=False,
						   widget=forms.Textarea(
						   		attrs={
						   			'rows': 3,
						   			'cols': 30
						   		}
						   		)
						   )

	class Meta:
		model = Result
		fields = ('game', 'by_in', 'result', 'date', 'rate', 'kind', 'max_players', 'memo')


