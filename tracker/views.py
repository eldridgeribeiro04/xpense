from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from .forms import *

from .models import ExpenseTracker, Money

from decimal import Decimal 

# Create your views here.

def add_money_view(request):
    money_instance = Money.objects.first()
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        if money_instance and amount:
            
            if Decimal(amount) <= 0:
                return render(request, 'tracker/add_money.html', {'message': 'Invalid number, please try again', "balance": balance})
            money_instance.add_money(Decimal(amount))
            
    balance = money_instance.total_money
        
    return render(request, 'tracker/add_money.html', {"balance": balance})


def tracker_view(request):
    money_instance = Money.objects.first()
    
    if not money_instance:
            return render(request, 'tracker/tracker.html', {'error': 'No money instance found'})

    if request.method == 'POST':
        form = TrackerForm(request.POST)

        if form.is_valid():
            tracker = form.save(commit=False)
            
            if tracker.product_cost * tracker.product_count > money_instance.total_money:
                    return render(request, 'tracker/tracker.html', {'error': 'Insufficient funds!'})
              
            # tracker.money_after_purchase()
            tracker.wallet = money_instance
            tracker.save()
        
    tracker_obj = ExpenseTracker.objects.all()
        
    for i in tracker_obj:
        i.total_cost = i.product_cost * i.product_count
    
    balance = money_instance.total_money
    form = TrackerForm()
                
    return render(request, 'tracker/tracker.html', {'balance': balance, 'tracker':tracker_obj, 'form': form})


def update_product(request, pk):
    tracker = get_object_or_404(ExpenseTracker, pk=pk)
    money_instance = Money.objects.first()
        
    if request.method == 'POST':
        form = TrackerForm(request.POST, instance=tracker)
        money_instance.total_money += (tracker.product_cost * tracker.product_count)
        # money_instance.save()
        
        if form.is_valid():
            updated_tracker = form.save(commit=False)
            
            total_cost = updated_tracker.product_cost * updated_tracker.product_count
            if total_cost > money_instance.total_money:
                return render(request, 'tracker/update.html', {'tracker': tracker, 'error': 'Insufficient funds!'})

            money_instance.save()
            
            tracker.money_after_purchase()
            updated_tracker.wallet = money_instance
            updated_tracker.save()
            
            return redirect('tracker')
    
    else:
        form = TrackerForm(instance=tracker)
        
    return render(request, "tracker/update.html", {'tracker': tracker, 'form': form})


def delete_product(request, pk):
    tracker = get_object_or_404(ExpenseTracker, pk=pk)
    tracker.wallet.total_money += tracker.product_count * tracker.product_cost
    tracker.wallet.save()
    tracker.delete()

    return redirect('tracker')
