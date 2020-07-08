from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .covidapi import country_stats_list, global_stats
from .seed import activities
from datetime import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Activity, Routine, Profile
from django.contrib.auth.models import User
from .forms import ActivityForm

# Create your views here.
def home(request):
    if request.method == 'POST':
        selected_activity = request.POST.get('activity')
        activity = list(filter(lambda a: a['activity'] == selected_activity, activities))
        return render(request, 'home.html', {
            'selected_activity': selected_activity,
            'activity': activity,
            'activities': activities,
            'global_stats': global_stats,
            'country_stats': country_stats_list,
            'current_date': datetime.date(datetime.now()),
            })
    else:
        return render(request, 'home.html', {
        'activities': activities,
        'global_stats': global_stats,
        'country_stats': country_stats_list,
        'current_date': datetime.date(datetime.now()),
})





def dashboard(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    location = profile.location.lower()
    user_country = next(country for country in country_stats_list if country['Name'].lower() == location)
    if request.method == 'POST':
        selected_activities = request.POST.getlist('activity')
        for sa in selected_activities:
            activity = list(filter(lambda a: a['activity'] == sa, activities))
        return render(request, 'dashboard.html', {
            'selected_activities': selected_activities,
            'location': location,
            'user_country': user_country,
            'activities': activities,
            'activity': activity,
            'country_stats': country_stats_list,
            'current_date': datetime.date(datetime.now())
    })
    else:
        return render(request, 'dashboard.html', {
        'location': location,
        'user_country': user_country,
        'activities': activities,
        'country_stats': country_stats_list,
        'current_date': datetime.date(datetime.now())
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
  profile = Profile.objects.get(user=request.user)
  # activities = Activities.objects.filter(user = request.user)
  activity_form = ActivityForm()
  # routine = Routine.objects.filter(user = request.user)
  return render(request, 'registration/profile.html', {'activity_form': activity_form, 'profile': profile})

def add_activity(request, profile_id):
  form = ActivityForm(request.POST)
  if form.is_valid():
    new_activity = form.save(commit=False)
    new_activity.profile_id = profile_id
    new_activity.save()
  return redirect('/accounts/profile', profile_id=profile_id)

def activites_detail(request, activity_id):
  activity = Activity.objects.get(id=activity_id)
  return render(request, 'profile/activity-detail.html', {'activity': activity})


class ActivityList(LoginRequiredMixin, ListView):
  model = Activity

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/accounts/profile'

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
