from django.urls import path
from . import views

urlpatterns = [
    # sign_up
    path('', views.home, name='home'),
    path('login/', views.sign_in, name='sign_in'),
    path('logout/', views.sign_out, name='sign_out'),
    path('register_user/', views.register, name='sign_up'),
    path('admin_dashboard/', views.staff_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.client_dashboard, name='staff_dashboard'),
    
    
    path('manage_users/', views.all_users, name='manage_users'),
    path('create_event/', views.register_event, name='create_event'),
    path('event_list/', views.event_list, name='event_list'),
    path('current_events/', views.current_events, name='current_events'),
    
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    
    # delete_sitting_form
    path('create_sitting_format/', views.create_sitting_format, name='create_sitting_format'),
    path('sitting_format_list/', views.sitting_format_list, name='sitting_format_list'),
    path('sitting_format/delete/<int:sitting_id>/', views.delete_sitting_form, name='delete_sitting_format'),
    
]