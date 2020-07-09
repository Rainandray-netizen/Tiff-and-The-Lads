from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/profile/', views.profile_show, name='show'),
    # path('activities/', views.activities_base, name='activities_base'),

    path('accounts/<int:profile_id>/add_activity', views.add_activity, name='activity_create'),
    path('accounts/<int:pk>/delete/', views.ActivityDelete.as_view(), name='activity_delete'),
    path('accounts/<int:activity_id>/activities', views.activites_detail, name='detail'),

    path('accounts/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('activity/<int:pk>/update/', views.ActivityUpdate.as_view(), name='activity_update'),
    
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),

    path('routine/create/', views.routine_create, name='routine_create'), ## Needs to be reviewed for drag and drop feature
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('routine/delete/<int:id>', views.routine_delete, name='routine_delete'),
]    
    # path('activities/<int:pk>/update/', views.  , name=)