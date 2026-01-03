# Views for Tasks API

from django.shortcuts import render
from core import models
from rest_framework import viewsets, mixins, status
from tasks import serializers, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

class TasksViewSet(viewsets.ModelViewSet):
	# Viewset for Tasks API
	serializer_class = serializers.TasksDetailedSerializer
	permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]
	authentication_classes = [JWTAuthentication,]
	queryset = models.Tasks.objects.all()

	def perform_create(self,serializer):
		# Assign the author to the authenticated user
		return serializer.save(user=self.request.user)

	def get_queryset(self):
		# Return only tasks what are with status PUBLIC
		return self.queryset.filter(public=True,completed=False).all()

	def get_serializer_class(self):
		# Return the right serializer based on the request
		if self.action in ['list', 'create']:
			return serializers.TasksSerializer
		return serializers.TasksDetailedSerializer

	@action(
		detail=True,
		methods=['post'],
		url_path='complete-task',
		permission_classes=[IsAuthenticated, permissions.IsOwnerOrReadOnly]
	)
	def complete_task(self, request, pk=None):
		task = self.get_object()

		if task.completed:
			return Response(
				{"detail": "Task is already completed."},
				status=status.HTTP_400_BAD_REQUEST
			)

		task.completed = True
		task.save()

		serializer = self.get_serializer(task)
		return Response(serializer.data, status=status.HTTP_200_OK)

class MyTasksViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
	# See only tasks that belong to the authenticated user
	serializer_class = serializers.TasksDetailedSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = [JWTAuthentication,]
	queryset = models.Tasks.objects.all()

	def get_queryset(self):
		# Return only tasks what belong to the authenticated user
		return self.queryset.filter(user=self.request.user,completed=False).all()


class CompletedTasksViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
	# See only completed tasks assigned to the authenticated user
	serializer_class = serializers.TasksDetailedSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = [JWTAuthentication,]
	queryset = models.Tasks.objects.all()

	def get_queryset(self):
		# Return only tasks what belong to the authenticated user
		return self.queryset.filter(user=self.request.user,completed=True).all()

class AllTasksViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
	# See all tasks to users that set them up to PUBLIC
	serializer_class = serializers.TasksDetailedSerializer
	permission_classes = [IsAuthenticated,]
	authentication_classes = [JWTAuthentication,]
	queryset = models.Tasks.objects.all()

	def get_queryset(self):
		# Return only tasks what belong to the authenticated user
		return self.queryset.filter(public=True,completed=False).all()