from django.urls import path
from . import views

urlpatterns = [
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("add-classes/", views.addClasses, name="add_classes"),
    path("edit-classes/<int:id>/", views.editClasses, name="edit_classes"),
    path("delete-classes/<int:id>/", views.deleteClasses, name="deleteClasses"),
    path("book-classes/<int:id_number>/", views.bookClasses, name="bookClasses"),
    path("membership/", views.membership, name="membership"),
    path("view-membership/", views.viewMembership, name="viewMembership"),
    path("view-booked-classes/", views.viewBookedClasses, name="viewBookedClasses"),
    path("cancel-booking/<int:booking_id>/", views.cancelBooking, name="cancelBooking"),
]
