from django.db import models
from customers.models import customers
from boxes.models import boxes
import datetime

class CustomPrimaryKeyField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return None
        else:
            now = datetime.datetime.now()
            present_year = now.year
            following_year = present_year + 1
            following_year_last_two_digits = following_year % 100
            financial_year_code = f"{present_year}-{following_year_last_two_digits:02d}"
            return f'GJ/S/{value}/{financial_year_code}'
        #CustomPrimaryKeyField(primary_key=True, max_length=10)

class sales(models.Model):

    metaltypes = (
        ('Gold','Gold'),
        ('Silver','Silver')
    )

    hsntypes = (
        ('7113','7113'),
        ('7114','7114')
    )

    puritytypes = (
        ('99.9','99.9'),
        ('91.6','91.6'),
        ('92.5', '92.5'),
        ('90.0','90.0'),
        ('85.0','85.0'),
        ('88 KDM','88 KDM'),
        ('85 kDM','85 KDM'),
        ('80.0','80.0'),
        ('78.0','78.0'),
        ('75.0','75.0'),
        ('70.0','70.0')
    )



    invoice_no = models.AutoField(primary_key=True)
    metal = models.CharField(max_length=10, null=False, choices=metaltypes )
    HSN_SAC_Code = models.CharField(max_length=4, null=False, choices=hsntypes )
    Purity = models.CharField(max_length=15, null=False, choices=puritytypes )
    ornament_type = models.CharField(max_length=100)
    HUID = models.CharField(max_length=10, null=True)
    item_sale_type = models.CharField(max_length=10, default = 'Retail')
    item_sale_12 = models.CharField(max_length=10)
    weight_with_tag = models.DecimalField(max_digits=10, decimal_places=3)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    stone_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3)
    value_added = models.DecimalField(max_digits=10, decimal_places=3)
    making_charge = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    stone_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_before_gst = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    amount_after_gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    declaration = models.CharField(max_length=100)
    old_metal_type = models.CharField(max_length=100, null=True, choices=metaltypes)
    old_items_type = models.CharField(max_length=100, null=True)
    old_items_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    old_items_dust = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    old_items_rate = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    old_items_touch = models.DecimalField(max_digits=10, decimal_places=2, null=True, choices=puritytypes )
    old_items_totalvalue = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    settled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unsettled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_id = models.ForeignKey(customers, on_delete=models.PROTECT, db_column='customer_id')
    box_id = models.ForeignKey(boxes, on_delete=models.PROTECT, db_column='box_id')
    cal_mode = models.CharField(max_length=100)
    sale_deleted = models.BooleanField(default=False)
    bycash = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    bycard = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    byupi = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    byib = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)


    def __str__(self):
        return self.sales

    def get_sales_for_customer(self, customer_id):
        print(sales.objects.filter(customer_id=customer_id).order_by('-sale_date'))
        return sales.objects.filter(customer_id=customer_id).order_by('-sale_date')

class sales2(models.Model):

    metaltypes = (
        ('Gold','Gold'),
        ('Silver','Silver')
    )

    hsntypes = (
        ('7113','7113'),
        ('7114','7114')
    )

    puritytypes = (
        ('99.9','99.9'),
        ('91.6','91.6'),
        ('92.5', '92.5'),
        ('90.0','90.0'),
        ('85.0','85.0'),
        ('88 KDM','88 KDM'),
        ('85 kDM','85 KDM'),
        ('80.0','80.0'),
        ('78.0','78.0'),
        ('75.0','75.0'),
        ('70.0','70.0')
    )

    invoice_no = models.AutoField(primary_key=True)
    metal = models.CharField(max_length=10, null=False, choices=metaltypes)
    HSN_SAC_Code = models.CharField(max_length=4, null=False, choices=hsntypes)
    Purity = models.CharField(max_length=15, null=False, choices=puritytypes)
    ornament_type = models.CharField(max_length=100)
    HUID = models.CharField(max_length=10, null=True)
    item_sale_type = models.CharField(max_length=10, default='Retail')
    item_sale_12 = models.CharField(max_length=10)
    weight_with_tag = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3)
    stone_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=3)
    value_added = models.DecimalField(max_digits=10, decimal_places=3)
    making_charge = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    stone_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_before_gst = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    amount_after_gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    declaration = models.CharField(max_length=100)
    old_metal_type = models.CharField(max_length=100, null=True, choices=metaltypes)
    old_items_type = models.CharField(max_length=100, null=True)
    old_items_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    old_items_dust = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    old_items_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    old_items_touch = models.DecimalField(max_digits=10, decimal_places=2, null=True, choices=puritytypes)
    old_items_totalvalue = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    settled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unsettled_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_id = models.ForeignKey(customers, on_delete=models.PROTECT, db_column='customer_id')
    box_id = models.ForeignKey(boxes, on_delete=models.PROTECT, db_column='box_id')
    cal_mode = models.CharField(max_length=100)
    sale_deleted = models.BooleanField(default=False)
    bycash = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    bycard = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    byupi = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    byib = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)


    def __str__(self):
        return self.sales2

