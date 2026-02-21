from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Custom Auth Routes
    path('login/', views.custom_login, name='login'),
    path('signup/', views.custom_signup, name='signup'),
    
    # We can still use Django's built-in logout view
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]