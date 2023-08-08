from django.contrib import admin
from .models import Product, Transport, Shipment, \
                    Company, Order, OrderInstance, TimeExecutionUser


class Orderinline(admin.TabularInline):
    model = Order
    extra = 0
    max_num = 0
    fields = ['company', 'products', 'transport_order', 'transport_number', 
              'net_weight', 'date_of_shipment', 'note']
    pass

class OrderInstanceInline(admin.TabularInline):
    model = OrderInstance
    extra = 0
    max_num = 0
    readonly_fields = ['due_back', 'status', 'display_created_by']
    pass

class TimeExecutionUserInline(admin.TabularInline):
    model = TimeExecutionUser
    extra = 0
    max_num = 0
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 
                    'contact_phone', 'contact_email')
    inlines = [Orderinline]
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('company', 'display_products', 'net_weight', 
                    'date_of_created', 'note')
    fieldsets = (
        ('Основное', {
            'fields': (['company', ('date_of_shipment', 'net_weight'), 
                        'products', 'transport_order', 'transport_number']) 
        }),
        ('Допольнительно', {
            'fields': (['order_by', 'note'])
        }),
    )
    pass

@admin.register(OrderInstance)
class OrderInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('title', 'due_back', 'date_allow', 'date_finish', 
                    'status', 'display_created_by', 'id')
                    
    fields = ['title', 'type_order', 'shipment_by',
             ('date_allow', 'date_finish', 'due_back', 'status'),
             ('controlling', 'controlling_allow', 'controlling_disallow'), 'id', 'created_by', 'id_document']

    inlines = [Orderinline, TimeExecutionUserInline]


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    pass


admin.site.register(Product)
admin.site.register(Shipment)
admin.site.register(TimeExecutionUser)

