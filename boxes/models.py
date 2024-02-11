from django.db import models
import datetime

class boxes(models.Model):

    box_id = models.AutoField(primary_key=True)
    box_name = models.CharField(max_length=100)
    box_metal = models.CharField(max_length=100)
    box_total_weight = models.DecimalField(max_digits=10, decimal_places=3)
    box_added_date = models.DateTimeField(auto_now_add=True)
    box_deleted = models.BooleanField(default=False)

class boxes_history(models.Model):
    box_name = models.CharField(max_length=100)
    box_added_weight = models.DecimalField(max_digits=10, decimal_places=3)
    box_existed_weight = models.DecimalField(max_digits=10, decimal_places=3)
    box_total_weight = models.DecimalField(max_digits=10, decimal_places=3)
    item_purchase_12 = models.CharField(max_length=10)
    purchase_id = models.CharField(max_length=10)
    box_id = models.ForeignKey(boxes, on_delete=models.PROTECT, db_column='box_id')
    box_updated_date = models.DateTimeField(auto_now_add=True)

class boxes_sale_history(models.Model):
    box_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    item_weight = models.DecimalField(max_digits=10, decimal_places=3)
    item_sale_type = models.CharField(max_length=100)
    item_sale_12 = models.CharField(max_length=10)
    sale_id = models.CharField(max_length=10)
    box_id = models.ForeignKey(boxes, on_delete=models.PROTECT, db_column='box_id')
    box_updated_date = models.DateTimeField(auto_now_add=True)



