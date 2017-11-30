# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from . import views
from .view import city, province

# admin.autodiscover()

# urlpatterns = [
#     url(r'^sitemap\.xml$', sitemap,
#         {'sitemaps': {'cmspages': CMSSitemap}}),
# ]

urlpatterns = i18n_patterns(
    # url(r'^filer/', include('filer.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/load$', views.data_load),
    url(r'^data/import$', views.data_import),
    url(r'^data/filter$', views.data_filter),
    url(r'^data/add$', views.data_add),
    url(r'^data/update$', views.data_update),
    url(r'^data/delete$', views.data_delete),
    url(r'^data/geojson$', views.data_geojson),
    url(r'^form/shapefile$', views.shapefile_create),
    url(r'^form/raster$', views.raster_calculate),
    url(r'^form/upload_file$', views.upload_file),
    url(r'^gis/city/save$', city.saveToORM),
    url(r'^gis/city/get$', city.getAll),
    url(r'^gis/province/save$', province.saveToORM),
    url(r'^gis/province/get$', province.getAll),
    url(r'^$', views.index),
    # url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
