from django.db import models
from apps.accounts.models import Users

class Item_Category(models.Model):
    item_cat = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    item_cat_name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'item_category'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['item_cat_name']),
        ]

    def __str__(self):
        return self.item_cat_name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    item_cat = models.ForeignKey(Item_Category, on_delete=models.CASCADE, db_column='item_cat')
    item_name = models.CharField(max_length=255, db_index=True)
    qty = models.IntegerField(default=0)
    available_qty = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['item_name']),
            models.Index(fields=['available_qty']),
            models.Index(fields=['item_cat']),
        ]

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('item_list')
