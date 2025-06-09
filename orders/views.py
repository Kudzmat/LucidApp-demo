from datetime import date, datetime
from django.shortcuts import render, redirect
from bank.models import BankTransaction
from .models import StoreOrder
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sales.models import Inventory

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
def create_existing_item_order(request):
    if request.method == "POST":
        form = ExistingItemOrderForm(request.POST)
        if form.is_valid():
            # get data from form
            date = form.cleaned_data['date']
            amount = form.cleaned_data['amount']
            quantity = form.cleaned_data['quantity']
            existing_item = form.cleaned_data.get('existing_item')

            

            store_item = Inventory.objects.get(id=existing_item.id)
            # Update the item's cost price if there's a new amount
            if amount is not None and amount > 0:
                store_item.cost_price = amount  # Update the cost price
                store_item.save()  # Save the updated item to the database
            else:
                amount = store_item.cost_price  # Use existing cost price if no new amount provided

            print(amount)

            # create store order
            new_store_order = StoreOrder.objects.create(
                date=form.cleaned_data.get('date'),
                item=existing_item,
                amount=store_item.cost_price,
                quantity=form.cleaned_data.get('quantity'),
            )
            new_store_order.save()


            # bank calculations
            # get current balance
            current_balance = get_current_balance()
            # calculate total cost
            total_cost = store_item.cost_price * quantity
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
                    description=f"Order for {quantity} x {store_item.name}",
                    debit=total_cost,
                    credit=0,
                    balance=new_balance,
                    notes=f"Order of {quantity} {store_item.name}(s) at ${store_item.cost_price} each."
                )
                bank_transaction.save() 

                messages.success(request, "Order created successfully!")
                return redirect('orders:new_existing_order')
    else:
        form = ExistingItemOrderForm()
    context = {
        'form': form,
        'current_balance': get_current_balance(),
    }
    return render(request, 'orders/restock.html', context)

@login_required
def create_new_item_order(request):
    if request.method == "POST":
        form = NewItemOrderForm(request.POST)
        if form.is_valid():
            # get data from form
            date = form.cleaned_data['date']
            amount = form.cleaned_data['amount']
            quantity = form.cleaned_data['quantity']
            new_item_name = form.cleaned_data.get('new_item_name')

            # create new inventory item
            new_inventory_item = Inventory.objects.create(
                name=new_item_name,
                cost_price=amount,
                quantity=0,  # Initial quantity set to 0 until order is delivered
            )
            new_inventory_item.save()

            # create store order
            new_store_order = StoreOrder.objects.create(
                date=form.cleaned_data.get('date'),
                item=new_inventory_item,
                amount=form.cleaned_data.get('amount'),
                quantity=form.cleaned_data.get('quantity'),
            )
            new_store_order.save()

            # bank calculations
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
                    description=f"Order for {quantity} x {new_inventory_item.name}",
                    debit=total_cost,
                    credit=0,
                    balance=new_balance,
                    notes=f"Order of {quantity} {new_inventory_item.name}(s) at ${amount} each."
                )
                bank_transaction.save() 

                messages.success(request, "Order created successfully!")
                return redirect('orders:new_order')
    else:
        form = NewItemOrderForm()
    context = {
        'form': form,
        'current_balance': get_current_balance(),
    }
    return render(request, 'orders/new_stock.html', context)

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
        order_id = request.POST.get('order_id')  # Get order ID for display
        try:
            order = StoreOrder.objects.get(id=order_id)

            if order:
                # Toggle the delivered status
                order.delivered = not order.delivered
                order.save()

                # Update inventory quantity if the order is marked as delivered
                if order.delivered:
                    inventory_item = Inventory.objects.get(id=order.item.id)
                    inventory_item.quantity += order.quantity  # Reduce inventory quantity
                    inventory_item.save()

                    messages.success(request, f"Order marked as delivered for {order.item}. Inventory updated.")
                else:
                    messages.success(request, f"Order status updated for {order.item}.")
            else:
                messages.error(request, "Order not found.")
        except StoreOrder.DoesNotExist:
            messages.error(request, "Order not found.")
        except Inventory.DoesNotExist:
            messages.error(request, "Inventory item not found.")

    context = {
        'orders': orders,
        'current_balance': get_current_balance(),
        'selected_month': selected_month,
    }
    return render(request, 'orders/view_orders.html', context)

@login_required
def view_inventory(request):
    inventory_items = Inventory.objects.all()
    context = {
        'inventory_items': inventory_items,
        'current_balance': get_current_balance(),
    }
    return render(request, 'orders/view_inventory.html', context)