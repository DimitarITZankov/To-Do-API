# Serializers for Tasks API

from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model


class TasksSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for Tasks API
    Used for creating and listing tasks
    """
    class Meta:
        model = models.Tasks
        fields = ('id', 'title', 'description', 'priority', 'user')
        read_only_fields = ('id', 'user')
        extra_kwargs = {
            'priority': {'required': True},
            'public': {'required': True},
        }


class TasksDetailedSerializer(TasksSerializer):
    """
    Detailed serializer for Tasks API
    Includes extra fields like completed and due_date
    """
    class Meta(TasksSerializer.Meta):
        fields = ('id', 'title', 'description', 'completed', 'priority', 'public', 'due_date', 'user')
        read_only_fields = ('id', 'completed', 'user')
        extra_kwargs = {
            'priority': {'required': True},
            'public': {'required': True},
        }