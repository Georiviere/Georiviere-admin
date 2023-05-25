from django.conf import settings
from django.urls import path, include
from rest_framework import routers

from georiviere.portal.views import GeoriviereVersionAPIView
from georiviere.portal.views.flatpage import FlatPageViewSet
from georiviere.portal.views.portal import PortalViewSet
from georiviere.portal.views.river import StreamViewSet
from georiviere.portal.views.sensitivity import SensitivityViewSet
from georiviere.portal.views.swagger import schema_view
from georiviere.portal.views.valorization import POIViewSet
from georiviere.portal.views.zoning import CityViewSet, DistrictViewSet, WatershedViewSet


router = routers.DefaultRouter()
router.register(r'(?P<portal_pk>\d+)/pois', POIViewSet, basename='pois')

router.register(r'(?P<portal_pk>\d+)/streams', StreamViewSet, basename='streams')

router.register(r'(?P<portal_pk>\d+)/flatpages', FlatPageViewSet, basename='flatpages')

router.register('portal', PortalViewSet, basename='portal')
router.register('cities', CityViewSet, basename='cities')
router.register('districts', DistrictViewSet, basename='districts')
router.register('watersheds', WatershedViewSet, basename='watersheds')
router.register('sensitivities', SensitivityViewSet, basename='sensitivities')

app_name = 'api_portal'

_urlpatterns = [
    path('version', GeoriviereVersionAPIView.as_view(), name='version'),
    path('', include(router.urls)),
]
if 'drf_yasg' in settings.INSTALLED_APPS:
    _urlpatterns.append(path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
urlpatterns = [path('api/portal/<lang:lang>/', include(_urlpatterns))]
