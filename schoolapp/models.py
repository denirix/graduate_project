from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', max_length=15)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Мужской'), ('F', 'Женский')], blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'
