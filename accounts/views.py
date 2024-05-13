from rest_framework import mixins, generics
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import BrndAdmin, CustomerUser
from accounts.serializers import BrndAdminSerializer, LogInSerializer, CustomerUserSerializer


# Create your views here.
class BrndAdminRegistrationAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = BrndAdmin.objects.all()
    serializer_class = BrndAdminSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerUserRegistrationAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
