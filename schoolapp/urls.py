from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name = "home"),
    path("news", views.news, name = "news"),
    path("study", views.study, name = "study"),
    path("aboutus", views.about, name = "about"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='schoolapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
