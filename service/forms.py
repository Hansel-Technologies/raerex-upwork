from django import forms
from .models import ServiceRequest, Equipment

class ServiceRequestForm(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = ServiceRequest
        fields = ['name', 'email', 'location', 'preferred_date', 'description', 'equipment']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }