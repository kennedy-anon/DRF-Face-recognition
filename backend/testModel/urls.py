from django.urls import path

from . import views

urlpatterns = [
    path('', views.recognize_image_view),
]