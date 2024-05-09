from django.contrib import admin
from django.urls import include, path

from dokku_demo.home import urls as home_urls

urlpatterns = [
    path("", include(home_urls)),
    path("django-admin/", admin.site.urls),
]
