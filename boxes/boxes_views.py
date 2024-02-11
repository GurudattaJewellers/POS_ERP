from django.http import HttpResponseRedirect
from boxes.models import boxes, boxes_history, boxes_sale_history
from customers.models import customers
from django.shortcuts import render
from django.db.models import F, Q, CharField, ExpressionWrapper
from django.http import JsonResponse
import re
import json
from decimal import Decimal
from datetime import datetime
from django.utils import timezone


def get_box_sale_history(request, box_id):
    sale_history = boxes_sale_history.objects.filter(box_id=box_id).order_by('-box_updated_date')
    data = []
    for history in sale_history:
        box_dict = {
            'box_name': history.box_name,
            'item_name': history.item_name,
            'item_weight': float(Decimal(history.item_weight)),
            'item_sale_type': history.item_sale_type,
            'item_sale_12': history.item_sale_12,
            'sale_id': history.sale_id,
            'box_updated_date': history.box_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data.append(box_dict)
    return JsonResponse(data, safe=False)

def get_box_purchase_history(request, box_id):
    purchase_history = boxes_history.objects.filter(box_id=box_id).order_by('-box_updated_date')
    data = []
    for purchase in purchase_history:
        box_dict = {
            'box_name': purchase.box_name,
            'box_total_weight': float(Decimal(purchase.box_total_weight)),
            'box_added_weight': float(Decimal(purchase.box_added_weight)),
            'box_existed_weight': float(Decimal(purchase.box_existed_weight)),
            'item_purchase_12': purchase.item_purchase_12,
            'purchase_id': purchase.purchase_id,
            'box_updated_date': purchase.box_updated_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(box_dict)
    return JsonResponse(data, safe=False)

def boxes_home(request):
    all_boxes = boxes.objects.all().order_by('-box_added_date')
    filtered_boxes = all_boxes.exclude(Q(box_deleted=True)) #| Q(boolean_field=None))
    return render(request,"boxes.html",{'boxes':filtered_boxes})

def boxes_weights_home(request, box_id):
    box_history = boxes_history.objects.all().order_by('-box_updated_date')
    box_sale_history = boxes_sale_history.objects.all().order_by('-box_updated_date')
    return render(request,"boxes_history.html",{'boxes_history':box_history, 'boxes_sale_history':box_sale_history})

def new_box(request):
    if request.method =="POST":
        box = boxes()
        box.box_name = request.POST.get('box_name')
        box.box_total_weight = '{:.2f}'.format(float(request.POST.get('box_weight')))
        box.box_metal = request.POST.get('box_metal')
        box.save()
        return HttpResponseRedirect('/boxes')
    else:
        return HttpResponseRedirect('/boxes')

def edit_box(request, box_id):
    if request.method == "POST":
        box = boxes()
        box.box_name = request.POST.get('box_name')
        box.box_total_weight = '{:.2f}'.format(float(request.POST.get('total_weight')))
        box.box_metal = request.POST.get('box_metal')
        box.box_added_date = datetime.now().strftime('%B %d, %Y, %I:%M %p')
        date_obj = datetime.strptime(box.box_added_date, '%B %d, %Y, %I:%M %p')
        box.box_added_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        naive_datetime = datetime(2023, 3, 16, 23, 28, 0)
        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
        boxes.objects.filter(box_id = box_id).update(box_name = box.box_name, box_total_weight = box.box_total_weight,
                                                     box_metal = box.box_metal, box_added_date = aware_datetime)
        return HttpResponseRedirect('/boxes')
    else:
        box = boxes.objects.get(box_id = box_id)
        box_dict = {
            'box_id': box.box_id,
            'box_name': box.box_name,
            'box_metal': box.box_metal,
            'box_total_weight': float(Decimal(box.box_total_weight)),
            'box_added_date': box.box_added_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JsonResponse(json.dumps(box_dict), safe=False)

def delete_box(request, box_id):
    box = boxes.objects.get(box_id = box_id)
    box.update(box_deleted = True)
    return HttpResponseRedirect('/boxes')
