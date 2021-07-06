from django.urls import path

from apps.dialogs.api import views

app_name = "threads"

urlpatterns = [
    path("threads/", views.ThreadView.as_view(), name="thread_list"),
    path("threads/<pk>/", views.ThreadDetailView.as_view(), name="thread_details"),
    path("threads/<pk>/messages/", views.messages_list, name="message_list"),
    path("threads/<pk>/messages/read/", views.messages_read, name="message_read"),
    path("threads/<pk>/messages/create/", views.message_create, name="message_create"),
    path("messages/<pk>/", views.message_details, name="message_details"),
]
