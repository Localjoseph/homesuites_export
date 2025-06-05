from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'address', 'city', 'country', 'zip_code',
                  'price_per_night', 'bedrooms', 'bathrooms', 'accommodates',
                  'property_type', 'amenities', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'amenities': forms.CheckboxSelectMultiple(),
        }


class PropertyImageForm(forms.ModelForm):
    # For single image uploads
    class Meta:
        model = PropertyImage
        fields = ['image']


class PropertySearchForm(forms.Form):
    location = forms.CharField(required=False, label='City or Country')
    check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.IntegerField(required=False, min_value=1)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    property_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + Property.PROPERTY_TYPES
    )
    bedrooms = forms.IntegerField(required=False, min_value=0)
