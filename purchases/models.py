from django.db import models
from vendors.models import vendors
from boxes.models import boxes

# Create your models here.
class purchases(models.Model):
    metaltypes = (
        ('Gold', 'Gold'),
        ('Silver', 'Silver')
    )

    hsntypes = (
        ('7113', '7113'),
        ('7114', '7114')
    )

    puritytypes = (
        ('99.9', '99.9'),
        ('91.6', '91.6'),
        ('92.5', '92.5'),
        ('90.0', '90.0'),
        ('85.0', '85.0'),
        ('88 KDM', '88 KDM'),
        ('85 kDM', '85 KDM'),
        ('80.0', '80.0'),
        ('78.0', '78.0'),
        ('75.0', '75.0'),
        ('70.0', '70.0')
    )

    purchase_id = models.AutoField(primary_key=True)
    bill_no = models.CharField(max_length=30)
    inv_date = models.CharField(max_length=50)
    metal = models.CharField(max_length=50, null=False, choices=metaltypes)
    description = models.CharField(max_length=50, null=True)
    Purity = models.CharField(max_length=15, null=False, choices=puritytypes)
    HSN_SAC_Code = models.CharField(max_length=4, null=False, choices=hsntypes)
    item_purchase_12 = models.CharField(max_length=10)
    less_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    tcs = models.DecimalField(max_digits=10, decimal_places=2)
    rounded_off = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    declaration = models.CharField(max_length=100)
    settled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unsettled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor_id = models.ForeignKey(vendors, on_delete=models.PROTECT, db_column='customer_id')
    box_id = models.ForeignKey(boxes, on_delete=models.PROTECT, db_column='box_id')
    purchase_deleted = models.BooleanField(default=False)
    delivery_mode = models.CharField(max_length=50)
    #image = models.ImageField(upload_to='images/', null=True)


class purchases2(models.Model):
    metaltypes = (
        ('Gold', 'Gold'),
        ('Silver', 'Silver')
    )

    hsntypes = (
        ('7113', '7113'),
        ('7114', '7114')
    )

    puritytypes = (
        ('99.9', '99.9'),
        ('91.6', '91.6'),
        ('92.5', '92.5'),
        ('90.0', '90.0'),
        ('85.0', '85.0'),
        ('88 KDM', '88 KDM'),
        ('85 kDM', '85 KDM'),
        ('80.0', '80.0'),
        ('78.0', '78.0'),
        ('75.0', '75.0'),
        ('70.0', '70.0')
    )

    purchase_id = models.AutoField(primary_key=True)
    bill_no = models.CharField(max_length=30)
    inv_date = models.CharField(max_length=50)
    metal = models.CharField(max_length=50, null=False, choices=metaltypes)
    description = models.CharField(max_length=50, null=True)
    Purity = models.CharField(max_length=15, null=False, choices=puritytypes)
    HSN_SAC_Code = models.CharField(max_length=4, null=False, choices=hsntypes)
    item_purchase_12 = models.CharField(max_length=10)
    less_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    tcs = models.DecimalField(max_digits=10, decimal_places=2)
    rounded_off = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    declaration = models.CharField(max_length=100)
    settled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unsettled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor_id = models.ForeignKey(vendors, on_delete=models.PROTECT, db_column='customer_id')
    box_id = models.ForeignKey(boxes, on_delete=models.PROTECT, db_column='box_id')
    purchase_deleted = models.BooleanField(default=False)
    delivery_mode = models.CharField(max_length=50)
    #image = models.ImageField(upload_to='images/', null=True)

