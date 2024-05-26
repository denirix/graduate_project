from os import name
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Course, Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import logging

def index(request):
    return render(request,'schoolapp/index.html')

def news(request):
    return render(request,'schoolapp/news.html')

def study(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(name__icontains=query)
    paginated_courses = paginate_courses(request, courses)

    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user, status='ordered')
        purchased_courses = Course.objects.filter(order__in=user_orders)
        cart, created = Order.objects.get_or_create(user=request.user, status='cart')
        cart_courses = cart.courses.all()
    else:
        purchased_courses = []
        cart_courses = []

    context = {
        'courses': paginated_courses,
        'purchased_courses': purchased_courses,
        'cart_courses': cart_courses,
    }
    return render(request, 'schoolapp/study.html', context)

def about(request):
    return render(request,'schoolapp/about.html')

logger = logging.getLogger(name)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                UserProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data.get('phone'),
                    gender=form.cleaned_data.get('gender'),
                    birth_date=form.cleaned_data.get('birth_date')
                )
                login(request, user)
                return redirect('home')
            except Exception as e:
                logger.error(f'Error creating UserProfile: {e}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'schoolapp/signup.html', {'form': form})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {
        'course': course,
    }
    return render(request, 'schoolapp/course_detail.html', context)

@login_required
def course_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.order_by('order')
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'schoolapp/course_lessons.html', context)

@login_required
def cart(request):
    cart, created = Order.objects.get_or_create(user=request.user, status='cart')
    cart_courses = cart.courses.all()
    context = {
        'cart': cart,
        'cart_courses': cart_courses,
    }
    return render(request, 'schoolapp/cart.html', context)

@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    cart, created = Order.objects.get_or_create(user=request.user, status='cart')
    cart.courses.add(course)

    current_url = request.META.get('HTTP_REFERER', 'study')
    return redirect(current_url)

@login_required
def remove_from_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    cart, created = Order.objects.get_or_create(user=request.user, status='cart')
    cart.courses.remove(course)
    return redirect('cart')

@login_required
def checkout(request):
    cart, _ = Order.objects.get_or_create(user=request.user, status='cart')

    if request.method == 'POST':
        cart.status = 'ordered'
        cart.save()
        messages.success(request, 'Спасибо за покупку!')
        return redirect(reverse('home'))

    context = {
        'cart': cart,
    }
    return render(request, 'schoolapp/checkout.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            request.user.profile.profile_picture = profile_picture
            request.user.profile.save()
            return redirect('profile')

    orders = Order.objects.filter(user=request.user, status='ordered')
    purchased_courses = Course.objects.filter(order__user=request.user, order__status='ordered').distinct()
    context = {
        'orders': orders,
        'purchased_courses': purchased_courses,
    }
    return render(request, 'schoolapp/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменен.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'schoolapp/change_password.html', {'form': form})

def paginate_courses(request, courses):
    paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return courses
