from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.retrieve_user_view)
]