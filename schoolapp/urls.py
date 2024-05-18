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
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('add-to-cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('course/<int:course_id>/lessons/', views.course_lessons, name='course_lessons'),
]
