from django.db import models

class vendors(models.Model):

    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=100)
    vendor_address = models.CharField(max_length=200)
    vendor_address2 = models.CharField(max_length=200)
    ven_emailid = models.CharField(max_length=200, null=True)
    ven_gstin = models.CharField(max_length=15)
    ven_state = models.CharField(max_length=100)
    ven_state_code = models.CharField(max_length=100)
    ven_mobile_no = models.CharField(max_length=15)
    ven_mobile_no2 = models.CharField(max_length=15, null=True)
    ven_bank_name = models.CharField(max_length=10)
    ven_bank_branch = models.CharField(max_length=12)
    ven_ac_no = models.CharField(max_length=100)
    ven_ifsc_code = models.CharField(max_length=15)
    ven_deleted = models.BooleanField(default=False)
    ven_added_date = models.DateTimeField(auto_now_add=True)