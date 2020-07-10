from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .covidapi import country_stats_list, global_stats
from .seed import activities
from datetime import datetime
from dateutil.parser import parse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Activity, Routine, Profile, Photo
from django.contrib.auth.models import User
from .forms import ActivityForm
import uuid
import boto3
import requests
from bs4 import BeautifulSoup

URL = 'https://chartwell.com/en/blog/2020/03/8-tips-to-help-prevent-coronavirus-infection-and-illness'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'covidriskapp'


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

def add_photo(request, profile_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"    
            photo = Photo(url=url, profile_id=profile_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('/accounts/profile', profile_id=profile_id)


def save(self, *args, **kwargs):
        try:
            this = Cars.objects.get(id=self.id)
            if this.image_file:
                this.image_file.delete()   
        except ObjectDoesNotExist: 
            pass        
        super(Cars, self).save(*args, **kwargs)
# if the routine has a date equal to todays date then pass them here 
def dashboard(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    location = profile.location.lower()
    # Get country data from API with NA for data that is not available
    user_country_with_NA = next(country for country in country_stats_list if country['Name'].lower() == location)
    # Get the last updated that is available from user_country_with_NA because country_values only returns values so cant query by the key
    last_updated = user_country_with_NA['Updated']
    # Retrives the values for the given country in a list
    country_values = list(user_country_with_NA.values())
    # Goes through the list to find NA and replaces it with 0 (need this because the graph wont work if a value is a string and these values differ for different countries)
    user_country = list(map(lambda na:0 if na=="NA" else na, country_values))
    p = profile.activity_set.all()
    user_activities = p.values_list('name', flat=True)
    routine = Routine.objects.filter(profile=profile, date=datetime.date(datetime.now())).values_list(('activity_name'))
    if request.method == 'POST':
        selected_activities = request.POST.getlist('activity')
        for sa in selected_activities:
            activity = list(filter(lambda a: a['activity'] == sa, activities))
        return render(request, 'dashboard.html', {
            'user_country_with_NA': user_country_with_NA,
            'today_routine': routine,
            'last_updated': last_updated,
            'user_activities': user_activities,
            'global_stats': global_stats,
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
        'user_country_with_NA': user_country_with_NA,
        'today_routine': routine,
        'last_updated': last_updated,
        'user_activities': user_activities,
        'location': location,
        'global_stats': global_stats,
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
      return redirect('profile_create')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def routine_delete(request, id):
    routine = Routine.objects.get(id=id)
    routine.delete()
    return redirect('/accounts/profile')

# @login_required
def profile_show(request):
  profile = Profile.objects.get(user=request.user)
  routine = Routine.objects.filter(profile=profile).values()
  # activities = Activities.objects.filter(user = request.user)
  activity_form = ActivityForm()
  # profile = profile_id
  # routine = Routine.objects.filter(user = request.user)
  p = profile.activity_set.all()
  user_activities = p.values_list('name', flat=True)
  return render(request, 'registration/profile.html', {'activity_form': activity_form, 'profile': profile, 'user_activities': user_activities, 'routine': routine})

def add_activity(request, profile_id):
  if request.method == 'POST':
    number_of_people = request.POST.get('number_of_people')
    distancing = request.POST.get('distancing')
    venue = request.POST.get('venue')
    time_length = request.POST.get('time_length')
    interaction = request.POST.get('interaction')
    risk_score = 0
    if int(number_of_people) <= 5:
      risk_score += 3
    elif int(number_of_people) > 5 and int(number_of_people) <= 10: 
      risk_score += 5
    elif int(number_of_people) > 10 and int(number_of_people) <= 15:
      risk_score += 6
    else:
      risk_score += 8

    if distancing == 'No':
      risk_score += 7
    else: 
      risk_score += 3

    if venue == 'A':
      risk_score += 3
    else:
      risk_score += 7

    if time_length == 'A':
      risk_score += 3
    elif time_length == 'B':
      risk_score += 5
    else:
      risk_score += 8

    if interaction == 'A':
      risk_score += 3
    elif interaction == 'B':
      risk_score += 5
    else:
      risk_score += 8
    risk_score = risk_score / 3.5
    print(risk_score)
    print(distancing)
    form = ActivityForm(request.POST)
    if form.is_valid():
      new_activity = form.save(commit=False)
      new_activity.profile_id = profile_id
      new_activity.risk_level= risk_score
      new_activity.save()
  return redirect('/accounts/profile', profile_id=profile_id)
  
def activites_detail(request, activity_id):
  activity = Activity.objects.get(id=activity_id)
  results = soup.find("div",{"class":'articleBody'})
  r = results.text
  print(r)
  return render(request, 'profile/activity-detail.html', {'activity': activity, 'r':r})

# @login_required
def routine_create(request):
    print(request.user.id)
    profile = Profile.objects.get(user=request.user.id)
    activity = Activity.objects.get(name=request.POST.get('activity'))
  
    if request.method == 'POST':
        date = request.POST.get('date')
        new_routine = Routine.objects.create(date=date, profile=profile, activity_name=activity)
        print(new_routine)
    return redirect('/accounts/profile', { 'profile': profile})

class RoutineDelete(LoginRequiredMixin, DeleteView):
  model = Routine
  success_url = '/accounts/profile'

class ActivityList(LoginRequiredMixin, ListView):
  model = Activity

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  success_url = '/accounts/profile'

class RoutineList(LoginRequiredMixin, ListView):
  model = Activity

class RoutineDetail(LoginRequiredMixin, DetailView):
  model = Activity

class RoutineUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = '__all__'

class ProfileCreate(LoginRequiredMixin, CreateView):
  model = Profile
  fields = ['name', 'location']
  success_url = '/accounts/profile/'

  def form_valid(self, form):
    # Assign the logged in user
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class ProfileUpdate(UpdateView):
  model = Profile
  fields = ['name', 'location']
  success_url = '/accounts/profile/'