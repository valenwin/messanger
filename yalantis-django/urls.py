import debug_toolbar
from . import views

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", views.index, name="index"),
    path("about-us", views.about_us, name="about_us"),
    path("authors", views.authors, name="authors"),
    path("contacts", views.contacts, name="contacts"),
]
