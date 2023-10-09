"""_summary: 
This file contains the class for user authentication.
"""

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from ..forms import LogInForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class UserAuth:
    
    """_summary_
    This class is used to authenticate the user.
    """
    
    def authenticateUser(request : HttpRequest) -> HttpResponse:
        """_summary_
        This function is used to authenticate the user.
        Args:
            request (HttpRequest): _description_

        Returns:
            HttpResponse: _description_
        """
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

    def registerUser(request : HttpRequest) -> bool:
        """_summary_
        This function is used to register the user.
        Args:
            request (HttpRequest): _description_

        Returns:
            bool: _description_
        """
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

    def logoutuser(request : HttpRequest) -> bool:
        """_summary_
        This function is used to logout the user.
        Args:
            request (HttpRequest): _description_

        Returns:
            bool: _description_
        """
        logout(request)
        return True
