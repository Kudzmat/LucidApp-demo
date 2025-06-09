from django import forms
from .models import StoreOrder
from sales.models import Inventory

class ExistingItemOrderForm(forms.ModelForm):
    # Field for selecting an existing inventory item
    existing_item = forms.ModelChoiceField(
        queryset=Inventory.objects.all(),
        required=True,  # Ensure this field is mandatory
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Existing Item"
    )

    class Meta:
        model = StoreOrder
        fields = ['date', 'existing_item', 'amount', 'quantity']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter item price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }
        labels = {
            'date': 'Order Date & Time',
            'amount': 'Item Price (USD) If price has changed',
            'quantity': 'Quantity',
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_item = cleaned_data.get('existing_item')
        new_item_name = cleaned_data.get('new_item_name')

        # Ensure at least one of the fields is filled
        if not existing_item and not new_item_name:
            raise forms.ValidationError("You must select an existing item or add a new item.")

        # If both fields are filled, prioritize the existing item
        if existing_item and new_item_name:
            cleaned_data['new_item_name'] = None  # Ignore new item name if existing item is selected

        return cleaned_data
    

class NewItemOrderForm(forms.ModelForm):
    # Field for adding a new inventory item name
    new_item_name = forms.CharField(
        required=True,  # Ensure this field is mandatory
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new item name'}),
        label="New Item Name"
    )

    class Meta:
        model = StoreOrder
        fields = ['date', 'new_item_name', 'amount', 'quantity']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter item price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }
        labels = {
            'date': 'Order Date & Time',
            'amount': 'New Item Price (USD)',
            'quantity': 'Quantity',
        }
