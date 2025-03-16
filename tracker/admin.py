from django.contrib import admin
from .models import ExpenseTracker, Money
# Register your models here.

admin.site.register(Money)
admin.site.register(ExpenseTracker)