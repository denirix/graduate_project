from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', max_length=15, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Мужской'), ('F', 'Женский')], blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_online = models.BooleanField(default=True)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=255, default='')
    description = models.TextField()
    video_url = models.URLField(default='')
    order = models.PositiveIntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='')
    courses = models.ManyToManyField(Course)

    def get_total_cost(self):
        total_cost = sum(course.price for course in self.courses.all())
        return total_cost
