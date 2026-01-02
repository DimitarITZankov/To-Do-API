# Views for Tasks API

from django.shortcuts import render
from core import models
from rest_framework import viewsets, mixins
from tasks import serializers, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class TasksViewSet(viewsets.ModelViewSet):
	# Viewset for Tasks API
	serializer_class = serializers.TasksSerializer
	permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]
	authentication_classes = [JWTAuthentication,]
	queryset = models.Tasks.objects.all()

	def perform_create(self,serializer):
		# Assign the author to the authenticated user
		return serializer.save(user=self.request.user)

	def get_queryset(self):
		# Return only tasks what are with status PUBLIC
		return self.queryset.filter(public=True).all()

class MyTasksViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
	# See only tasks that belong to the authenticated user
	serializer_class = serializers.TasksSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = [JWTAuthentication,]
	queryset = models.Tasks.objects.all()

	def get_queryset(self):
		# Return only tasks what belong to the authenticated user
		return self.queryset.filter(user=self.request.user).all()