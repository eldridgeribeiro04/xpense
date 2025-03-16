from django.forms import ModelForm
from .models import ExpenseTracker, Money

class MoneyForm(ModelForm):
    
    class Meta:
        model = Money
        fields = ["total_money"]


class TrackerForm(ModelForm):
    
    class Meta:
        model = ExpenseTracker
        fields = ["wallet", "product", "product_count", "product_cost"]