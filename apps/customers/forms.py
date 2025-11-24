from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'contact_no', 'email', 'address', 'city', 'status']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
    
    def clean_contact_no(self):
        """Validate phone number format"""
        import re
        contact_no = self.cleaned_data.get('contact_no')
        if contact_no:
            # Remove spaces and dashes
            cleaned = re.sub(r'[\s\-]', '', contact_no)
            # Check if it's numeric and has reasonable length (10-15 digits)
            if not cleaned.isdigit() or len(cleaned) < 10 or len(cleaned) > 15:
                raise forms.ValidationError('Please enter a valid phone number (10-15 digits).')
        return contact_no
