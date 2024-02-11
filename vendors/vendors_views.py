from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import vendors
from purchases.models import purchases, purchases2
from purchases import purchases_views
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.db.models import F, Q, ExpressionWrapper, DecimalField
import re
# Create your views here.

def vendors_home(request):
    all_vendors = vendors.objects.all().order_by('-ven_added_date')
    filtered_vendors = all_vendors.exclude(Q(ven_deleted = True))
    return render(request,"vendors.html",{'vendors':filtered_vendors})

def vendors_deleted(request):
    all_vendors = vendors.objects.all().order_by('-ven_added_date')
    filtered_vendors = all_vendors.exclude(Q(ven_deleted = False))
    return render(request,"deleted_vendors.html",{'vendors':filtered_vendors})

def new_vendor(request):
    if request.method =="POST":
        if request.POST.get('vendor_name')\
            and request.POST.get('vendor_address')\
            and request.POST.get('vendor_address2') \
            and request.POST.get('ven_state') \
            and request.POST.get('ven_state_code') \
            and request.POST.get('ven_mobile_no'):
            # and request.POST.get('cus_emailid') \
            # and request.POST.get('cus_gstin') \
            # and request.POST.get('cus_pan_no') \
            # and request.POST.get('cus_aadhar_no') \
            #and request.POST.get('cus_mobile_no2') \
            vend = vendors()
            vend.vendor_name = request.POST.get('vendor_name').strip()
            vend.vendor_address = request.POST.get('vendor_address').strip()
            vend.vendor_address2 = request.POST.get('vendor_address2').strip()
            vend.ven_emailid = request.POST.get('ven_emailid').strip()
            vend.ven_gstin = request.POST.get('ven_gstin').strip()
            vend.ven_state = request.POST.get('ven_state').strip()
            vend.ven_state_code = request.POST.get('ven_state_code').strip()
            vend.ven_mobile_no = request.POST.get('ven_mobile_no').strip()
            vend.ven_mobile_no2 = request.POST.get('ven_mobile_no2').strip()
            vend.ven_bank_name = request.POST.get('ven_bank_name').strip()
            vend.ven_bank_branch = request.POST.get('ven_bank_branch').strip()
            vend.ven_ac_no = request.POST.get('ven_ac_no').strip()
            vend.ven_ifsc_code = request.POST.get('ven_ifsc_code').strip()
            vend.save()
            return HttpResponseRedirect('/vendors')
    else:
        return render(request,'new_vendor.html')

def vendor(request, vendor_id):
    vend = vendors.objects.get(vendor_id=vendor_id)
    #sales_of_cust = sales.objects.all().order_by('-sale_date')#
    purchases_from_vend = purchases.objects.all().filter(vendor_id = vendor_id.strip()).filter(purchase_deleted=False).order_by('-inv_date')
    '''sales.objects.all().filter(customer_id=customer_id.strip()) \
        .order_by('-sale_date') \
        .annotate(cus_id_no = ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField()))
    for sale in sales_of_cust:
        customer_id_number = re.search(r'\d+', str(sale.customer_id))
        sale.customer_id = customer_id_number.group(0)'''
    return render(request, "view_vendor.html", {'vendor': vend, 'purchases': purchases_from_vend})

def edit_vendor(request, vendor_id):
    if request.method =="POST":
        if request.POST.get('vendor_name')\
            and request.POST.get('vendor_address')\
            and request.POST.get('vendor_address2')\
            and request.POST.get('ven_state')\
            and request.POST.get('ven_state_code')\
            and request.POST.get('ven_mobile_no')\
            and request.POST.get('ven_gstin'):
            # and request.POST.get('ven_emailid')
            # and request.POST.get('ven_mobile_no2')
            # and request.POST.get('ven_bank_name')
            # and request.POST.get('ven_bank_branch')
            # and request.POST.get('ven_ac_no')
            # and request.POST.get('ven_ifsc_code')
            vend = vendors.objects.get(vendor_id=vendor_id)
            vend.vendor_name = request.POST.get('vendor_name')
            vend.vendor_name = vend.vendor_name.strip()
            vend.vendor_address = request.POST.get('vendor_address')
            vend.vendor_address = vend.vendor_address.strip()
            vend.vendor_address2 = request.POST.get('vendor_address2')
            vend.vendor_address2 = vend.vendor_address2.strip()
            vend.ven_emailid = request.POST.get('ven_emailid')
            vend.ven_emailid = vend.ven_emailid.strip()
            vend.ven_mobile_no2 = request.POST.get('ven_mobile_no2')
            vend.ven_mobile_no2 = vend.ven_mobile_no2.strip()
            vend.ven_state = request.POST.get('ven_state')
            vend.ven_state = vend.ven_state.strip()
            vend.ven_state_code = request.POST.get('ven_state_code')
            vend.ven_state_code = vend.ven_state_code.strip()
            vend.ven_mobile_no = request.POST.get('ven_mobile_no')
            vend.ven_mobile_no = vend.ven_mobile_no.strip()
            vend.ven_bank_name = request.POST.get('ven_bank_name')
            vend.ven_bank_name = vend.ven_bank_name.strip()
            vend.ven_bank_branch = request.POST.get('ven_bank_branch')
            vend.ven_bank_branch = vend.ven_bank_branch.strip()
            vend.ven_ac_no = request.POST.get('ven_ac_no')
            vend.ven_ac_no = vend.ven_ac_no.strip()
            vend.ven_ifsc_code = request.POST.get('ven_ifsc_code')
            vend.ven_ifsc_code = vend.ven_ifsc_code.strip()
            vend.ven_gstin = request.POST.get('ven_gstin')
            vend.ven_gstin = vend.ven_gstin.strip()

            vendors.objects.filter(vendor_id=vendor_id).update(vendor_name=vend.vendor_name,
                                                               vendor_address=vend.vendor_address,
                                                               vendor_address2=vend.vendor_address2,
                                                               ven_emailid=vend.ven_emailid,
                                                               ven_state=vend.ven_state,
                                                               ven_state_code=vend.ven_state_code,
                                                               ven_mobile_no=vend.ven_mobile_no,
                                                               ven_mobile_no2=vend.ven_mobile_no2,
                                                               ven_bank_name=vend.ven_bank_name,
                                                               ven_bank_branch=vend.ven_bank_branch,
                                                               ven_ac_no=vend.ven_ac_no,
                                                               ven_ifsc_code=vend.ven_ifsc_code,
                                                               ven_gstin=vend.ven_gstin)
            return HttpResponseRedirect('/vendors')
    else:
        vend = vendors.objects.get(vendor_id=vendor_id)
        return render(request, "edit_vendor.html", {'vendor': vend})

def delete_vendor(request, vendor_id):
    #cust = customers.objects.get(customer_id = customer_id)
    vendors.objects.filter(vendor_id = vendor_id).update(ven_deleted = True)
    return HttpResponseRedirect('/vendors')

def add_vendor_back(request, vendor_id):
    vendors.objects.filter(vendor_id=vendor_id).update(ven_deleted=False)
    return HttpResponseRedirect('/vendors')

def delete_vendor_complete(request, vendor_id):
    vend = vendors.objects.get(vendor_id=vendor_id)
    vend.delete();
    return HttpResponseRedirect('/vendors')