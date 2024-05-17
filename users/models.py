from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birth_day = models.DateField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    another_information = models.TextField(blank=True, null=True)
    scientific_degree = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='users_photo/', blank=True, null=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class PasswordResets(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'password_resets'
        unique_together = (('user', 'created_at'),)
        index_together = (('user', 'created_at'),)
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'


