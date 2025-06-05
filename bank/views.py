from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *

# function for getting most recent account balance
def get_current_balance():
    last_entry = BankTransaction.objects.order_by('-date').first()

    if last_entry:
        current_balance = last_entry.balance
    else:
        current_balance = 0  # Default value if no entries exist

    return current_balance

# Create your views here.
@login_required
def withdrawal(request):
    form = WithdrawalForm(request.POST)
    if request.method == "POST":
        if form.is_valid():

            # get data from form
            date=form.cleaned_data['date'],
            description=form.cleaned_data['description'],
            amount=form.cleaned_data['amount'],
            notes=form.cleaned_data['notes']

            # get current balance
            current_balance = get_current_balance()
            # calculate new balance
            new_balance = current_balance - amount
      
            # create a new transaction
            transaction = BankTransaction.objects.create(
                date=date,
                description=description,
                debit=amount,
                credit=0,
                balance=new_balance,  # This will be updated below
                notes=notes
            )
            transaction.save()

            messages.success(request, "Withdrawal recorded successfully!")
            return redirect('bank:withdrawal')
    else:
        form = WithdrawalForm()

    context = {
        'form': form,
        'current_balance': get_current_balance(),
    }
    return render(request, 'bank/withdrawal.html', context)

@login_required
def deposit(request):
    form = DepositForm(request.POST)
    if request.method == "POST":
        if form.is_valid():

            # get data from form
            date=form.cleaned_data['date'],
            description=form.cleaned_data['description'],
            amount=form.cleaned_data['amount'],
            notes=form.cleaned_data['notes']

            # get current balance
            current_balance = get_current_balance()
            # calculate new balance
            new_balance = current_balance + amount
      
            # create a new transaction
            transaction = BankTransaction.objects.create(
                date=date,
                description=description,
                debit=0,
                credit=amount,
                balance=new_balance,  # This will be updated below
                notes=notes
            )
            transaction.save()

            messages.success(request, f"Deposit recorded successfully!")
            return redirect('bank:deposit')
    else:
        form = DepositForm()

    context = {
        'form': form,
        'current_balance': get_current_balance(),
    }
    return render(request, 'bank/deposit.html', context)

@login_required
def view_statement(request):
    transactions = BankTransaction.objects.all().order_by('-date')
    current_balance = get_current_balance()

    context = {
        'transactions': transactions,
        'current_balance': current_balance,
    }
    return render(request, 'bank/statement.html', context)

