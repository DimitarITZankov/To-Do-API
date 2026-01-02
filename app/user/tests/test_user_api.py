# Tests for User API

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:register')
JWT_TOKEN_URL = reverse('user:login-jwt')
ME_URL = reverse('user:me-list')

def create_user(**params):
	# Create and return a new user
	return get_user_model().objects.create_user(**params)

class PublicUserAPI(TestCase):
	# Test the public features of API
	def setUp(self):
		self.client = APIClient()

	def test_create_user_successfully(self):
		# Test creating a user successful
		data = {
			'username':'Test Username',
			'email':'test@test.com',
			'name':'Test Name',
			'password':'TestPassword123!'
		}
		result = self.client.post(CREATE_USER_URL,data,format='json')
		self.assertEqual(result.status_code,status.HTTP_201_CREATED)

	def test_create_user_existing_email(self):
		# Test creating a user with existing email
		data = {
			'username':'Test Username',
			'email':'test@test.com',
			'name':'Test Name',
			'password':'TestPassword123!'
		}
		create_user(**data)
		result = self.client.post(CREATE_USER_URL,data,format='json')
		self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)

	def test_create_user_short_password(self):
		# Test creating a user with too short password
		data = {
			'username':'Test Username',
			'email':'test@test.com',
			'name':'Test Name',
			'password':'pw'
		}
		result = self.client.post(CREATE_USER_URL,data,format='json')
		self.assertEqual(result.status_code,status.HTTP_400_BAD_REQUEST)
		# Check if the user is created with the short password
		user_exists = get_user_model().objects.filter(email=data['email']).exists()
		self.assertFalse(user_exists)

	def test_create_jwt(self):
		# Test creating and returning access and refresh tokens
		user_data = {
			'username':'Test Username',
			'email':'test@test.com',
			'name':'Test Name',
			'password':'pw'
		}
		create_user(**user_data)
		data = {
			'email':user_data['email'],
			'password':user_data['password']
		}
		result = self.client.post(JWT_TOKEN_URL,data,format='json')
		self.assertEqual(result.status_code,status.HTTP_200_OK)
		# Check if we have both of the codes
		self.assertIn('access',result.data)
		self.assertIn('refresh',result.data)

	def test_bad_credentials_jwt(self):
		# Test logging in with bad credentials
		create_user(email='email@email.com',password='password123')
		data = {'email':'email@email.com','password':'password456'}
		result = self.client.post(JWT_TOKEN_URL,data,format='json')
		self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertNotIn('access',result.data)
		self.assertNotIn('refresh',result.data)

	def test_jwt_blank_password(self):
		# Test if it returns error on blank password as it should
		data = {'email':'test@example.com', 'password':''}
		result = self.client.post(JWT_TOKEN_URL, data)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

	def test_retrieve_user_unauthorized(self):
		# Test that authentication is required for endpoint /me/
		result = self.client.get(ME_URL)
		self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)