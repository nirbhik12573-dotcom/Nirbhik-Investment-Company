from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Department, Student


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email address",
    )

    first_name = forms.CharField(
        required=True,
        max_length=100,
        label="First name",
    )

    last_name = forms.CharField(
        required=True,
        max_length=100,
        label="Last name",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class StudentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your name",
            }
        ),
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your address",
            }
        ),
    )

    email = forms.EmailField()
    age = forms.IntegerField()

    department = forms.ModelChoiceField(
        queryset=Department.objects.all()
    )


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student

        fields = [
            "name",
            "address",
            "email",
            "age",
            "department",
        ]

        # It must be "widgets", not "widget".
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your name",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Enter your address",
                }
            ),
        }


class MessageForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
    )

    email = forms.EmailField(
        label="Email Address",
    )

    phone = forms.CharField(
        max_length=20,
        label="Phone Number",
    )

    advice = forms.CharField(
        max_length=200,
        label="What advice do you need?",
    )

    appointment_date = forms.DateField(
        label="Preferred Appointment Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    appointment_time = forms.TimeField(
        label="Preferred Appointment Time",
        widget=forms.TimeInput(
            attrs={
                "type": "time",
            }
        ),
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={
                "rows": 6,
            }
        ),
    )

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]

        if appointment_date.weekday() >= 5:
            raise forms.ValidationError(
                "Appointments are available from Monday to Friday only."
            )

        return appointment_date

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data["appointment_time"]

        if appointment_time.hour < 8 or appointment_time.hour >= 20:
            raise forms.ValidationError(
                "Please select a time between 8:00 AM and 8:00 PM."
            )

        return appointment_time