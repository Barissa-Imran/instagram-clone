from django.urls import path
from gram import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
