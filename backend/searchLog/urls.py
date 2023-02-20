from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_log_view),
]