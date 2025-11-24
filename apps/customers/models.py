from django.db import models
from apps.accounts.models import Users

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    customer_name = models.CharField(max_length=255, db_index=True)
    contact_no = models.CharField(max_length=20) # Changed to CharField for flexibility
    email = models.EmailField(db_index=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['customer_name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.customer_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('customer_list')
