from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if (CustomUser.objects
                .filter(email=email).exclude(pk=self.instance.pk).exists()):
            raise forms.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return email

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }


class PasswordEditForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
        help_text='''
            Ваш пароль должен содержать как минимум 8 символов.
            Ваш пароль не может состоять только из цифр.
        '''
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )

    class Meta:
        model = CustomUser
        fields = []

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError(
                'Пароль должен содержать как минимум 8 символов'
            )
        if password.isdigit():
            raise forms.ValidationError(
                'Пароль не может состоять только из цифр'
            )
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
