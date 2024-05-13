from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LogInView, BrndAdminRegistrationAPIView, CustomerUserRegistrationAPIView

urlpatterns = [
    path('login/', LogInView.as_view(),name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/brnd-admin/', BrndAdminRegistrationAPIView.as_view(), name='brnd_admin_registration'),
    path('register/customer/', CustomerUserRegistrationAPIView.as_view(), name='customer_user_registration'),
]
