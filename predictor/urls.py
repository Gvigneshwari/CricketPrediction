from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),             # Home page
    path('prediction/', views.prediction, name='prediction'),  # Prediction page
]