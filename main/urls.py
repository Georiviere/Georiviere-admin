from django.urls import path
from .views import JSSettings

app_name = 'main'
urlpatterns = [
    path('api/settings.json', JSSettings.as_view(), name='settings_json'),
]
