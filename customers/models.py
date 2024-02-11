from django.db import models
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
            return f'GJ/C/{value}/{financial_year_code}'
        #CustomPrimaryKeyField(primary_key=True, max_length=10)

class customers(models.Model):

    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=200)
    customer_address2 = models.CharField(max_length=200)
    cus_emailid = models.CharField(max_length=200, null=True)
    cus_gstin = models.CharField(max_length=15, null=True)
    cus_state = models.CharField(max_length=100)
    cus_state_code = models.CharField(max_length=100)
    cus_mobile_no = models.CharField(max_length=15)
    cus_mobile_no2 = models.CharField(max_length=15, null=True)
    cus_pan_no = models.CharField(max_length=10, null=True)
    cus_aadhar_no = models.CharField(max_length=12, null=True)
    cus_kyc = models.CharField(max_length=100)
    cus_added_date = models.DateTimeField(auto_now_add=True)
    cus_deleted = models.BooleanField(default=False)