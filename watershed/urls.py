from django.urls import path
from . import views


app_name = 'watershed'
urlpatterns = [
    path('api/watershed/watershed.geojson', views.WatershedGeoJSONLayer.as_view(), name="watershed_layer"),
    path('api/watershed/type/<int:type_pk>/watershed.geojson', views.WatershedTypesGeoJSONLayer.as_view(),
         name="watershed_type_layer"),
]
