from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#from sales import views
from customers import customers_views
from sales import sales_views
from boxes import boxes_views
from vendors import vendors_views
from purchases import purchases_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', sales_views.sales_home,name='sales_home'),
    path('sales2/', sales_views.sales_home_two,name='sales_home_two'),
    path('new_sale/<customer_id>',sales_views.new_sale,name='new_sale'),
    path('invoice/<invoice_no>', sales_views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('edit_sale/<invoice_no>/<item_sale_12>',sales_views.edit_sale,name='edit_sale'),
    path('delete_sale/<invoice_no>',sales_views.delete_sale,name='delete_sale'),
    path('delete_sale2/<invoice_no>',sales_views.delete_sale_two,name='delete_sale_two'),
    path('', customers_views.home, name='home'),
    path('customers/', customers_views.customers_home, name='customers_home'),
    path('deleted_customers/',customers_views.customers_deleted, name='customers_deleted'),
    path('add_customer_back/<customer_id>',customers_views.add_customer_back, name='add_customer_back'),
    path('delete_customer_complete/<customer_id>',customers_views.delete_customer_complete, name = 'delete_customer_complete'),
    path('new_customer', customers_views.new_customer, name='new_customer'),
    path('customer/<customer_id>', customers_views.customer, name='customer'),
    path('edit_customer/<customer_id>', customers_views.edit_customer, name='edit_customer'),
    path('delete_customer/<customer_id>', customers_views.delete_customer, name='delete_customer'),
    path('boxes/', boxes_views.boxes_home,name='boxes_home'),
    path('get_box_sale_history/<box_id>', boxes_views.get_box_sale_history, name='get_box_sale_history'),
    path('get_box_purchase_history/<box_id>', boxes_views.get_box_purchase_history, name='get_box_purchase_history'),
    path('new_box', boxes_views.new_box, name='new_box'),
    path('box/<box_id>', boxes_views.boxes_weights_home, name='boxes_weights_home'),
    path('edit_box/<box_id>', boxes_views.edit_box, name='edit_box'),
    path('delete_box/<box_id>', boxes_views.delete_box, name='delete_box'),

    path('vendors/', vendors_views.vendors_home, name='vendors_home'),
    path('deleted_vendors/',vendors_views.vendors_deleted, name='vendors_deleted'),
    path('add_vendor_back/<vendor_id>',vendors_views.add_vendor_back, name='add_vendor_back'),
    path('delete_vendor_complete/<vendor_id>',vendors_views.delete_vendor_complete, name = 'delete_vendor_complete'),
    path('new_vendor', vendors_views.new_vendor, name='new_vendor'),
    path('vendor/<vendor_id>', vendors_views.vendor, name='vendor'),
    path('edit_vendor/<vendor_id>', vendors_views.edit_vendor, name='edit_vendor'),
    path('delete_vendor/<vendor_id>', vendors_views.delete_vendor, name='delete_vendor'),

    path('purchases/', purchases_views.purchases_home, name='purchases_home'),
    path('purchases2/', purchases_views.purchases_home_two, name='purchases_home_two'),
    path('new_purchase/<vendor_id>', purchases_views.new_purchase, name='new_purchase'),
    path('edit_purchase/<bill_no>/<item_sale_12>', purchases_views.edit_purchase, name='edit_purchase'),
    path('delete_purchase/<bill_no>', purchases_views.delete_purchase, name='delete_purchase'),
    path('delete_purchase2/<bill_no>', purchases_views.delete_purchase_two, name='delete_purchase_two'),

#    path('api/v1/',include('djoser.urls')),
#    path('api/v1/',include('djoser.urls.authtoken'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
