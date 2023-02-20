from django.urls import path, include


urlpatterns = [
    path('train/', include('train.urls')),
    path('recognize/', include('testModel.urls')),
    path('logs/', include('searchLog.urls'))
]