from django.forms import ModelForm
from .models import Activity

class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    fields = ['name', 'number_of_people', 'distancing','venue', 'time_length', 'interaction']