from django.shortcuts import render
from django.core.exceptions import ValidationError

from .forms import TrackerForm, MoneyForm
from .models import ExpenseTracker, Money

from decimal import Decimal

# Create your views here.

def add_money_view(request):
    
    money_instance = Money.objects.first()
    balance = money_instance.total_money
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        if money_instance and amount:
            
            if Decimal(amount) <= 0:
                return render(request, 'tracker/add_money.html', {'message': 'Invalid number, please try again', "balance": balance})
            money_instance.add_money(Decimal(amount))
        
    return render(request, 'tracker/add_money.html', {"balance": balance})


def tracker_view(request):
    
    money_instance = Money.objects.first()
    
    if not money_instance:
            return render(request, 'tracker/tracker.html', {'error': 'No money instance found'})
        
    balance = money_instance.total_money

    if request.method == 'POST':
        
        product = request.POST.get('product')
        product_count = request.POST.get('product_count')
        product_cost = request.POST.get('product_cost')
        
        try:
            product_count = int(product_count)
            product_cost = Decimal(product_cost)
            
            tracker = ExpenseTracker(
                wallet =money_instance,
                product=product,
                product_count=product_count,
                product_cost=product_cost
            )
                        
            tracker.save()
            tracker.money_after_purchase()
                    
        except ValidationError as e:
            return render(request, 'tracker/tracker.html', {'error': str(e)})
        except (TypeError, ValueError):
            return render(request, 'tracker/tracker.html', {'error': 'Invalid input values'})
        
    tracker_obj = ExpenseTracker.objects.all()
    for i in tracker_obj:
        i.total_cost = i.product_cost * i.product_count
        
    return render(request, 'tracker/tracker.html', {"balance": balance, 'tracker':tracker_obj})