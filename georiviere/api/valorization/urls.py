from django.conf import settings
from django.urls import path, include
from rest_framework import routers

from georiviere.api.valorization.views import GeoriviereVersionAPIView
from georiviere.api.valorization.views.river import StreamViewSet
from georiviere.api.valorization.views.swagger import schema_view
from georiviere.api.valorization.views.valorization import POIViewSet
from georiviere.api.valorization.views.zoning import CityViewSet, DistrictViewSet


router = routers.DefaultRouter()
router.register('poi', POIViewSet, basename='poi')
router.register('city', CityViewSet, basename='city')
router.register('district', DistrictViewSet, basename='district')
router.register('stream', StreamViewSet, basename='stream')

app_name = 'api_valorization'

_urlpatterns = [
    path('version', GeoriviereVersionAPIView.as_view()),
    path('', include(router.urls)),
]
if 'drf_yasg' in settings.INSTALLED_APPS:
    _urlpatterns.append(path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
urlpatterns = [path('api/valorization/', include(_urlpatterns))]
