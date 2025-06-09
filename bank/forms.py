from django import forms


class WithdrawalForm(forms.Form):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Enter the date and time of the event")
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ATM withdrawal, cash out...'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount to withdraw'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))


class DepositForm(forms.Form):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Enter the date and time of the event")
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Payment for order, supplier...'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Amount to pay'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}))