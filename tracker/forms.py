from django.forms import ModelForm, ValidationError, Textarea, DateField
from django.utils.translation import gettext_lazy as _

from .models import ExpenseTracker, Money

class TrackerForm(ModelForm):
    
    class Meta:
        model = ExpenseTracker
        fields = ["product", "product_count", "product_cost"]
        labels = {
            "product": _("Product name"),
        }
        
    def clean_product_count(self):
        product_count = self.cleaned_data.get('product_count')
        if product_count <= 0:
            raise ValidationError("Product count must be greater than zero.")
        return product_count