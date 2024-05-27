from django.db import models
from django.contrib.auth.models import User
# Модель профиля пользователя, расширяющая базовую модель User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Мужской'), ('F', 'Женский')], blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'
# Модель курса
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_online = models.BooleanField(default=True)
# Модель урока в рамках курса
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=255, default='')
    description = models.TextField()
    video_url = models.URLField(default='')
    order = models.PositiveIntegerField()
# Модель заказа, сделанного пользователем
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='')
    courses = models.ManyToManyField(Course)
# Метод для расчета общей стоимости заказа
    def get_total_cost(self):
        total_cost = sum(course.price for course in self.courses.all())
        return total_cost
# Модель новости
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news_images', null=True, blank=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title
