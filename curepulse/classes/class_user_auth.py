from django.contrib.auth.models import User
from django.http import HttpResponse
from ..forms import LogInForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class UserAuth:
    def authenticateUser(request):
        if request.method == 'POST':
            form = LogInForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return user
                else:
                    return False
            return HttpResponse()

    def registerUser(request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                try:
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = User.objects.create_user(
                        username=username, password=password, is_active=True)
                    user.save()
                    return True
                except:
                    return False

    def logoutuser(request):
        logout(request)
        return True
