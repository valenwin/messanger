from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from ..models import Thread, Message

from .serializers import ThreadSerializer, MessageSerializer
from ...accounts.models import User


class ThreadView(generics.ListCreateAPIView):
    """
    Thread list view
    Create new thread with 2 participants only
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get information about one thread by pk
    Update thread
    Destroy thread and thread's messages while there no participants
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def get(self, request, *args, **kwargs):
        """
        Get thread and destroy thread and thread's messages while there no participants
        """
        instance = self.get_object()
        instance_participants = self.get_object().participants
        if instance_participants.count() == 0:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.retrieve(request, *args, **kwargs)


@api_view(["GET"])
def messages_list(request, pk):
    """
    Get list messages for thread
    """
    thread = get_object_or_404(Thread, pk=pk)
    return Response(data=MessageSerializer(thread.thread_messages.all(), many=True).data)


@permission_classes(
    [
        IsOwnerOrReadOnly,
    ]
)
@api_view(["GET"])
def messages_read(request, pk):
    """
    Set is_read True if message unread
    """
    thread = get_object_or_404(Thread, pk=pk)
    messages = Message.objects.filter(
        thread=thread, thread__participants__id=request.user.id
    )
    messages.update(is_read=True)
    return Response(data=MessageSerializer(messages, many=True).data)


@permission_classes(
    [
        IsOwnerOrReadOnly,
    ]
)
@api_view(
    [
        "POST",
    ]
)
def message_create(request, pk):
    """
    Create message for thread
    """
    thread = Thread.objects.filter(pk=pk, participants__id=request.user.id).first()
    if thread is None:
        raise ValidationError("You are not thread participant.")
    sender = get_object_or_404(User, pk=request.user.id)
    serializer = MessageSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    serializer.save(sender=sender, thread=thread, text=request.data.get("text"))
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@permission_classes(
    [
        IsOwnerOrReadOnly,
    ]
)
@api_view(["GET", "PUT", "DELETE"])
def message_details(request, pk):
    """
    Get, update, delete message by pk
    """
    message = get_object_or_404(Message, pk=pk)

    if request.method == "GET":
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = MessageSerializer(message, data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
