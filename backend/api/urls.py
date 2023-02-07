from django.urls import path, include


urlpatterns = [
    path('train/', include('train.urls'))
]