from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    order_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']