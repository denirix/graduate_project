from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
import logging

def index(request):
    return render(request,'schoolapp/index.html')

def news(request):
    return render(request,'schoolapp/news.html')

def study(request):
    return render(request,'schoolapp/study.html')

def about(request):
    return render(request,'schoolapp/about.html')

logger = logging.getLogger(__name__)

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
