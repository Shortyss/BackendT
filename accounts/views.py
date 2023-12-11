from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

