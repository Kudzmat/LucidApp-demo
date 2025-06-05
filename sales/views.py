from django.shortcuts import render, redirect
from .forms import StorePurchaseForm, OnlinePurchaseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def new_sale(request):
    form = StorePurchaseForm(request.POST or None)
    if request.method == 'POST':
        store_form = StorePurchaseForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Store purchase recorded successfully!")
            return redirect('sales:new_sale')
    else:
        form = StorePurchaseForm()

    context = {
        'form': form,
    }
    return render(request, 'sales/store_sale.html', context)

@login_required
def new_online_sale(request):
    form = OnlinePurchaseForm(request.POST or None)
    if request.method == 'POST':
        online_form = OnlinePurchaseForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Online purchase recorded successfully!")
            return redirect('sales:new_online_sale')
    else:
        form = OnlinePurchaseForm()

    context = {
        'form': form,
    }
    return render(request, 'sales/online_sale.html', context)