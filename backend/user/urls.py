from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.retrieve_user_view),
    path('user/change-password/', views.change_password_view)
]