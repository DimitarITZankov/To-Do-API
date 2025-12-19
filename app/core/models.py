# Database models for our API

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

class CustomUserManager(BaseUserManager):
	# Create custom base user manager
	def create_user(self,email,password=None,**extra_fields):
		# Create user
		if not email:
			raise ValueError("Every user must provide email")
		user = self.model(email=self.normalize_email(email),**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,password,**extra_fields):
		# Create superuser
		user = self.create_user(email,password,**extra_fields)
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	# Custom user model
	username = models.CharField(max_length=255,unique=True)
	email = models.EmailField(max_length=255,unique=True)
	name = models.CharField(max_length=50)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	# We assign the custom model to custom user manager
	objects = CustomUserManager()

	# Assign login and required fields
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name','username']

	# Helper Functions
	def get_full_name(self):
		return self.name
	def get_short_name(self):
		return self.name
	def __str__(self):
		return self.username
