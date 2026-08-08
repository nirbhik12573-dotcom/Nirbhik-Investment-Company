from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.conf import settings
import requests
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Student
from .forms import (
    StudentForm,
    StudentModelForm,
    CustomUserCreationForm,
    MessageForm,
)


# Only superusers can manage employees
def is_admin(user):
    return user.is_authenticated and user.is_superuser


def home(request):
    return render(request, "app/home.html")


def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                f"Account created successfully for {user.username}.",
            )

            return redirect("login")

    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "app/register.html",
        {
            "form": form,
        },
    )

def login_user(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                "Logged in successfully."
            )

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "app/login.html",
        {"next": next_url}
    )


@login_required
def logout_user(request):
    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


# Employee list
@login_required
def employee(request):
    students = Student.objects.all().order_by("name")

    paginator = Paginator(students, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "students": students,
        "page_obj": page_obj,
    }

    return render(
        request,
        "app/employee.html",
        context
    )


# Add employee: superuser only
@user_passes_test(is_admin, login_url="login")
def add_student(request):
    if request.method == "POST":
        form = StudentModelForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Employee added successfully."
            )

            return redirect("employee")
    else:
        form = StudentModelForm()

    return render(
        request,
        "app/add_student.html",
        {"form": form}
    )


# Update employee: superuser only
@user_passes_test(is_admin, login_url="login")
def update_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student.name = form.cleaned_data["name"]
            student.address = form.cleaned_data["address"]
            student.age = form.cleaned_data["age"]
            student.email = form.cleaned_data["email"]
            student.department = form.cleaned_data["department"]
            student.save()

            messages.success(
                request,
                "Employee updated successfully."
            )

            return redirect("employee")
    else:
        form = StudentForm(
            initial={
                "name": student.name,
                "address": student.address,
                "age": student.age,
                "email": student.email,
                "department": student.department,
            }
        )

    return render(
        request,
        "app/update_student.html",
        {"form": form}
    )


# Delete employee: superuser only
@user_passes_test(is_admin, login_url="login")
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()

    messages.success(
        request,
        "Employee deleted successfully."
    )

    return redirect("employee")


def about(request):
    return render(request, "app/about.html")


def contact(request):
    return render(
        request,
        "app/contact.html"
    )

@login_required
def message_us(request):
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            advice = form.cleaned_data["advice"]
            appointment_date = form.cleaned_data["appointment_date"]
            appointment_time = form.cleaned_data["appointment_time"]
            message_text = form.cleaned_data["message"]

            subject = f"New appointment request from {name}"

            email_body = f"""
New message from the Nirbhik Investment Company website.

Name:
{name}

Email:
{email}

Phone:
{phone}

Advice or service required:
{advice}

Preferred appointment date:
{appointment_date}

Preferred appointment time:
{appointment_time}

Message:
{message_text}
"""
try:
    if not settings.BREVO_API_KEY:
        raise ValueError("BREVO_API_KEY is missing.")

    brevo_url = "https://api.brevo.com/v3/smtp/email"

    brevo_headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    brevo_data = {
        "sender": {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL,
        },
        "to": [
            {
                "email": settings.CONTACT_EMAIL,
            }
        ],
        "replyTo": {
            "email": email,
            "name": name,
        },
        "subject": subject,
        "textContent": email_body,
    }

    response = requests.post(
        brevo_url,
        headers=brevo_headers,
        json=brevo_data,
        timeout=30,
    )

    response.raise_for_status()

    messages.success(
        request,
        "Your message was sent successfully.",
    )

    return redirect("message-success")

except requests.RequestException as error:
    print("BREVO API ERROR:", repr(error))

    messages.error(
        request,
        "The message could not be sent. Please try again later.",
    )

except Exception as error:
    print("EMAIL ERROR:", repr(error))

    messages.error(
        request,
        "An unexpected email error occurred.",
    )
def message_success(request):
    return render(
        request,
        "app/message_success.html"
    )