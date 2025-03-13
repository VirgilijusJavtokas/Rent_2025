from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
        }
