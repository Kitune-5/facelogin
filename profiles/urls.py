from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('classify/', views.find_user_view, name='classify'),
    path('profile/', views.user_profile, name='profile'),
    path('students/', views.students, name='students'),
    
]
