from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Логин',
                                      'class': 'body-register__input'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Пароль',
                                          'class': 'body-register__input'}),
    )


class CreationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Имя', 'class': 'body-register__input'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Фамилия', 'class': 'body-register__input'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Имя пользователя', 'class': 'body-register__input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'off', 'placeholder': 'Адрес эл. почты', 'class': 'body-register__input'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Пароль', 'class': 'body-register__input'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'placeholder': 'Подтвердить пароль', 'class': 'body-register__input'})
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
