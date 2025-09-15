from django.urls import path
from . import views

urlpatterns = [
    path('', views.evento_cultural_list, name='evento_cultural_list'),
]