# Serializers for Tasks API

from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model

class TasksSerializer(serializers.ModelSerializer):
	# Serializer for Tasks API
	class Meta:
		model = models.Tasks
		fields = ('id','title','description','completed','priority','public','due_date','user')
		read_only_fields = ('id','completed','user')
	extra_kwargs = {
            'priority': {'required': True},
            'public': {'required': True},
        }