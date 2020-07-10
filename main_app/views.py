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
            # 'global_stats': global_stats,
            # 'country_stats': country_stats_list,
            'current_date': datetime.date(datetime.now()),
            })
    else:
        return render(request, 'home.html', {
        'activities': activities,
        # 'global_stats': global_stats,
        # 'country_stats': country_stats_list,
        'current_date': datetime.date(datetime.now()),
})

def add_photo(request, profile_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
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
    # user_country = next(country for country in country_stats_list if country['Name'].lower() == location)
    # last_updated = parse(user_country['Updated'])
    p = profile.activity_set.all()
    user_activities = p.values_list('name', flat=True)
    routine = Routine.objects.filter(date=datetime.date(datetime.now()))
    if request.method == 'POST':
        selected_activities = request.POST.getlist('activity')
        for sa in selected_activities:
            activity = list(filter(lambda a: a['activity'] == sa, activities))
        return render(request, 'dashboard.html', {
            'today_routine': routine,
            # 'last_updated': last_updated,
            'user_activities': user_activities,
            'selected_activities': selected_activities,
            'location': location,
            'user_country': user_country,
            'activities': activities,
            'activity': activity,
            # 'country_stats': country_stats_list,
            'current_date': datetime.date(datetime.now())
    })
    else:
        return render(request, 'dashboard.html', {
        'today_routine': routine,
        # 'last_updated': last_updated,
        'user_activities': user_activities,
        'location': location,
        # 'user_country': user_country,
        'activities': activities,
        # 'country_stats': country_stats_list,
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
    risk_score = risk_score / 4
    form = ActivityForm(request.POST)
    if form.is_valid():
      new_activity = form.save(commit=False)
      new_activity.profile_id = profile_id
      new_activity.risk_level= risk_score
      new_activity.save()
  return redirect('/accounts/profile', profile_id=profile_id)
  
def activites_detail(request, activity_id):
  activity = Activity.objects.get(id=activity_id)
  return render(request, '/profile/activity-detail.html', {'activity': activity})

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