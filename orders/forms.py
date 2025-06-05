from django import forms
from .models import StoreOrder

class StoreOrderForm(forms.ModelForm):
    class Meta:
        model = StoreOrder
        fields = ['date', 'item', 'amount', 'quantity',]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Item price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }
        labels = {
            'date': 'Order Date & Time',
            'item': 'Item Name',
            'amount': 'Item Price (USD)',
            'quantity': 'Quantity',
        }
