from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db import models
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from datetime import date
import phonenumbers

phone_validator = RegexValidator(r'^\+?\d{1,20}$', 'Пожалуйста, введите действительный номер телефона.')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator()])
    phone = forms.CharField(max_length=20, required=True, validators=[phone_validator])
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

    def clean_username(self):
         username = self.cleaned_data.get('username')
         if User.objects.filter(username=username).exists():
             raise forms.ValidationError('Этот username уже занят.')
         return username

    def clean_phone(self):
       phone = self.cleaned_data.get('phone')
       try:
           parsed_phone = parse(phone, None)
           if not is_valid_number(parsed_phone):
               raise forms.ValidationError('Некорректный номер телефона.')
           formatted_phone = format_number(parsed_phone, PhoneNumberFormat.INTERNATIONAL)
           return formatted_phone
       except phonenumbers.phonenumberutil.NumberParseException:
           raise forms.ValidationError('Некорректный номер телефона.')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if not birth_date:
            return birth_date

        min_date = date(2006, 1, 1)
        max_date = date.today()

        if birth_date >= max_date:
            raise ValidationError('Дата рождения не может быть позже сегодняшней даты.')
        if birth_date >= min_date:
            raise ValidationError('Вы должны быть старше 18 лет.')

        return birth_date
