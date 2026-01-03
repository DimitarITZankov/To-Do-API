# Serializers for user API

from rest_framework import serializers
from core import models
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
	# Create register serializer
	password = serializers.CharField(write_only=True,style={'input_type':'password'})
	class Meta:
		model = get_user_model()
		fields = ['id','username','email','name','password']
		read_only_fields = ['id']
	def validate_password(self, value):
		# Validate the password field using the django's built-in validator
		validate_password(value)
		return value

	def create(self,validated_data):
		# Override the create method
		password = validated_data.pop('password')
		user = get_user_model().objects.create_user(password=password,**validated_data)
		return user

class ChangePasswordSerializer(serializers.Serializer):
	# Change password
	old_password = serializers.CharField(write_only=True)
	new_password_first = serializers.CharField(write_only=True)
	new_password_second = serializers.CharField(write_only=True)

	def validate(self,attrs):
		user = self.context['request'].user

		# Check if old password match
		if not user.check_password(attrs['old_password']):
			raise serializers.ValidationError('Old password is incorrect')

		# Check if the new password match
		if attrs['new_password_first'] != attrs['new_password_second']:
			raise serializers.ValidationError("Passwords do not match")

		return attrs