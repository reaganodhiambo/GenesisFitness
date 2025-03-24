from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", trainerDashboard, name="trainers"),
    # path("editProfile/<int:id_number>/", editProfile, name="editProfile"),
    path("viewProfile/<int:id_number>/", viewProfile, name="viewProfile"),
    path("viewClasses/<int:id_number>/", viewClasses, name="viewClasses"),
    path("viewMembers", viewMembers, name="viewMembers"),
    path("generate-report/", views.generate_report, name="generate_report"),
]
