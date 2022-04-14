from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('' , views.home, name="home"),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
]
