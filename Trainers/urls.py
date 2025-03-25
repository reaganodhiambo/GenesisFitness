from django.urls import path
from . import views

urlpatterns = [
    path("", views.trainerDashboard, name="trainers"),
    path("viewProfile/<int:id_number>/", views.viewProfile, name="viewProfile"),
    path("viewClasses/<int:id_number>/", views.viewClasses, name="viewClasses"),
    path("viewMembers", views.viewMembers, name="viewMembers"),
    path("generate-report/", views.generate_report, name="generate_report"),
    path(
        "create-profile/", views.create_trainer_profile, name="create_trainer_profile"
    ),
    path("view-profile/", views.view_trainer_profile, name="view_trainer_profile"),
    path("edit-profile/", views.edit_trainer_profile, name="edit_trainer_profile"),
    path("dashboard/", views.trainerDashboard, name="trainer_dashboard"),
]
