from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def about_us(request):
    return HttpResponse("About Us")


def contacts(request):
    return HttpResponse("Contacts")


def authors(request):
    return HttpResponse("Authors")
