# forms.py
from django import forms
from .models import StorePurchase, OnlinePurchase

class StorePurchaseForm(forms.ModelForm):
    class Meta:
        model = StorePurchase
        fields = [
            'date', 'item', 'amount', 'quantity',
            'customer_name', 'customer_email', 'customer_address',
            'sold_by'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_address': forms.TextInput(attrs={'class': 'form-control'}),
            'sold_by': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OnlinePurchaseForm(forms.ModelForm):
    class Meta:
        model = OnlinePurchase
        exclude = ['sold_by']  # Explicitly exclude inherited field
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_address': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),
            'channel': forms.Select(attrs={'class': 'form-select'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'delivered': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
