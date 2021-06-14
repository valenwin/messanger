from django.conf import settings
from django.db import models
from .managers import MessageManager


class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return (
            f"Message: {self.id}; "
            f"Read: {self.is_read}; "
            f"{self.created_at.strftime('%d, %b %Y - %Hh %Mm')}"
        )
