from django.urls import path
from rest_framework_jwt import views

app_name = "users"

urlpatterns = [path("login/", views.obtain_jwt_token)]