from django import forms
from .models import Item, Item_Category

class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = Item_Category
        fields = ['item_cat_name']
        widgets = {
            'item_cat_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_cat', 'item_name', 'qty', 'available_qty']
        widgets = {
            'item_cat': forms.Select(attrs={'class': 'form-select'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_qty': forms.NumberInput(attrs={'class': 'form-control'}),
        }
