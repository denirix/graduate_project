from django.contrib import admin
from .models import Course, Order, UserProfile, Lesson

admin.site.register(Course)
admin.site.register(Order)
admin.site.register(Lesson)
admin.site.register(UserProfile)

# Register your models here.
