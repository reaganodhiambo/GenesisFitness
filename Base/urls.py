from django.urls import path

from .views import *

urlpatterns = [
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("add-classes/", addClasses, name="add_classes"),
    path("edit-classes/<int:id>/", editClasses, name="edit_classes"),
    path("delete-classes/<int:id>/", deleteClasses, name="deleteClasses"),
    path("book-classes/", bookClasses, name="bookClasses"),
]
