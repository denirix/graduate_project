from os import name
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Course, Order, News
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import logging

def index(request):
    return render(request,'schoolapp/index.html')

def study(request):
    query = request.GET.get('q', '') # Получает параметр поиска из запроса
    courses = Course.objects.filter(name__icontains=query) # Фильтрует курсы по названию
    paginated_courses = paginate_courses(request, courses) # Добавляет постраничный вывод курсов

    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user, status='ordered') # Получает все заказы пользователя со статусом 'ordered'
        purchased_courses = Course.objects.filter(order__in=user_orders)  # Получает все курсы, входящие в эти заказы
        cart, created = Order.objects.get_or_create(user=request.user, status='cart') # Создает или получает корзину пользователя со статусом 'cart'
        cart_courses = cart.courses.all() # Получает все курсы, находящиеся в корзине
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
        form = CustomUserCreationForm(request.POST) # Создает форму регистрации с данными из запроса
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
                logger.error(f'Error creating UserProfile: {e}') # Логирует ошибку при создании профиля пользователя
    else:
        form = CustomUserCreationForm() # Создает пустую форму регистрации
    return render(request, 'schoolapp/signup.html', {'form': form})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id) # Получает объект курса по id или возвращает 404
    context = {
        'course': course,
    }
    return render(request, 'schoolapp/course_detail.html', context)

@login_required
def course_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id) # Получает объект курса по id или возвращает 404
    lessons = course.lessons.order_by('order') # Получает уроки курса, отсортированные по порядку
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'schoolapp/course_lessons.html', context)

@login_required
def cart(request):
    cart, created = Order.objects.get_or_create(user=request.user, status='cart') # Создает или получает корзину пользователя со статусом 'cart'
    cart_courses = cart.courses.all() # Получает все курсы, находящиеся в корзине
    context = {
        'cart': cart,
        'cart_courses': cart_courses,
    }
    return render(request, 'schoolapp/cart.html', context)

@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id) # Получает объект курса по id или возвращает 404
    cart, created = Order.objects.get_or_create(user=request.user, status='cart') # Создает или получает корзину пользователя со статусом 'cart'
    cart.courses.add(course)

    current_url = request.META.get('HTTP_REFERER', 'study') # Возвращает пользователя на предыдущую страницу или на страницу курсов
    return redirect(current_url)

@login_required
def remove_from_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id) # Получает объект курса по id или возвращает 404
    cart, created = Order.objects.get_or_create(user=request.user, status='cart') # Создает или получает корзину пользователя со статусом 'cart'
    cart.courses.remove(course)
    return redirect('cart')

@login_required
def checkout(request):
    cart, _ = Order.objects.get_or_create(user=request.user, status='cart') # Создает или получает корзину пользователя со статусом 'cart'

    if request.method == 'POST':
        cart.status = 'ordered' # Обрабатывает POST-запрос на оформление заказа
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

    orders = Order.objects.filter(user=request.user, status='ordered') # Получает все заказы пользователя со статусом 'ordered'
    purchased_courses = Course.objects.filter(order__user=request.user, order__status='ordered').distinct() # Получает все курсы, купленные пользователем
    context = {
        'orders': orders,
        'purchased_courses': purchased_courses,
    }
    return render(request, 'schoolapp/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST) # Создает форму смены пароля с данными из запроса
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Обновляет сессию авторизации
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

def news(request):
    news_list = News.objects.order_by('-pub_date') # Получает все новости, отсортированные по дате публикации в обратном порядке
    context = {'news_list': news_list}
    return render(request, 'schoolapp/news.html', context)

def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id) # Получает объект новости по id или возвращает 404
    return render(request, 'schoolapp/news_detail.html', {'news': news_item})
