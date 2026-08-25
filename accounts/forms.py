from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'sx-input',
            'placeholder': 'e.g. Ama Konadu'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'sx-input',
            'placeholder': 'e.g. Owusu'
        })
    )
    student_id = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'sx-input',
            'placeholder': 'e.g. 20244001'
        })
    )
    course = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'sx-input',
            'placeholder': 'e.g. Computer Science'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'sx-input',
            'placeholder': 'you@knust.edu.gh'
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'student_id',
            'course', 'email', 'username', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to default fields
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'sx-input'})
        self.fields['username'].widget.attrs['placeholder'] = 'e.g. ama_k'
        self.fields['password1'].widget.attrs['placeholder'] = 'Choose a strong password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your password'


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':       'sx-input',
            'placeholder': 'Enter your username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':       'sx-input',
            'placeholder': 'Enter your password',
        })
    )
