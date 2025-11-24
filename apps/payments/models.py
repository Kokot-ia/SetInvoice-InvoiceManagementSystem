from django.db import models
from apps.accounts.models import Users
from apps.invoices.models import Invoice

class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online'),
    ]

    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_column='invoice_id', related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    payment_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['invoice']),
            models.Index(fields=['payment_date']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} for {self.invoice.invoice_number}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('payment_detail', kwargs={'payment_id': self.payment_id})
