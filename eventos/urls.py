from django.urls import path
from . import views
from .views import evento_cultural_view

urlpatterns = [
    path('evento_cultural/', evento_cultural_view, name='evento_cultural_list')
]