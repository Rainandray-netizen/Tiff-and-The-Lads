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
from .models import Activity, Routine
from .forms import ActivityForm

# Create your views here.
def home(request):
    if request.method == 'POST':
        # gets a list of the selected activities from the dropdown 
        selected_activities = request.POST.getlist('activity')
        # if there is only one selected activity then select that activity by selecting it by index 0 (since there is only one activity in the list)
        if len(selected_activities) == 1:
            single_activity = selected_activities[0]
            # filters through the activities seed file and and finds the matching object to the current selected activity and sets it to activity (use this to access the risk and factor)
            activity = list(filter(lambda a: a['activity'] == single_activity, activities))
            return render(request, 'home.html', {
                'single_activity': single_activity,
                'activity': activity,
                'selected_activities': selected_activities,
                'activities': activities,
                'global_stats': global_stats,
                'country_stats': country_stats_list,
                'current_date': datetime.date(datetime.now()),
                })
        # if there are multiple selections then loop through the list
        elif len(selected_activities) > 1:
            for sa in selected_activities:
                # for each activity that is in the list find the corresponding object in the activities seed file
                # activity is now set to the object from the seed file
                activity = list(filter(lambda a: a['activity'] == sa, activities))
            return render(request, 'home.html', {
                'activity': activity,
                'selected_activities': selected_activities,
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
  activity_form = ActivityForm()
  # routine = Routine.objects.filter(user = request.user)
  return render(request, 'registration/profile.html', {'activity_form': activity_form})

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
