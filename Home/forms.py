from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MemberProfile, Club, Event

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class MemberSignupForm(forms.ModelForm):
    clubs = forms.ModelMultipleChoiceField(queryset=Club.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = MemberProfile
        fields = ['full_name', 'email', 'phone_number', 'branch', 'semester', 'clubs' ]

    email = forms.EmailField(required=True)

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name']

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Event
        fields = ['event_name', 'date', 'time', 'organizing_club', 'event_description']

class ReportForm(forms.Form):
    name = forms.CharField(max_length=100, label="Event Name")
    date = forms.DateField(label="Event Date", widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea, label="Event Description")

