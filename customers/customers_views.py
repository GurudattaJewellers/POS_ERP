from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import customers
from sales.models import sales
from sales import sales_views
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.db.models import F, Q, ExpressionWrapper, DecimalField
import re

def home(request):
    #all_customers = customers.objects.all().order_by('-cus_added_date')
    return render(request,"home.html")

'''def customers_data(request):
    all_customers = customers.objects.all().order_by('-cus_added_date')
    data = list(all_customers.values())
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
    #return render(request,"customers.html",{'customers':all_customers}) 
    '''
def customers_home(request):
    all_customers = customers.objects.all().order_by('-cus_added_date')
    filtered_customers = all_customers.exclude(Q(cus_deleted = True))
    return render(request,"customers.html",{'customers':filtered_customers})

def customers_deleted(request):
    all_customers = customers.objects.all().order_by('-cus_added_date')
    filtered_customers = all_customers.exclude(Q(cus_deleted = False))
    return render(request,"deleted_customers.html",{'customers':filtered_customers})

def new_customer(request):
    if request.method =="POST":
        if request.POST.get('customer_name')\
            and request.POST.get('customer_address')\
            and request.POST.get('customer_address2') \
            and request.POST.get('cus_state') \
            and request.POST.get('cus_state_code') \
            and request.POST.get('cus_mobile_no') \
            and request.POST.get('cus_kyc'):
            # and request.POST.get('cus_emailid') \
            # and request.POST.get('cus_gstin') \
            # and request.POST.get('cus_pan_no') \
            # and request.POST.get('cus_aadhar_no') \
            #and request.POST.get('cus_mobile_no2') \
            cust = customers()
            cust.customer_name = request.POST.get('customer_name')
            cust.customer_name = cust.customer_name.strip()
            cust.customer_address = request.POST.get('customer_address')
            cust.customer_address = cust.customer_address.strip()
            cust.customer_address2 = request.POST.get('customer_address2')
            cust.customer_address2 = cust.customer_address2.strip()
            cust.cus_emailid = request.POST.get('cus_emailid')
            cust.cus_emailid = cust.cus_emailid.strip()
            cust.cus_gstin = request.POST.get('cus_gstin')
            cust.cus_gstin = cust.cus_gstin.strip()
            cust.cus_state = request.POST.get('cus_state')
            cust.cus_state = cust.cus_state.strip()
            cust.cus_state_code = request.POST.get('cus_state_code')
            cust.cus_state_code = cust.cus_state_code.strip()
            cust.cus_mobile_no = request.POST.get('cus_mobile_no')
            cust.cus_mobile_no = cust.cus_mobile_no.strip()
            cust.cus_mobile_no2 = request.POST.get('cus_mobile_no2')
            cust.cus_mobile_no2 = cust.cus_mobile_no2.strip()
            cust.cus_pan_no = request.POST.get('cus_pan_no')
            cust.cus_pan_no = cust.cus_pan_no.strip()
            cust.cus_aadhar_no = request.POST.get('cus_aadhar_no')
            cust.cus_aadhar_no = cust.cus_aadhar_no.strip()
            cust.cus_kyc = request.POST.get('cus_kyc')
            cust.cus_kyc = cust.cus_kyc.strip()
            cust.save()
            return HttpResponseRedirect('/customers')
    else:
        return render(request,'new_customer.html')

def customer(request, customer_id):
    cust = customers.objects.get(customer_id=customer_id)
    #sales_of_cust = sales.objects.all().order_by('-sale_date')#
    sales_of_cust = sales.objects.all().filter(customer_id = customer_id.strip()).filter(sale_deleted=False).order_by('-sale_date')
    '''sales.objects.all().filter(customer_id=customer_id.strip()) \
        .order_by('-sale_date') \
        .annotate(cus_id_no = ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField()))
    for sale in sales_of_cust:
        customer_id_number = re.search(r'\d+', str(sale.customer_id))
        sale.customer_id = customer_id_number.group(0)'''
    return render(request, "view_customer.html", {'customer': cust, 'sales': sales_of_cust})

def edit_customer(request, customer_id):
    if request.method =="POST":
        if request.POST.get('customer_name') \
            and request.POST.get('customer_address') \
            and request.POST.get('customer_address2') \
            and request.POST.get('cus_state') \
            and request.POST.get('cus_state_code') \
            and request.POST.get('cus_mobile_no') \
            and request.POST.get('cus_kyc'):
            # and request.POST.get('cus_emailid') \
            # and request.POST.get('cus_gstin') \
            # and request.POST.get('cus_pan_no') \
            # and request.POST.get('cus_aadhar_no') \
            # and request.POST.get('cus_mobile_no2') \
            cust = customers()
            cust.customer_name = request.POST.get('customer_name')
            cust.customer_name = cust.customer_name.strip()
            cust.customer_address = request.POST.get('customer_address')
            cust.customer_address = cust.customer_address.strip()
            cust.customer_address2 = request.POST.get('customer_address2')
            cust.customer_address2 = cust.customer_address2.strip()
            if request.POST.get('cus_emailid'):
                cust.cus_emailid = request.POST.get('cus_emailid')
                cust.cus_emailid = cust.cus_emailid.strip()

            if request.POST.get('cus_gstin'):
                cust.cus_gstin = request.POST.get('cus_gstin')
                cust.cus_gstin = cust.cus_gstin.strip()

            if request.POST.get('cus_mobile_no2'):
                cust.cus_mobile_no2 = request.POST.get('cus_mobile_no2')
                cust.cus_mobile_no2 = cust.cus_mobile_no2.strip()
            cust.cus_state = request.POST.get('cus_state')
            cust.cus_state = cust.cus_state.strip()
            cust.cus_state_code = request.POST.get('cus_state_code')
            cust.cus_state_code = cust.cus_state_code.strip()
            cust.cus_mobile_no = request.POST.get('cus_mobile_no')
            cust.cus_mobile_no = cust.cus_mobile_no.strip()

            if request.POST.get('cus_pan_no'):
                cust.cus_pan_no = request.POST.get('cus_pan_no')
                cust.cus_pan_no = cust.cus_pan_no.strip()
            if request.POST.get('cus_aadhar_no'):
                cust.cus_aadhar_no = request.POST.get('cus_aadhar_no')
                cust.cus_aadhar_no = cust.cus_aadhar_no.strip()

            cust.cus_kyc = request.POST.get('cus_kyc')
            cust.cus_kyc = cust.cus_kyc.strip()
            #cust.cus_added_date = datetime.now().strftime('%B %d, %Y, %I:%M %p')
            #date_obj = datetime.strptime(cust.cus_added_date, '%B %d, %Y, %I:%M %p')
            #cust.cus_added_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            customers.objects.filter(customer_id = customer_id).update(customer_name = cust.customer_name, customer_address = cust.customer_address2,
                                                            customer_address2 = cust.customer_address2, cus_emailid = cust.cus_emailid,
                                                            cus_state = cust.cus_state, cus_state_code = cust.cus_state_code,
                                                            cus_mobile_no = cust.cus_mobile_no, cus_mobile_no2 = cust.cus_mobile_no2,
                                                            cus_gstin = cust.cus_gstin, cus_pan_no = cust.cus_pan_no,
                                                            cus_aadhar_no = cust.cus_aadhar_no, cus_kyc = cust.cus_kyc )
            return HttpResponseRedirect('/customers')
    else:
        cust = customers.objects.get(customer_id = customer_id)
        return render(request, "edit_customer.html", {'customer': cust})
        #cust = customers.objects.get(customer_id = request.POST.get('customer_id'))
        #if cust != None:
        #return HttpResponseRedirect('/')

def delete_customer(request, customer_id):
    #cust = customers.objects.get(customer_id = customer_id)
    customers.objects.filter(customer_id = customer_id).update(cus_deleted = True)
    return HttpResponseRedirect('/customers')

def add_customer_back(request, customer_id):
    customers.objects.filter(customer_id=customer_id).update(cus_deleted=False)
    return HttpResponseRedirect('/customers')

def delete_customer_complete(request, customer_id):
    cust = customers.objects.get(customer_id=customer_id)
    cust.delete();
    return HttpResponseRedirect('/customers')