from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests', 'special_requests']
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        if check_in and check_out:
            # Check that check-in is not in the past
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")
            
            # Check that check-out is after check-in
            if check_out <= check_in:
                raise forms.ValidationError("Check-out date must be after check-in date.")
        
        return cleaned_data
