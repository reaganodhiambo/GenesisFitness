from django.urls import path
from .views import *
urlpatterns = [
    path("", home, name="home"),
    path("register/", registerUser, name="register"),
    path("login/", loginUser, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("members/", memberDashboard, name="members"),
    # path("trainers/", trainers, name="trainers"),
    # path("profile/", profile, name="profile"),
]
