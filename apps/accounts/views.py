from django.shortcuts import render


def reset_password(request):
    return render(request, "apps/accounts/reset_password.html")


def sign_in(request):
    return render(request, "apps/accounts/login.html")


def sign_up(request):
    return render(request, "apps/accounts/signup.html")
