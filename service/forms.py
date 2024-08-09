from django import forms
from .models import ServiceRequest, Equipment
from shop.models import Product

class ServiceRequestForm(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = ServiceRequest
        fields = ['name', 'company', 'email', 'phone', 'location', 'preferred_date', 'description', 'equipment', 'product', 'equipment_photo']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }