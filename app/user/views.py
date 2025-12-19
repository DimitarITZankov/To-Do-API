# Views for user API

from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics, status

from rest_framework.response import Response

from core import models
from user import serializers, permissions

class RegisterViewSet(generics.CreateAPIView):
	# Register API
	serializer_class = serializers.RegisterSerializer
	permission_clases = [permissions.IsNotAuthenticated,]

	def create(self,request,*args,**kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({"message":"User registered successfully"}, status=status.HTTP_201_CREATED)
