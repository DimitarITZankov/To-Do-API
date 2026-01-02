# Database models for our API

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.conf import settings

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


class Tasks(models.Model):
	# Create tasks model
	class Priority(models.TextChoices):
		LOW = 'low', 'Low'
		MEDIUM = 'medium', 'Medium'
		HIGH = 'high', 'High'
	title = models.CharField(max_length=100,null=False,blank=False)
	description = models.CharField(max_length=500)
	completed = models.BooleanField(default=False)
	priority = models.CharField(
		max_length=10,
		choices=Priority.choices,
		default=Priority.MEDIUM
	)
	public = models.BooleanField(default=True)
	due_date = models.DateField(null=True, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

	def __str__(self):
		return self.title
