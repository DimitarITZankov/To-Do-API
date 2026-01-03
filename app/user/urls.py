# URLs for user API

from django.urls import path, include
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# This is used for out test case where its searching for user in the URL (reverse function)
app_name = 'user'

router = DefaultRouter()
router.register('me', views.UserProfileViewSet,basename='me')

urlpatterns = [
	# JWT Endpoints
	path('login-jwt/', TokenObtainPairView.as_view(), name='login-jwt'),
	path('refresh-jwt/', TokenRefreshView.as_view(), name='refresh-jwt'),

	# Register Endpoint
	path('register/', views.RegisterViewSet.as_view(),name='register'),

	# Change Password Endpoint
	path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

	# Router Endpoints
	path('', include(router.urls)),
]