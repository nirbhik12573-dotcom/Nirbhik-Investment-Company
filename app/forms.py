from django import forms
from .models import Department,Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

class StudentForm(forms.Form):
    name=forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder":"Enter your name"})
    )
    address=forms.CharField()
    email=forms.EmailField()
    age=forms.IntegerField()
    department= forms.ModelChoiceField(
        queryset=Department.objects.all()
    )

class StudentModelForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["name","address","email","age","department"]

        widget={
            "name": forms.TextInput(
               attrs={
                    "placeholder":"Enter your name",
                    "class":"w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
                }
            ),
            "address":forms.TextInput(
                attrs={
                    "placeholder":"Enter your Address",
                    "class":"w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
                }
            )
        }


class MessageForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
            "placeholder": "Enter your full name",
        })
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
            "placeholder": "Enter your email address",
        })
    )

    phone = forms.CharField(
        max_length=20,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
            "placeholder": "Enter your phone number",
        })
    )

    advice = forms.CharField(
        max_length=200,
        label="What advice do you need?",
        widget=forms.TextInput(attrs={
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
            "placeholder": "Example: Investment planning",
        })
    )

    appointment_date = forms.DateField(
        label="Preferred Appointment Date",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
        })
    )

    appointment_time = forms.TimeField(
        label="Preferred Appointment Time",
        widget=forms.TimeInput(attrs={
            "type": "time",
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
        })
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "rows": 6,
            "class": (
                "w-full rounded-xl border border-slate-300 px-4 py-3 "
                "text-sm outline-none transition "
                "focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
            ),
            "placeholder": "Write your message here...",
        })
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