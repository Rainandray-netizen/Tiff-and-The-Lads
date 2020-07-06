from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('profile/', views.profile_show, name='show'),
    # path('activities/', views.activities_base, name='activities_base'),

    # path('activities/create/', views.ActivityCreate, name='activity_create'),
    # path('activity/<int:pk>/update/', views.ActivityUpdate.as_view(), name='activity_update'),
    # path('activity/<int:pk>/delete/', views.ActivityDelete.as_view(), name='activity_delete'),
    

    # path('routine/create/', views.RoutineCreate, name='routine_create'), ## Needs to be reviewed for drag and drop feature
    # path('routine/<int:pk>/update/', views.RoutineUpdate.as_view(), name='routine_update'),
    # path('routine/<int:pk>/delete/', views.RoutineDelete.as_view(), name='routine_delete'),
]    
    # path('activities/<int:pk>/update/', views.  , name=)
