from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, Invoice_Item

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'issue_date', 'due_date', 'notes', 'term', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'term': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean(self):
        """Validate that due_date is after issue_date"""
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        due_date = cleaned_data.get('due_date')
        
        if issue_date and due_date and due_date <= issue_date:
            raise forms.ValidationError('Due date must be after issue date.')
        
        return cleaned_data

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = Invoice_Item
        fields = ['item', 'description', 'quantity', 'price', 'tax_rate']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-select item-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control price-input', 'min': '0', 'step': '0.01'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control tax-input', 'min': '0', 'max': '100', 'step': '0.01'}),
        }
    
    def clean_quantity(self):
        """Validate quantity is positive and doesn't exceed available stock"""
        quantity = self.cleaned_data.get('quantity')
        item = self.cleaned_data.get('item')
        
        if quantity and quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        
        if item and quantity:
            if quantity > item.available_qty:
                raise forms.ValidationError(
                    f'Quantity ({quantity}) exceeds available stock ({item.available_qty}).'
                )
        
        return quantity
    
    def clean_price(self):
        """Validate price is positive"""
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError('Price must be positive.')
        return price
    
    def clean_tax_rate(self):
        """Validate tax rate is between 0 and 100"""
        tax_rate = self.cleaned_data.get('tax_rate')
        if tax_rate and (tax_rate < 0 or tax_rate > 100):
            raise forms.ValidationError('Tax rate must be between 0 and 100.')
        return tax_rate

InvoiceItemFormSet = inlineformset_factory(
    Invoice, Invoice_Item, form=InvoiceItemForm,
    extra=1, can_delete=True
)
