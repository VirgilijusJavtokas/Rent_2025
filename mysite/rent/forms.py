from .models import Profile, Reservation
from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class DateInput(forms.DateInput):
    input_type = 'date'

class ReservationCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'start_date', 'end_date']
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}

