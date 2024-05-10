from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request,'schoolapp/index.html')

def news(request):
    return render(request,'schoolapp/news.html')

def study(request):
    return render(request,'schoolapp/study.html')

def about(request):
    return render(request,'schoolapp/about.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'schoolapp/signup.html', {'form': form})
