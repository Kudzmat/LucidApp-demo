from datetime import date, datetime
from django.shortcuts import render, redirect
from bank.models import BankTransaction
from .models import StoreOrder
from .forms import StoreOrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
def new_order(request):
    form = StoreOrderForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # get data from form
            date = form.cleaned_data['date']
            item = form.cleaned_data['item']
            amount = form.cleaned_data['amount']
            quantity = form.cleaned_data['quantity']
            delivered = form.cleaned_data['delivered']

            # get current balance
            current_balance = get_current_balance()
            # calculate total cost
            total_cost = amount * quantity
            # check if sufficient balance
            if total_cost > current_balance:
                messages.error(request, "Insufficient balance for this order.")
                return redirect('orders:new_order')
            else:
                # get new balance
                new_balance = current_balance - total_cost
                # update the bank transaction
                bank_transaction = BankTransaction.objects.create(
                    date=date,
                    description=f"Order for {quantity} x {item}",
                    debit=total_cost,
                    credit=0,
                    balance=new_balance,
                    notes=f"Order of {quantity} {item}(s) at ${amount} each."
                )
                bank_transaction.save()    
                form.save()
                messages.success(request, "Order created successfully!")
                return redirect('orders:new_order')
    else:
        form = StoreOrderForm()
    context = {
        'form': form,
        'current_balance': get_current_balance(),
    }
    return render(request, 'orders/new_order.html', context)

@login_required
def view_store_orders(request):
    # Get the selected month from the query parameters
    selected_month = request.GET.get('month', datetime.now().strftime('%Y-%m'))  # Default to the current month

    # Parse the selected month into year and month
    try:
        # Split the selected_month string (e.g., "2025-05") into year and month as integers.
        # map(int, ...) converts the split strings into integers.
        year, month = map(int, selected_month.split('-'))
    except ValueError:
        # If the selected_month is invalid (e.g., not in "YYYY-MM" format),
        # fall back to the current year and month using datetime.now().
        year, month = datetime.now().year, datetime.now().month

    orders = StoreOrder.objects.filter(date__year=year, date__month=month)

    if request.method == 'POST':
        # Handle toggling of the order_delivered option
        order_id = request.POST.get('order_id')  # get order id for display
        order = StoreOrder.objects.get(id=order_id)

        if order:
            order.delivered = not order.delivered
            order.save()
            messages.success(request, f"Order status updated for {order.item}.")
        else:
            messages.error(request, "Order not found.")

    context = {
        'orders': orders,
        'current_balance': get_current_balance(),
        'selected_month': selected_month,
    }
    return render(request, 'orders/view_orders.html', context)