from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class BaseUser(models.Model):
    phone_number = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CustomerUser(BaseUser):
    pass


class BrndAdmin(BaseUser):
    pass
