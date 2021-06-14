from django.urls import path

import apps.accounts.views as views

urlpatterns = [
    path("reset-password/", views.reset_password, name="reset_password"),
    path("sign-in/", views.sign_in, name="sign_in"),
    path("sign-up/", views.sign_up, name="sign_up"),
]
