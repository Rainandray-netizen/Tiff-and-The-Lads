from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .covidapi import country_stats_list, global_stats
from .seed import activities

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Activity, Routine, Profile


# Create your views here.
def home(request):
  return render(request, 'home.html', {
    'activities': activities,
    'global_stats': global_stats,
    'country_stats': country_stats_list,

})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# @login_required
def profile_show(request):
  # activities = Activities.objects.filter(user = request.user)
  # routine = Routine.objects.filter(user = request.user)
  return render(request, 'registration/profile.html')

class ActivityList(LoginRequiredMixin, ListView):
  model = Activity

class ActivityDetail(LoginRequiredMixin, DetailView):
  model = Activity

class ActivityCreate(LoginRequiredMixin, CreateView):
  model = Activity
  fields = '__all__'

class ActivityUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = '__all__'

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/profile/index/'




class RoutineList(LoginRequiredMixin, ListView):
  model = Activity

class RoutineDetail(LoginRequiredMixin, DetailView):
  model = Activity

class RoutineCreate(LoginRequiredMixin, CreateView):
  model = Activity
  fields = '__all__'

class RoutineUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = '__all__'

class RoutineDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/profile/index/'
