# Urls for Tasks API

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks import views

router = DefaultRouter()
router.register('tasks', views.TasksViewSet)
router.register('my-tasks', views.MyTasksViewSet, basename='my-tasks')
urlpatterns = [
	path('', include(router.urls))
]