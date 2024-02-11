from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseBadRequest
from purchases.models import purchases, purchases2
from vendors.models import vendors
from fpdf import FPDF
from customers.models import customers
from boxes.models import boxes, boxes_sale_history
from django.shortcuts import render, redirect
from django.db.models import F, Q, CharField, ExpressionWrapper
from datetime import datetime
import re
# Create your views here.

def purchases_home(request):
    all_purchases = purchases.objects.all().order_by('-inv_date')
    filtered_purchases = all_purchases.exclude(Q(purchase_deleted = True))
    return render(request,"purchases.html",{'purchases':filtered_purchases})

def purchases_home_two(request):
    all_purchases = purchases2.objects.all().order_by('-inv_date')
    filtered_purchases = all_purchases.exclude(Q(purchase_deleted = True))
    return render(request,"purchases_two.html",{'purchases':filtered_purchases})

def new_purchase(request, vendor_id):
    if request.method == "POST" and request.POST.get('item_purchase_12') == '1':
        purchase = purchases()
        purchase.bill_no = request.POST.get('bill_no')
        purchase.inv_date = datetime.strptime(request.POST.get('inv_date'), '%Y-%m-%d')
        purchase.metal = request.POST.get('metal')
        purchase.description = request.POST.get('description')
        purchase.Purity = request.POST.get('purity')
        purchase.HSN_SAC_Code = request.POST.get('hsn_sac')
        purchase.item_purchase_12 = request.POST.get('item_purchase_12')
        purchase.less_weight = '{:.3f}'.format(float(request.POST.get('less_weight')))
        purchase.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
        purchase.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
        purchase.rate = '{:.2f}'.format(float(request.POST.get('rate')))
        purchase.gst = '{:.2f}'.format(float(request.POST.get('gst')))
        purchase.tcs = '{:.2f}'.format(float(request.POST.get('tcs')))
        purchase.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount')))
        purchase.rounded_off = '{:.2f}'.format(float(request.POST.get('rounded_off')))
        purchase.total = '{:.2f}'.format(float(request.POST.get('total')))
        purchase.declaration = request.POST.get('declaration')
        purchase.delivery_mode = request.POST.get('delivery_mode')
        purchase.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
        purchase.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
        box = boxes.objects.get(box_id = request.POST.get('box_id'))
        purchase.box_id = box
        vendor = vendors.objects.get(vendor_id=request.POST.get('vendor_id'))
        purchase.vendor_id = vendor
        purchase.save()

        '''purchase_id = purchase.purchase_id

        box = Box.objects.get(box_id=request.POST.get('box_id'))
        updated_weight = (float(box.box_total_weight) + float(request.POST.get('net_weight')))
        Box.objects.filter(box_id=request.POST.get('box_id')).update(box_total_weight='{:.2f}'.format(updated_weight))

        box_purchase = BoxPurchaseHistory()
        box_purchase.box_name = box.box_name
        box_purchase.item_name = request.POST.get('description')
        box_purchase.item_weight = '{:.2f}'.format(float(request.POST.get('net_weight')))
        box_purchase.item_sale_12 = request.POST.get('purchase_1_2')
        box_purchase.purchase_id = purchase_id
        box_purchase.box_id = box
        box_purchase.box_updated_date = purchase.inv_date
        box_purchase.save()'''

        return HttpResponseRedirect('/vendor/' + str(vendor.vendor_id))
    elif request.method == "POST" and request.POST.get('item_purchase_12') == '2':
        purchase = purchases2()
        purchase.bill_no = request.POST.get('bill_no')
        purchase.inv_date = datetime.strptime(request.POST.get('inv_date'), '%Y-%m-%d')
        purchase.metal = request.POST.get('metal')
        purchase.description = request.POST.get('description')
        purchase.Purity = request.POST.get('purity')
        purchase.HSN_SAC_Code = request.POST.get('hsn_sac')
        purchase.item_purchase_12 = request.POST.get('item_purchase_12')
        purchase.less_weight = '{:.3f}'.format(float(request.POST.get('less_weight')))
        purchase.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
        purchase.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
        purchase.rate = '{:.2f}'.format(float(request.POST.get('rate')))
        purchase.gst = '{:.2f}'.format(float(request.POST.get('gst')))
        purchase.tcs = '{:.2f}'.format(float(request.POST.get('tcs')))
        purchase.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount')))
        purchase.rounded_off = '{:.2f}'.format(float(request.POST.get('rounded_off')))
        purchase.total = '{:.2f}'.format(float(request.POST.get('total')))
        purchase.declaration = request.POST.get('declaration')
        purchase.delivery_mode = request.POST.get('delivery_mode')
        purchase.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
        purchase.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
        box = boxes.objects.get(box_id = request.POST.get('box_id'))
        purchase.box_id = box
        vendor = vendors.objects.get(vendor_id=request.POST.get('vendor_id'))
        purchase.vendor_id = vendor
        purchase.save()
        return HttpResponseRedirect('/vendor/' + str(vendor.vendor_id))
    else:
        vend = vendors.objects.get(vendor_id=vendor_id)
        all_boxes = boxes.objects.all().order_by('-box_added_date')
        filtered_boxes = all_boxes.exclude(Q(box_deleted=True))
        return render(request, "new_purchase.html", {'vendor': vend, 'boxes': filtered_boxes})

def edit_purchase(request, purchase_id, item_purchase_12):
    if request.method == "POST" and item_purchase_12 == '1':
        purchases_object = purchases.objects.filter(purchase_id=purchase_id).first()
        if purchases_object is not None:
            pur = purchases()
            pur.bill_no = request.POST.get('bill_no')
            pur.inv_date = datetime.strptime(request.POST.get('inv_date'), '%Y-%m-%d')
            pur.metal = request.POST.get('metal')
            pur.description = request.POST.get('description')
            pur.Purity = request.POST.get('purity')
            pur.HSN_SAC_Code = request.POST.get('hsn_sac')
            pur.item_purchase_12 = request.POST.get('item_purchase_12')
            pur.less_weight = '{:.3f}'.format(float(request.POST.get('less_weight')))
            pur.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            pur.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            pur.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            pur.gst = '{:.2f}'.format(float(request.POST.get('gst')))
            pur.tcs = '{:.2f}'.format(float(request.POST.get('tcs')))
            pur.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount')))
            pur.rounded_off = '{:.2f}'.format(float(request.POST.get('rounded_off')))
            pur.total = '{:.2f}'.format(float(request.POST.get('total')))
            pur.declaration = request.POST.get('declaration')
            pur.delivery_mode = request.POST.get('delivery_mode')
            pur.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            pur.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            box = boxes.objects.get(box_id = request.POST.get('box_id'))
            pur.box_id = box
            vendor = vendors.objects.get(vendor_id=request.POST.get('vendor_id'))
            pur.vendor_id = vendor
            purchases.objects.filter(purchase_id=purchase_id).update(bill_no = pur.bill_no, inv_date = pur.inv_date, metal = pur.metal,
                                                                     description = pur.description, Purity = pur.Purity, HSN_SAC_Code = pur.HSN_SAC_Code,
                                                                     item_purchase_12 = pur.item_purchase_12, less_weight=pur.less_weight, gross_weight = pur.gross_weight,
                                                                     net_weight = pur.net_weight, rate = pur.rate, gst = pur.gst, tcs =pur.tcs,
                                                                     total_amount = pur.total_amount, rounded_off = pur.rounded_off, total = pur.total,
                                                                     declaration = pur.declaration, delivery_mode = pur.delivery_mode, settled_amount = pur.settled_amount,
                                                                     unsettled_amount = pur.unsettled_amount, box_id = pur.box_id, vendor_id = pur.vendor_id)
        else:
            purchases2.objects.filter(purchase_id=purchase_id).update(purchase_deleted=True)
            purchase = purchases()
            purchase.bill_no = request.POST.get('bill_no')
            purchase.inv_date = datetime.strptime(request.POST.get('inv_date'), '%Y-%m-%d')
            purchase.metal = request.POST.get('metal')
            purchase.description = request.POST.get('description')
            purchase.Purity = request.POST.get('purity')
            purchase.HSN_SAC_Code = request.POST.get('hsn_sac')
            purchase.item_purchase_12 = request.POST.get('item_purchase_12')
            purchase.less_weight = '{:.3f}'.format(float(request.POST.get('less_weight')))
            purchase.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            purchase.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            purchase.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            purchase.gst = '{:.2f}'.format(float(request.POST.get('gst')))
            purchase.tcs = '{:.2f}'.format(float(request.POST.get('tcs')))
            purchase.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount')))
            purchase.rounded_off = '{:.2f}'.format(float(request.POST.get('rounded_off')))
            purchase.total = '{:.2f}'.format(float(request.POST.get('total')))
            purchase.declaration = request.POST.get('declaration')
            purchase.delivery_mode = request.POST.get('delivery_mode')
            purchase.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            purchase.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            purchase.box_id = box
            vendor = vendors.objects.get(vendor_id=request.POST.get('vendor_id'))
            purchase.vendor_id = vendor
            purchase.save()


    elif request.method == "POST" and item_purchase_12 == '2':
        purchases_object = purchases2.objects.filter(purchase_id=purchase_id).first()
        if purchases_object is not None:
            pur = purchases2()
            pur.bill_no = request.POST.get('bill_no')
            pur.inv_date = datetime.strptime(request.POST.get('inv_date'), '%Y-%m-%d')
            pur.metal = request.POST.get('metal')
            pur.description = request.POST.get('description')
            pur.Purity = request.POST.get('purity')
            pur.HSN_SAC_Code = request.POST.get('hsn_sac')
            pur.item_purchase_12 = request.POST.get('item_purchase_12')
            pur.less_weight = '{:.3f}'.format(float(request.POST.get('less_weight')))
            pur.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            pur.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            pur.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            pur.gst = '{:.2f}'.format(float(request.POST.get('gst')))
            pur.tcs = '{:.2f}'.format(float(request.POST.get('tcs')))
            pur.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount')))
            pur.rounded_off = '{:.2f}'.format(float(request.POST.get('rounded_off')))
            pur.total = '{:.2f}'.format(float(request.POST.get('total')))
            pur.declaration = request.POST.get('declaration')
            pur.delivery_mode = request.POST.get('delivery_mode')
            pur.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            pur.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            box = boxes.objects.get(box_id = request.POST.get('box_id'))
            pur.box_id = box
            vendor = vendors.objects.get(vendor_id=request.POST.get('vendor_id'))
            pur.vendor_id = vendor
            purchases.objects.filter(purchase_id=purchase_id).update(bill_no = pur.bill_no, inv_date = pur.inv_date, metal = pur.metal,
                                                                     description = pur.description, Purity = pur.Purity, HSN_SAC_Code = pur.HSN_SAC_Code,
                                                                     item_purchase_12 = pur.item_purchase_12, less_weight=pur.less_weight, gross_weight = pur.gross_weight,
                                                                     net_weight = pur.net_weight, rate = pur.rate, gst = pur.gst, tcs =pur.tcs,
                                                                     total_amount = pur.total_amount, rounded_off = pur.rounded_off, total = pur.total,
                                                                     declaration = pur.declaration, delivery_mode = pur.delivery_mode, settled_amount = pur.settled_amount,
                                                                     unsettled_amount = pur.unsettled_amount, box_id = pur.box_id, vendor_id = pur.vendor_id)
        else:
            purchases.objects.filter(purchase_id=purchase_id).update(purchase_deleted=True)
            purchase = purchases2()
            purchase.bill_no = request.POST.get('bill_no')
            purchase.inv_date = datetime.strptime(request.POST.get('inv_date'), '%Y-%m-%d')
            purchase.metal = request.POST.get('metal')
            purchase.description = request.POST.get('description')
            purchase.Purity = request.POST.get('purity')
            purchase.HSN_SAC_Code = request.POST.get('hsn_sac')
            purchase.item_purchase_12 = request.POST.get('item_purchase_12')
            purchase.less_weight = '{:.3f}'.format(float(request.POST.get('less_weight')))
            purchase.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            purchase.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            purchase.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            purchase.gst = '{:.2f}'.format(float(request.POST.get('gst')))
            purchase.tcs = '{:.2f}'.format(float(request.POST.get('tcs')))
            purchase.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount')))
            purchase.rounded_off = '{:.2f}'.format(float(request.POST.get('rounded_off')))
            purchase.total = '{:.2f}'.format(float(request.POST.get('total')))
            purchase.declaration = request.POST.get('declaration')
            purchase.delivery_mode = request.POST.get('delivery_mode')
            purchase.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            purchase.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            purchase.box_id = box
            vendor = vendors.objects.get(vendor_id=request.POST.get('vendor_id'))
            purchase.vendor_id = vendor
            purchase.save()
    else:
        if item_purchase_12 == '1':
            purchase = purchases.objects.get(purchase_id=purchase_id)
            result = re.search(r'\d+', str(purchase.box_id))
            box = boxes.objects.get(box_id = result.group(0))
            all_boxes = boxes.objects.all().order_by('-box_added_date')
            filtered_boxes = all_boxes.exclude(Q(box_deleted=True))
            result = re.search(r'\d+', str(purchase.vendor_id))
            vend = vendors.objects.get(vendor_id=result.group(0))
            return render(request, "edit_purchase.html", {'purchase': purchase, 'vendor': vend, 'boxes': filtered_boxes, 'box':box})
        else:
            purchase = purchases2.objects.get(purchase_id=purchase_id)
            result = re.search(r'\d+', str(purchase.box_id))
            box = boxes.objects.get(box_id=result.group(0))
            all_boxes = boxes.objects.all().order_by('-box_added_date')
            filtered_boxes = all_boxes.exclude(Q(box_deleted=True))
            result = re.search(r'\d+', str(purchase.vendor_id))
            vend = vendors.objects.get(vendor_id=result.group(0))
            return render(request, "edit_purchase.html",
                          {'purchase': purchase, 'vendor': vend, 'boxes': filtered_boxes, 'box': box})

def delete_purchase(request, purchase_id):
    purchases.objects.filter(purchase_id=purchase_id).update(purchase_deleted=True)
    return HttpResponseRedirect('/purchases')

def delete_purchase_two(request, purchase_id):
    purchases2.objects.filter(purchase_id=purchase_id).update(purchase_deleted=True)
    return HttpResponseRedirect('/purchases2')
