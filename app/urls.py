from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "employee/",
        views.employee,
        name="employee"
    ),

    # Message and appointment pages
    path(
        "message-us/",
        views.message_us,
        name="message-us"
    ),

    path(
        "message-success/",
        views.message_success,
        name="message-success"
    ),

    # Employee pages
    path(
        "student/add/",
        views.add_student,
        name="add-student"
    ),

    path(
        "student/update/<int:id>/",
        views.update_student,
        name="update-student"
    ),

    path(
        "student/delete/<int:id>/",
        views.delete_student,
        name="delete-student"
    ),

    # Authentication pages
    path(
        "user/register/",
        views.register_user,
        name="register"
    ),

    path(
        "user/login/",
        views.login_user,
        name="login"
    ),

    path(
        "user/logout/",
        views.logout_user,
        name="logout"
    ),
]