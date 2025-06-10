# forms.py
from django import forms
from .models import *
from django.contrib.auth.models import User

class StorePurchaseForm(forms.Form):
    # Fields for StorePurchase
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Purchase Date"
    )
    item = forms.ModelChoiceField(
        queryset=Inventory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Item"
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Quantity"
    )
    sold_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Sold By"
    )

    # Fields for Customer details
    customer_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer Name"
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Customer Email"
    )
    customer_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer Address"
    )
    customer_city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer City"
    )
    customer_country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer Country"
    )

class OnlinePurchaseForm(forms.Form):
    # Fields for OnlinePurchase
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Purchase Date"
    )
    item = forms.ModelChoiceField(
        queryset=Inventory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Item"
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Quantity"
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Assigned To"
    )
    delivery_method = forms.ChoiceField(
        choices=[('standard', 'Standard Shipping'), ('express', 'Express Shipping'), ('pickup', 'In-Store Pickup')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Delivery Method"
    )
    channel = forms.ChoiceField(
        choices=[('website', 'Website'), ('whatsapp', 'WhatsApp'), ('instagram', 'Instagram')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Channel"
    )

    # Fields for Customer details
    customer_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer Name"
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Customer Email"
    )
    customer_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer Address"
    )
    customer_city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer City"
    )
    customer_country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Customer Country"
    )