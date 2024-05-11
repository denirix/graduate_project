from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db import models
from django.core.validators import EmailValidator

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator()])
    phone = forms.CharField(max_length=20, required=True)
    gender = forms.ChoiceField(choices=[('M', 'Мужской'), ('F', 'Женский')], required=True)
    birth_date = forms.DateField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone', 'gender', 'birth_date')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'

    def as_widget(self, widget=None, widget_type=None, widget_renderer=None):
        widgets = super().as_widget(widget, widget_type, widget_renderer)
        for field_name, field in self.fields.items():
            if field_name == 'password1' or field_name == 'password2':
                widgets[field_name].field.widget.render_value = False
        return widgets

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email
