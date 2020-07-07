from django.forms import ModelForm
from .models import Activity

class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    fields = ['name', 'number_of_people', 'venue', 'time_length', 'interaction']