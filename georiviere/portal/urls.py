from django.conf import settings
from django.urls import path, include
from rest_framework import routers

from georiviere.portal.views import GeoriviereVersionAPIView
from georiviere.portal.views.flatpage import FlatPageViewSet
from georiviere.portal.views.contribution import (
    ContributionViewSet,
    CustomContributionTypeViewSet,
)
from georiviere.portal.views.portal import PortalViewSet
from georiviere.portal.views.river import StreamViewSet
from georiviere.portal.views.sensitivity import SensitivityViewSet
from georiviere.portal.views.valorization import POIViewSet
from georiviere.portal.views.zoning import (
    CityViewSet,
    DistrictViewSet,
    WatershedViewSet,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = routers.DefaultRouter()
# Datas are available depending on portal or not.
router.register(
    r"(?P<lang>[a-z]{2})/(?P<portal_pk>\d+)/pois", POIViewSet, basename="pois"
)

router.register(
    r"(?P<lang>[a-z]{2})/(?P<portal_pk>\d+)/streams", StreamViewSet, basename="streams"
)

router.register(
    r"(?P<lang>[a-z]{2})/(?P<portal_pk>\d+)/flatpages",
    FlatPageViewSet,
    basename="flatpages",
)
router.register(
    r"(?P<lang>[a-z]{2})/(?P<portal_pk>\d+)/contributions",
    ContributionViewSet,
    basename="contributions",
)
router.register(
    r"(?P<lang>[a-z]{2})/(?P<portal_pk>\d+)/custom-contribution-types",
    CustomContributionTypeViewSet,
    basename="custom_contribution_types",
)
router.register(
    r"(?P<lang>[a-z]{2})/(?P<portal_pk>\d+)/watersheds",
    WatershedViewSet,
    basename="watersheds",
)

router.register(r"(?P<lang>[a-z]{2})/portal", PortalViewSet, basename="portal")
router.register(r"(?P<lang>[a-z]{2})/cities", CityViewSet, basename="cities")
router.register(r"(?P<lang>[a-z]{2})/districts", DistrictViewSet, basename="districts")
router.register(
    r"(?P<lang>[a-z]{2})/sensitivities", SensitivityViewSet, basename="sensitivities"
)

app_name = "api_portal"

_urlpatterns = []
if settings.API_SCHEMA:  # pragma: no cover
    _urlpatterns += [path("schema/", SpectacularAPIView.as_view(), name="schema")]
    if settings.API_SWAGGER:
        _urlpatterns += [
            path(
                "schema/swagger/",
                SpectacularSwaggerView.as_view(url_name="api_portal:schema"),
                name="swagger",
            )
        ]
    if settings.API_REDOC:
        _urlpatterns += [
            path(
                "schema/redoc/",
                SpectacularRedocView.as_view(url_name="api_portal:schema"),
                name="redoc",
            )
        ]
_urlpatterns += [
    path("version", GeoriviereVersionAPIView.as_view(), name="version"),
    path("", include(router.urls)),
]
urlpatterns = [path("api/portal/", include(_urlpatterns))]
