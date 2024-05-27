from django.contrib import admin
from .models import Course, Order, UserProfile, Lesson, News

admin.site.register(Course)
admin.site.register(Order)
admin.site.register(Lesson)
admin.site.register(UserProfile)
admin.site.register(News)
