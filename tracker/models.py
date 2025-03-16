from django.db import models
from django.core.exceptions import ValidationError

from decimal import Decimal

# Create your models here.

class Money(models.Model):
    total_money = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)
    
    def add_money(self, added_money):
        self.total_money += Decimal(added_money)
        self.save()
        return self.total_money
    
    def __str__(self):
        if self.total_money:
            return str(f"£{self.total_money} as on {self.date_added}")
        else:
            return f"Account balance as of {self.date_added} is zero"


class ExpenseTracker(models.Model):
    wallet = models.ForeignKey(Money, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    product_count = models.PositiveIntegerField()
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def total_cost(self):
        return self.product_cost * self.product_count
        
    def money_after_purchase(self):
        total_cost = self.product_cost * self.product_count
        
        if total_cost > self.wallet.total_money:
            raise ValidationError("You do not have sufficient funds for this!")
        
        self.wallet.total_money -= total_cost
        self.wallet.save()
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.money_after_purchase()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.product
    