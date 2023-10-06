from django.urls import path
from . import views

urlpatterns = [
    path("", views.LogInPage.as_view(), name="login"),
    path("ratings", views.HomePageView.as_view(), name="index"),
    path("login", views.LogInPage.as_view(), name="login"),
    path("mam_register", views.RegisterUser.as_view(), name="register"),
    path("logout", views.LogOutUser.as_view(), name="logout"),
    path("datapoint", views.DataPoint.as_view(), name="datapoint"),
]
