from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path('selected/<slug:pk>/', views.click, name="click"),
    path('practice/', views.learn_bootstrap, name="css"),

]