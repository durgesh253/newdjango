from django.shortcuts import render
from django.urls import path
from .views import Registreview,LoginView,LogoutView

urlpatterns = [
    path('register/', Registreview.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', lambda request: render(request, 'home.html'), name='home'),  # Dummy home view

]
