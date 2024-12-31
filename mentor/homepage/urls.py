from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('login', views.login_page, name="login"),
    path('signup', views.signup_user, name="signup"),
    path('logout', views.logout_user, name="logout"),
    path('create/', views.create_profile, name='create_profile'),
    path('edit-profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('browse/', views.browse_profile, name='browse_profile'),
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'), 
    path('delete/', views.delete_profile, name='delete_profile'),
    path('send-connection-request/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
]
