from django.forms import ModelForm
from wiki.models import Exercise

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
