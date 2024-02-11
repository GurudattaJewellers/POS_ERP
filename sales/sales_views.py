from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseBadRequest
from sales.models import sales, sales2
from fpdf import FPDF
from.utils import render_to_pdf
from customers.models import customers
from boxes.models import boxes, boxes_sale_history
from django.shortcuts import render, redirect
from django.db.models import F, Q, CharField, ExpressionWrapper
from num2words import num2words
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

def sales_home(request):
    all_sales = sales.objects.all().order_by('-sale_date')
    filtered_sales = all_sales.exclude(Q(sale_deleted = True))
    '''all_sales = sales.objects.all().order_by('-sale_date') \
        .annotate(cus_id_no=ExpressionWrapper(
        (re.search(r'\d+', F('customer_id__id')).group(0) if re.search(r'\d+', F('customer_id__id')) else ''),
        output_field=CharField()
    ))'''
    return render(request,"sales.html",{'sales':filtered_sales})

def sales_home_two(request):
    all_sales = sales2.objects.all().order_by('-sale_date')
    filtered_sales = all_sales.exclude(Q(sale_deleted = True))
    return render(request,"sales_two.html",{'sales':filtered_sales})

'''def generate_invoice_pdf(request, customer_id):
    #invoice = Invoice.objects.get(pk=invoice_id)
    pdf = Invoice(request, customer_id)
    print(pdf)
    response = HttpResponse(pdf.generate_pdf(), content_type='application/pdf')
    response['Content-Disposition'] = f'filename="Invoice.pdf"' #{invoice.invoice_no}
    return response'''
def generate_invoice_pdf(request, invoice_no):
    template_name = "sale_pdf.html"
    sale = sales.objects.get(invoice_no=invoice_no)
    result = re.search(r'\d+', str(sale.customer_id))
    cust = customers.objects.get(customer_id=result.group(0))
    rounded_x = round(sale.amount_after_gst ,2)
    amount_in_words ='Indian Rupees - ' + num2words(round(sale.amount_after_gst)) + " rupees only"
    round_off = "{:.2f}".format(round((rounded_x - int(rounded_x)), 2))

    sale_date = sale.sale_date.strftime('%d/%m/%Y')

    return render_to_pdf(
        template_name,
        {
            "customer": cust,
            "sale":sale,
            "amount_in_words":amount_in_words,
            "sale_date":sale_date,
            "round_off":round_off,
            "total_payable" :round(sale.amount_after_gst)
        },
    )

def new_sale(request, customer_id):
    if request.method =="POST"\
            and request.POST.get('sale_1_2') == '1':
        print(request.POST)
        sale = sales()
        sale.metal = request.POST.get('metal')
        sale.HSN_SAC_Code = request.POST.get('hsn_sac')
        # sales.Purity = request.POST.get('Purity')
        if request.POST.get('purity_gold'):
            sale.Purity = request.POST.get('purity_gold')
        elif request.POST.get('purity_silver'):
            sale.Purity = request.POST.get('purity_silver')
        sale.ornament_type = request.POST.get('ornament')

        sale.item_sale_type = request.POST.get('sale_type')
        sale.item_sale_12 = request.POST.get('sale_1_2')

        sale.HUID = request.POST.get('HUID')

        sale.weight_with_tag = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
        sale.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
        sale.stone_weight = '{:.3f}'.format(float(request.POST.get('stone_weight')))
        sale.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
        sale.value_added = '{:.3f}'.format(float(request.POST.get('value_added')))
        sale.making_charge = '{:.2f}'.format(float(request.POST.get('making_charge')))
        sale.rate = '{:.2f}'.format(float(request.POST.get('rate')))
        sale.stone_cost = '{:.2f}'.format(float(request.POST.get('stone_cost')))
        sale.amount_before_gst = '{:.2f}'.format(float(request.POST.get('amount_before_gst')))
        sale.cgst = '{:.2f}'.format(float(request.POST.get('cgst_p')))
        sale.sgst = '{:.2f}'.format(float(request.POST.get('sgst_p')))
        sale.amount_after_gst = '{:.2f}'.format(float(request.POST.get('new_sale_total_p')))
        sale.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount_p')))
        customer = customers.objects.get(customer_id = customer_id)
        sale.customer_id = customer
        box = boxes.objects.get(box_id = request.POST.get('box_id'))
        sale.box_id= box
        sale.old_metal_type = request.POST.get('oldmetal')
        sale.old_items_type = request.POST.get('olditemstype')
        sale.old_items_weight = '{:.3f}'.format(float(request.POST.get('old_items_weight')))
        sale.old_items_rate = '{:.2f}'.format(float(request.POST.get('old_items_rate')))
        sale.old_items_dust = '{:.3f}'.format(float(request.POST.get('old_items_dust')))
        sale.old_items_touch = '{:.2f}'.format(float(request.POST.get('old_items_touch')))
        sale.old_items_totalvalue = '{:.2f}'.format(float(request.POST.get('old_quote_p')))
        sale.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
        sale.discount = '{:.2f}'.format(float(request.POST.get('discount')))
        sale.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
        sale.declaration = request.POST.get('declaration')
        sale.cal_mode = request.POST.get('net_gross_p')
        sale.bycash = '{:.2f}'.format(float(request.POST.get('bycash')))
        sale.bycard = '{:.2f}'.format(float(request.POST.get('bycard')))
        sale.byupi = '{:.2f}'.format(float(request.POST.get('byupi')))
        sale.byib = '{:.2f}'.format(float(request.POST.get('byib')))
        sale.save()

        sale_id= sale.invoice_no

        box = boxes.objects.get(box_id=request.POST.get('box_id'))
        updated_weight = (float(box.box_total_weight) - float(request.POST.get('weight_with_tag')))
        boxes.objects.filter(box_id=request.POST.get('box_id')).update(box_total_weight = '{:.3f}'.format(updated_weight))

        box_sale = boxes_sale_history()
        box_sale.box_name = box.box_name

        box_sale.item_name = request.POST.get('ornament')
        box_sale.item_weight = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
        box_sale.item_sale_type = request.POST.get('sale_type')
        box_sale.item_sale_12 = request.POST.get('sale_1_2')
        box_sale.sale_id = sale_id
        box_sale.box_id = box
        box_sale.box_updated_date = sale.sale_date
        box_sale.save()

        return HttpResponseRedirect('/customer/' + customer_id)
        #return render(request, 'customers.html', {'redirect_url': f'/customer/{customer_id}/', 'pdf_response': generate_invoice_pdf(request, customer_id)})
        #return redirect('/customer/' + customer_id, response=generate_invoice_pdf(request, customer_id))

    elif request.method =="POST"\
            and request.POST.get('sale_1_2') == '2':
        print(request.POST)
        sale = sales2()
        sale.metal = request.POST.get('metal')
        sale.HSN_SAC_Code = request.POST.get('hsn_sac')
        # sales.Purity = request.POST.get('Purity')
        if request.POST.get('purity_gold'):
            sale.Purity = request.POST.get('purity_gold')
        elif request.POST.get('purity_silver'):
            sale.Purity = request.POST.get('purity_silver')
        sale.ornament_type = request.POST.get('ornament')

        sale.item_sale_type = request.POST.get('sale_type')
        sale.item_sale_12 = request.POST.get('sale_1_2')

        sale.HUID = request.POST.get('HUID')

        sale.weight_with_tag = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
        sale.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
        sale.stone_weight = '{:.3f}'.format(float(request.POST.get('stone_weight')))
        sale.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
        sale.value_added = '{:.3f}'.format(float(request.POST.get('value_added')))
        sale.making_charge = '{:.2f}'.format(float(request.POST.get('making_charge')))
        sale.rate = '{:.2f}'.format(float(request.POST.get('rate')))
        sale.stone_cost = '{:.2f}'.format(float(request.POST.get('stone_cost')))
        sale.amount_before_gst = '{:.2f}'.format(float(request.POST.get('amount_before_gst')))
        sale.cgst = '{:.2f}'.format(float(request.POST.get('cgst_p')))
        sale.sgst = '{:.2f}'.format(float(request.POST.get('sgst_p')))
        sale.amount_after_gst = '{:.2f}'.format(float(request.POST.get('new_sale_total_p')))
        sale.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount_p')))
        customer = customers.objects.get(customer_id=customer_id)
        sale.customer_id = customer
        box = boxes.objects.get(box_id=request.POST.get('box_id'))
        sale.box_id = box
        sale.old_metal_type = request.POST.get('oldmetal')
        sale.old_items_type = request.POST.get('olditemstype')
        sale.old_items_weight = '{:.3f}'.format(float(request.POST.get('old_items_weight')))
        sale.old_items_rate = '{:.2f}'.format(float(request.POST.get('old_items_rate')))
        sale.old_items_dust = '{:.3f}'.format(float(request.POST.get('old_items_dust')))
        sale.old_items_touch = '{:.2f}'.format(float(request.POST.get('old_items_touch')))
        sale.old_items_totalvalue = '{:.2f}'.format(float(request.POST.get('old_quote_p')))
        sale.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
        sale.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
        sale.discount = '{:.2f}'.format(float(request.POST.get('discount')))
        sale.declaration = request.POST.get('declaration')
        sale.cal_mode = request.POST.get('net_gross_p')
        sale.bycash = '{:.2f}'.format(float(request.POST.get('bycash')))
        sale.bycard = '{:.2f}'.format(float(request.POST.get('bycard')))
        sale.byupi = '{:.2f}'.format(float(request.POST.get('byupi')))
        sale.byib = '{:.2f}'.format(float(request.POST.get('byib')))
        sale.save()

        sale_id = sale.invoice_no

        box = boxes.objects.get(box_id=request.POST.get('box_id'))
        updated_weight = (float(box.box_total_weight) - float(sale.weight_with_tag))
        boxes.objects.filter(box_id=request.POST.get('box_id')).update(box_total_weight='{:.3f}'.format(updated_weight))

        box_sale = boxes_sale_history()
        box_sale.box_name = box.box_name

        box_sale.item_name = request.POST.get('ornament')
        box_sale.item_weight = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
        box_sale.item_sale_type = request.POST.get('sale_type')
        box_sale.item_sale_12 = request.POST.get('sale_1_2')
        box_sale.sale_id = sale_id
        box_sale.box_id = box
        box_sale.box_updated_date = sale.sale_date
        box_sale.save()

        return HttpResponseRedirect('/customer/' + customer_id)
    else:
        cust = customers.objects.get(customer_id=customer_id)
        all_boxes = boxes.objects.all().order_by('-box_added_date')
        filtered_boxes = all_boxes.exclude(Q(box_deleted=True))
        url = 'http://kjpl.in/'
        response = requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        gold_rate = soup.find('span', {'class': 'gold-rate'}).text.strip()
        silver_rate = soup.find('span', {'class': 'silver-rate'}).text.strip()
        return render(request, "new_sale.html", {'customer': cust, 'boxes': filtered_boxes, 'gold_rate':gold_rate, 'silver_rate':silver_rate})

def edit_sale(request, invoice_no, item_sale_12):
    if request.method == "POST"\
        and request.POST.get('sale_1_2') == '1':
        sales_object = sales.objects.filter(invoice_no = invoice_no).first()
        if sales_object is not None:
            box_sale_last = boxes_sale_history.objects.filter(sale_id=invoice_no).last()
            sale = sales()
            sale.metal = request.POST.get('metal')
            sale.HSN_SAC_Code = request.POST.get('hsn_sac')
            # sales.Purity = request.POST.get('Purity')
            if request.POST.get('purity_gold'):
                sale.Purity = request.POST.get('purity_gold')
            elif request.POST.get('purity_silver'):
                sale.Purity = request.POST.get('purity_silver')
            sale.ornament_type = request.POST.get('ornament')

            sale.item_sale_type = request.POST.get('sale_type')
            sale.item_sale_12 = request.POST.get('sale_1_2')

            sale.HUID = request.POST.get('HUID')
            sale.weight_with_tag = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
            sale.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            sale.stone_weight = '{:.3f}'.format(float(request.POST.get('stone_weight')))
            sale.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            sale.value_added = '{:.3f}'.format(float(request.POST.get('value_added')))
            sale.making_charge = '{:.2f}'.format(float(request.POST.get('making_charge')))
            sale.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            sale.stone_cost = '{:.2f}'.format(float(request.POST.get('stone_cost')))
            sale.amount_before_gst = '{:.2f}'.format(float(request.POST.get('amount_before_gst')))
            sale.cgst = '{:.2f}'.format(float(request.POST.get('cgst_p')))
            sale.sgst = '{:.2f}'.format(float(request.POST.get('sgst_p')))
            sale.amount_after_gst = '{:.2f}'.format(float(request.POST.get('new_sale_total_p')))
            sale.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount_p')))
            sale.old_metal_type = request.POST.get('oldmetal')
            sale.old_items_type = request.POST.get('olditemstype')
            sale.old_items_weight = '{:.3f}'.format(float(request.POST.get('old_items_weight')))
            sale.old_items_rate = '{:.2f}'.format(float(request.POST.get('old_items_rate')))
            sale.old_items_dust = '{:.3f}'.format(float(request.POST.get('old_items_dust')))
            sale.old_items_touch = '{:.2f}'.format(float(request.POST.get('old_items_touch')))
            sale.old_items_totalvalue = '{:.2f}'.format(float(request.POST.get('old_quote_p')))
            sale.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            sale.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            sale.discount = '{:.2f}'.format(float(request.POST.get('discount')))
            sale.declaration = request.POST.get('declaration')
            sale.cal_mode = request.POST.get('net_gross_p')
            sale.bycash = '{:.2f}'.format(float(request.POST.get('bycash')))
            sale.bycard = '{:.2f}'.format(float(request.POST.get('bycard')))
            sale.byupi = '{:.2f}'.format(float(request.POST.get('byupi')))
            sale.byib = '{:.2f}'.format(float(request.POST.get('byib')))
            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            sale.box_id = box
            sales.objects.filter(invoice_no = invoice_no).update(metal = sale.metal, HSN_SAC_Code = sale.HSN_SAC_Code, Purity = sale.Purity, HUID = sale.HUID, weight_with_tag = sale.weight_with_tag,
                                                               ornament_type = sale.ornament_type, item_sale_type = sale.item_sale_type, item_sale_12 = sale.item_sale_12,
                                                               gross_weight = sale.gross_weight, stone_weight = sale.stone_weight,
                                                               net_weight = sale.net_weight, value_added = sale.value_added, making_charge = sale.making_charge,
                                                               rate = sale.rate, stone_cost = sale.stone_cost, amount_before_gst = sale.amount_before_gst, amount_after_gst = sale.amount_after_gst,
                                                               cgst = sale.cgst, sgst = sale.sgst, total_amount = sale.total_amount,
                                                               old_metal_type = sale.old_metal_type, old_items_type = sale.old_items_type, old_items_weight = sale.old_items_weight,
                                                               old_items_rate = sale.old_items_rate, old_items_dust =sale.old_items_dust, old_items_touch = sale.old_items_touch,
                                                               old_items_totalvalue = sale.old_items_totalvalue, settled_amount = sale.settled_amount, unsettled_amount = sale.unsettled_amount, discount = sale.discount,
                                                               declaration = sale.declaration, cal_mode = sale.cal_mode,
                                                               bycash = sale.bycash, bycard = sale.bycard, byupi = sale.byupi, byib = sale.byib, box_id = box)

            if '{:.3f}'.format(box_sale_last.item_weight) != '{:.3f}'.format(sale.weight_with_tag) :

                box = boxes.objects.get(box_id=request.POST.get('box_id'))
                if box_sale_last.box_id == request.POST.get('box_id'):
                    updated_weight = (float(box.box_total_weight) + float(box_sale_last.item_weight))
                    updated_weight = (float(updated_weight) - float(sale.weight_with_tag))
                    boxes.objects.filter(
                        box_id=request.POST.get('box_id')).update(box_total_weight='{:.3f}'.format(updated_weight))
                else:
                    updated_weight = (float(box_sale_last.box_total_weight) + float(sale.weight_with_tag))
                    boxes.objects.filter(
                        box_id=box_sale_last.box_id).update(box_total_weight = '{:.3f}'.format(updated_weight))

                    updated_weight = (float(box.box_total_weight) - float(sale.weight_with_tag))
                    boxes.objects.filter(
                        box_id=request.POST.get('box_id')).update(box_total_weight='{:.3f}'.format(updated_weight))

                box_sale = boxes_sale_history()
                box_sale.box_name = box.box_name
                box_sale.item_name = request.POST.get('ornament')
                box_sale.item_weight = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
                box_sale.item_sale_type = request.POST.get('sale_type')
                box_sale.item_sale_12 = request.POST.get('sale_1_2')
                box_sale.sale_id = invoice_no
                box_sale.box_id = box
                box_sale.box_updated_date = sale.sale_date
                box_sale.save()

            return HttpResponseRedirect('/sales')
        else:
            sales2.objects.filter(invoice_no=invoice_no).update(sale_deleted=True)
            sale = sales()
            sale.metal = request.POST.get('metal')
            sale.HSN_SAC_Code = request.POST.get('hsn_sac')
            # sales.Purity = request.POST.get('Purity')
            if request.POST.get('purity_gold'):
                sale.Purity = request.POST.get('purity_gold')
            elif request.POST.get('purity_silver'):
                sale.Purity = request.POST.get('purity_silver')
            sale.ornament_type = request.POST.get('ornament')

            sale.item_sale_type = request.POST.get('sale_type')
            sale.item_sale_12 = request.POST.get('sale_1_2')

            sale.HUID = request.POST.get('HUID')
            sale.weight_with_tag = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
            sale.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            sale.stone_weight = '{:.3f}'.format(float(request.POST.get('stone_weight')))
            sale.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            sale.value_added = '{:.3f}'.format(float(request.POST.get('value_added')))
            sale.making_charge = '{:.2f}'.format(float(request.POST.get('making_charge')))
            sale.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            sale.stone_cost = '{:.2f}'.format(float(request.POST.get('stone_cost')))
            sale.amount_before_gst = '{:.2f}'.format(float(request.POST.get('amount_before_gst')))
            sale.cgst = '{:.2f}'.format(float(request.POST.get('cgst_p')))
            sale.sgst = '{:.2f}'.format(float(request.POST.get('sgst_p')))
            sale.amount_after_gst = '{:.2f}'.format(float(request.POST.get('new_sale_total_p')))
            sale.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount_p')))
            customer = customers.objects.get(customer_id=request.POST.get('customer_id'))
            sale.customer_id = customer
            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            sale.box_id = box
            sale.old_metal_type = request.POST.get('oldmetal')
            sale.old_items_type = request.POST.get('olditemstype')
            sale.old_items_weight = '{:.3f}'.format(float(request.POST.get('old_items_weight')))
            sale.old_items_rate = '{:.2f}'.format(float(request.POST.get('old_items_rate')))
            sale.old_items_dust = '{:.3f}'.format(float(request.POST.get('old_items_dust')))
            sale.old_items_touch = '{:.2f}'.format(float(request.POST.get('old_items_touch')))
            sale.old_items_totalvalue = '{:.2f}'.format(float(request.POST.get('old_quote_p')))
            sale.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            sale.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            sale.discount = '{:.2f}'.format(float(request.POST.get('discount')))
            sale.declaration = request.POST.get('declaration')
            sale.cal_mode = request.POST.get('net_gross_p')
            sale.bycash = '{:.2f}'.format(float(request.POST.get('bycash')))
            sale.bycard = '{:.2f}'.format(float(request.POST.get('bycard')))
            sale.byupi = '{:.2f}'.format(float(request.POST.get('byupi')))
            sale.byib = '{:.2f}'.format(float(request.POST.get('byib')))
            sale.save()

            sale_id = sale.invoice_no

            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            updated_weight = (float(box.box_total_weight) - float(sale.weight_with_tag))
            boxes.objects.filter(box_id=request.POST.get('box_id')).update(
                box_total_weight='{:.3f}'.format(updated_weight))

            box_sale = boxes_sale_history()
            box_sale.box_name = box.box_name

            box_sale.item_name = request.POST.get('ornament')
            box_sale.item_weight = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
            box_sale.item_sale_type = request.POST.get('sale_type')
            box_sale.item_sale_12 = request.POST.get('sale_1_2')
            box_sale.sale_id = sale_id
            box_sale.box_id = box
            box_sale.box_updated_date = sale.sale_date
            box_sale.save()

            return HttpResponseRedirect('/sales')

    elif request.method =="POST"\
            and request.POST.get('sale_1_2') == '2':
        sales_object = sales2.objects.filter(invoice_no=invoice_no).first()
        if sales_object is not None:
            sale = sales2()
            sale.metal = request.POST.get('metal')
            sale.HSN_SAC_Code = request.POST.get('hsn_sac')
            # sales.Purity = request.POST.get('Purity')
            if request.POST.get('purity_gold'):
                sale.Purity = request.POST.get('purity_gold')
            elif request.POST.get('purity_silver'):
                sale.Purity = request.POST.get('purity_silver')
            sale.ornament_type = request.POST.get('ornament')

            sale.item_sale_type = request.POST.get('sale_type')
            sale.item_sale_12 = request.POST.get('sale_1_2')

            sale.HUID = request.POST.get('HUID')
            sale.weight_with_tag = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
            sale.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            sale.stone_weight = '{:.3f}'.format(float(request.POST.get('stone_weight')))
            sale.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            sale.value_added = '{:.3f}'.format(float(request.POST.get('value_added')))
            sale.making_charge = '{:.2f}'.format(float(request.POST.get('making_charge')))
            sale.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            sale.stone_cost = '{:.2f}'.format(float(request.POST.get('stone_cost')))
            sale.amount_before_gst = '{:.2f}'.format(float(request.POST.get('amount_before_gst')))
            sale.cgst = '{:.2f}'.format(float(request.POST.get('cgst_p')))
            sale.sgst = '{:.2f}'.format(float(request.POST.get('sgst_p')))
            sale.amount_after_gst = '{:.2f}'.format(float(request.POST.get('new_sale_total_p')))
            sale.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount_p')))
            sale.old_metal_type = request.POST.get('oldmetal')
            sale.old_items_type = request.POST.get('olditemstype')
            sale.old_items_weight = '{:.3f}'.format(float(request.POST.get('old_items_weight')))
            sale.old_items_rate = '{:.2f}'.format(float(request.POST.get('old_items_rate')))
            sale.old_items_dust = '{:.3f}'.format(float(request.POST.get('old_items_dust')))
            sale.old_items_touch = '{:.2f}'.format(float(request.POST.get('old_items_touch')))
            sale.old_items_totalvalue = '{:.2f}'.format(float(request.POST.get('old_quote_p')))
            sale.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            sale.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            sale.discount = '{:.2f}'.format(float(request.POST.get('discount')))
            sale.declaration = request.POST.get('declaration')
            sale.cal_mode = request.POST.get('net_gross_p')
            sale.bycash = '{:.2f}'.format(float(request.POST.get('bycash')))
            sale.bycard = '{:.2f}'.format(float(request.POST.get('bycard')))
            sale.byupi = '{:.2f}'.format(float(request.POST.get('byupi')))
            sale.byib = '{:.2f}'.format(float(request.POST.get('byib')))
            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            sale.box_id = box
            sales2.objects.filter(invoice_no=invoice_no).update(metal=sale.metal, HSN_SAC_Code=sale.HSN_SAC_Code,
                                                               Purity=sale.Purity, HUID =sale.HUID, weight_with_tag = sale.weight_with_tag,
                                                               ornament_type=sale.ornament_type,
                                                               item_sale_type=sale.item_sale_type,
                                                               item_sale_12=sale.item_sale_12,
                                                               gross_weight=sale.gross_weight,
                                                               stone_weight=sale.stone_weight,
                                                               net_weight=sale.net_weight, value_added=sale.value_added,
                                                               making_charge=sale.making_charge,
                                                               rate=sale.rate, stone_cost=sale.stone_cost,
                                                               amount_before_gst=sale.amount_before_gst,
                                                               amount_after_gst=sale.amount_after_gst,
                                                               cgst=sale.cgst, sgst=sale.sgst,
                                                               total_amount=sale.total_amount,
                                                               old_metal_type=sale.old_metal_type,
                                                               old_items_type=sale.old_items_type,
                                                               old_items_weight=sale.old_items_weight,
                                                               old_items_rate=sale.old_items_rate,
                                                               old_items_dust=sale.old_items_dust,
                                                               old_items_touch=sale.old_items_touch,
                                                               old_items_totalvalue=sale.old_items_totalvalue,
                                                               settled_amount=sale.settled_amount,
                                                               unsettled_amount=sale.unsettled_amount, discount = sale.discount,
                                                               declaration=sale.declaration, cal_mode=sale.cal_mode,
                                                               bycash = sale.bycash, bycard = sale.bycard, byupi = sale.byupi, byib = sale.byib,
                                                               box_id = box)
            if '{:.3f}'.format(box_sale_last.item_weight) != '{:.3f}'.format(sale.weight_with_tag):
                box = boxes.objects.get(box_id=request.POST.get('box_id'))
                if box_sale_last.box_id == request.POST.get('box_id'):
                    updated_weight = (float(box.box_total_weight) + float(box_sale_last.item_weight))
                    updated_weight = (float(updated_weight) - float(sale.weight_with_tag))
                    boxes.objects.filter(
                        box_id=request.POST.get('box_id')).update(box_total_weight='{:.3f}'.format(updated_weight))
                else:
                    updated_weight = (float(box_sale_last.box_total_weight) + float(sale.weight_with_tag))
                    boxes.objects.filter(
                        box_id=box_sale_last.box_id).update(box_total_weight='{:.3f}'.format(updated_weight))

                    updated_weight = (float(box.box_total_weight) - float(sale.weight_with_tag))
                    boxes.objects.filter(
                        box_id=request.POST.get('box_id')).update(box_total_weight='{:.3f}'.format(updated_weight))

                box_sale = boxes_sale_history()
                box_sale.box_name = box.box_name
                box_sale.item_name = request.POST.get('ornament')
                box_sale.item_weight = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
                box_sale.item_sale_type = request.POST.get('sale_type')
                box_sale.item_sale_12 = request.POST.get('sale_1_2')
                box_sale.sale_id = invoice_no
                box_sale.box_id = box
                box_sale.box_updated_date = sale.sale_date
                box_sale.save()

            return HttpResponseRedirect('/sales2')
        else:
            sales.objects.filter(invoice_no=invoice_no).update(sale_deleted=True)
            sale = sales2()
            sale.metal = request.POST.get('metal')
            sale.HSN_SAC_Code = request.POST.get('hsn_sac')
            # sales.Purity = request.POST.get('Purity')
            if request.POST.get('purity_gold'):
                sale.Purity = request.POST.get('purity_gold')
            elif request.POST.get('purity_silver'):
                sale.Purity = request.POST.get('purity_silver')
            sale.ornament_type = request.POST.get('ornament')

            sale.item_sale_type = request.POST.get('sale_type')
            sale.item_sale_12 = request.POST.get('sale_1_2')

            sale.HUID = request.POST.get('HUID')
            sale.weight_with_tag = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
            sale.gross_weight = '{:.3f}'.format(float(request.POST.get('gross_weight')))
            sale.stone_weight = '{:.3f}'.format(float(request.POST.get('stone_weight')))
            sale.net_weight = '{:.3f}'.format(float(request.POST.get('net_weight')))
            sale.value_added = '{:.3f}'.format(float(request.POST.get('value_added')))
            sale.making_charge = '{:.2f}'.format(float(request.POST.get('making_charge')))
            sale.rate = '{:.2f}'.format(float(request.POST.get('rate')))
            sale.stone_cost = '{:.2f}'.format(float(request.POST.get('stone_cost')))
            sale.amount_before_gst = '{:.2f}'.format(float(request.POST.get('amount_before_gst')))
            sale.cgst = '{:.2f}'.format(float(request.POST.get('cgst_p')))
            sale.sgst = '{:.2f}'.format(float(request.POST.get('sgst_p')))
            sale.amount_after_gst = '{:.2f}'.format(float(request.POST.get('new_sale_total_p')))
            sale.total_amount = '{:.2f}'.format(float(request.POST.get('total_amount_p')))
            customer = customers.objects.get(customer_id=request.POST.get('customer_id'))
            sale.customer_id = customer
            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            sale.box_id = box
            sale.old_metal_type = request.POST.get('oldmetal')
            sale.old_items_type = request.POST.get('olditemstype')
            sale.old_items_weight = '{:.3f}'.format(float(request.POST.get('old_items_weight')))
            sale.old_items_rate = '{:.2f}'.format(float(request.POST.get('old_items_rate')))
            sale.old_items_dust = '{:.3f}'.format(float(request.POST.get('old_items_dust')))
            sale.old_items_touch = '{:.2f}'.format(float(request.POST.get('old_items_touch')))
            sale.old_items_totalvalue = '{:.2f}'.format(float(request.POST.get('old_quote_p')))
            sale.settled_amount = '{:.2f}'.format(float(request.POST.get('settled_amount')))
            sale.unsettled_amount = '{:.2f}'.format(float(request.POST.get('unsettled_amount')))
            sale.discount = '{:.2f}'.format(float(request.POST.get('discount')))
            sale.declaration = request.POST.get('declaration')
            sale.cal_mode = request.POST.get('net_gross_p')
            sale.bycash = '{:.2f}'.format(float(request.POST.get('bycash')))
            sale.bycard = '{:.2f}'.format(float(request.POST.get('bycard')))
            sale.byupi = '{:.2f}'.format(float(request.POST.get('byupi')))
            sale.byib = '{:.2f}'.format(float(request.POST.get('byib')))
            sale.save()

            sale_id = sale.invoice_no

            box = boxes.objects.get(box_id=request.POST.get('box_id'))
            updated_weight = (float(box.box_total_weight) - float(sale.weight_with_tag))
            boxes.objects.filter(box_id=request.POST.get('box_id')).update(
                box_total_weight='{:.3f}'.format(updated_weight))

            box_sale = boxes_sale_history()
            box_sale.box_name = box.box_name

            box_sale.item_name = request.POST.get('ornament')
            box_sale.item_weight = '{:.3f}'.format(float(request.POST.get('weight_with_tag')))
            box_sale.item_sale_type = request.POST.get('sale_type')
            box_sale.item_sale_12 = request.POST.get('sale_1_2')
            box_sale.sale_id = sale_id
            box_sale.box_id = box
            box_sale.box_updated_date = sale.sale_date
            box_sale.save()

            return HttpResponseRedirect('/sales2')

    else:
        if item_sale_12 == '1':
            sale = sales.objects.get(invoice_no=invoice_no)
            result = re.search(r'\d+', str(sale.box_id))
            box = boxes.objects.get(box_id = result.group(0))
            all_boxes = boxes.objects.all().order_by('-box_added_date')
            filtered_boxes = all_boxes.exclude(Q(box_deleted=True))
            result = re.search(r'\d+', str(sale.customer_id))
            cust = customers.objects.get(customer_id=result.group(0))
            return render(request, "edit_sale.html", {'sale': sale, 'customer': cust, 'boxes': filtered_boxes, 'box':box})
        else:
            sale = sales2.objects.get(invoice_no=invoice_no)
            result = re.search(r'\d+', str(sale.box_id))
            box = boxes.objects.get(box_id=result.group(0))
            all_boxes = boxes.objects.all().order_by('-box_added_date')
            filtered_boxes = all_boxes.exclude(Q(box_deleted=True))
            result = re.search(r'\d+', str(sale.customer_id))
            cust = customers.objects.get(customer_id=result.group(0))
            return render(request, "edit_sale.html", {'sale': sale, 'customer': cust, 'boxes': filtered_boxes, 'box':box})


def delete_sale(request, invoice_no):
    sales.objects.filter(invoice_no=invoice_no).update(sale_deleted=True)
    return HttpResponseRedirect('/sales')

def delete_sale_two(request, invoice_no):
    sales2.objects.filter(invoice_no=invoice_no).update(sale_deleted=True)
    return HttpResponseRedirect('/sales2')

