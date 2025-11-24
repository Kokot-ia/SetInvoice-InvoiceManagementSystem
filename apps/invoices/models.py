from django.db import models
from apps.accounts.models import Users
from apps.customers.models import Customer
from apps.inventory.models import Item

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    invoice_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_id')
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    issue_date = models.DateField(db_index=True)
    due_date = models.DateField(db_index=True)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    notes = models.TextField(blank=True, null=True)
    term = models.TextField(blank=True, null=True, help_text="Payment Terms")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoice'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['customer']),
            models.Index(fields=['invoice_number']),
            models.Index(fields=['issue_date']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status', 'issue_date']),
        ]

    def __str__(self):
        return self.invoice_number

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('invoice_detail', kwargs={'invoice_id': self.invoice_id})
    
    def is_editable(self):
        """Check if invoice can be edited (only draft and pending invoices)"""
        return self.status in ['draft', 'pending']
    
    def is_finalized(self):
        """Check if invoice is finalized (paid or cancelled)"""
        return self.status in ['paid', 'cancelled']
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate invoice number (format: INV-2025-0001)"""
        if not self.invoice_number:
            from datetime import date
            today = date.today()
            year = today.year
            
            # Get the last invoice number for this year
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=f'INV-{year}-'
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                # Extract the sequence number and increment
                try:
                    last_seq = int(last_invoice.invoice_number.split('-')[-1])
                    new_seq = last_seq + 1
                except (ValueError, IndexError):
                    new_seq = 1
            else:
                new_seq = 1
            
            self.invoice_number = f'INV-{year}-{new_seq:04d}'
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate invoice data"""
        from django.core.exceptions import ValidationError
        
        # Validate due_date is after issue_date
        if self.due_date and self.issue_date and self.due_date <= self.issue_date:
            raise ValidationError({
                'due_date': 'Due date must be after issue date.'
            })
        
        # Validate amounts are positive
        if self.subtotal < 0:
            raise ValidationError({'subtotal': 'Subtotal must be positive.'})
        if self.tax_total < 0:
            raise ValidationError({'tax_total': 'Tax total must be positive.'})
        if self.discount < 0:
            raise ValidationError({'discount': 'Discount must be positive.'})
        if self.total_amount < 0:
            raise ValidationError({'total_amount': 'Total amount must be positive.'})

class Invoice_Item(models.Model):
    invoice_item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_column='invoice_id', related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_column='item_id')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.item.item_name}"
