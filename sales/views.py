from django.shortcuts import render, redirect
from .forms import StorePurchaseForm, OnlinePurchaseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bank.models import BankTransaction
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
def new_store_sale(request):
    if request.method == 'POST':
        form = StorePurchaseForm(request.POST)
        if form.is_valid():
            # Create the Customer object
            new_customer = Customer.objects.create(
                name=form.cleaned_data['customer_name'],
                email=form.cleaned_data['customer_email'],
                address=form.cleaned_data['customer_address'],
                city=form.cleaned_data['customer_city'],
                country=form.cleaned_data['customer_country']
            )
            new_customer.save()

            # Update the inventory
            inventory_item = Inventory.objects.get(id=form.cleaned_data['item'].id)
            inventory_item.quantity -= form.cleaned_data['quantity']
            inventory_item.save()

            # calculate the total price
            item_price = inventory_item.cost_price
            total_price = item_price * form.cleaned_data['quantity']

            # check bank balance
            current_balance = get_current_balance()
            credit = total_price
            new_balance = current_balance + credit
            # Create a new bank transaction
            BankTransaction.objects.create(
                date=form.cleaned_data['date'],
                description=f"Store Purchase: {form.cleaned_data['item']}",
                debit=0,
                credit=credit,
                balance=new_balance,
                notes=f"Sold by {form.cleaned_data['sold_by']}"
            )

            # Create the StorePurchase object
            StorePurchase.objects.create(
                date=form.cleaned_data['date'],
                item=form.cleaned_data['item'],
                amount=total_price,
                quantity=form.cleaned_data['quantity'],
                customer_details=new_customer,  # Link the new customer
                sold_by=form.cleaned_data['sold_by']  # Link the selected user
            )

            return redirect('sales:new_sale')  # Redirect to a success page
    else:
        form = StorePurchaseForm()

        context = {
        'form': form,
        'current_balance': get_current_balance(),
        'success_message': None,
    }

    return render(request, 'sales/store_sale.html', context=context)

@login_required
def new_online_sale(request):
    if request.method == 'POST':
        form = OnlinePurchaseForm(request.POST)
        if form.is_valid():
                        # Create the Customer object
            new_customer = Customer.objects.create(
                name=form.cleaned_data['customer_name'],
                email=form.cleaned_data['customer_email'],
                address=form.cleaned_data['customer_address'],
                city=form.cleaned_data['customer_city'],
                country=form.cleaned_data['customer_country']
            )
            new_customer.save()

            # Update the inventory
            inventory_item = Inventory.objects.get(id=form.cleaned_data['item'].id)
            inventory_item.quantity -= form.cleaned_data['quantity']
            inventory_item.save()

            # calculate the total price
            item_price = inventory_item.cost_price
            total_price = item_price * form.cleaned_data['quantity']

            # check bank balance
            current_balance = get_current_balance()
            credit = total_price
            new_balance = current_balance + credit
            # Create a new bank transaction
            bank_transaction = BankTransaction.objects.create(
                date=form.cleaned_data['date'],
                description=f"Online Purchase: {form.cleaned_data['item']}",
                debit=0,
                credit=credit,
                balance=new_balance,
                notes=f"Online Sale Assigned to {form.cleaned_data['assigned_to']}"
            )
            bank_transaction.save()

            # Create the StorePurchase object
            OnlinePurchase.objects.create(
                date=form.cleaned_data['date'],
                item=form.cleaned_data['item'],
                amount= total_price,
                quantity=form.cleaned_data['quantity'],
                customer_details=new_customer,  # Link the new customer
                assigned_to=form.cleaned_data['assigned_to']  # Link the selected user
                )
            messages.success(request, "Online sale recorded successfully!")
            return redirect('sales:new_online_sale')    # Redirect to a success page
    else:
        form = OnlinePurchaseForm()

    context = {
        'form': form,
        'current_balance': get_current_balance(),
        'success_message': None,
    }
    return render(request, 'sales/online_sale.html', context)