from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.views.i18n import JavaScriptCatalog

from main.views import home

admin.autodiscover()

urlpatterns = [
    path('', home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('paperclip/', include('paperclip.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('geotrek.altimetry.urls', namespace='altimetry')),
    path('', include('main.urls'), ),
    path('', include('mapentity.urls'),),
    path('', include('river.urls')),
    path('', include('description.urls')),
    path('', include('knowledge.urls')),
    path('', include('observations.urls')),
    path('', include('studies.urls')),
    path('', include('geotrek.zoning.urls')),
    path('', include('watershed.urls')),
    path('', include('finances_administration.urls')),
    path('', include('proceeding.urls')),
    path('', include('maintenance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
