from django.contrib import admin
from .models import RailwayOrder, RecipientDoc, SenderDoc, Supplier, Shipper, Attechment, Address


class RailwayOrderinline(admin.TabularInline):
    model = RailwayOrder
    extra = 0
    max_num = 0
    readonly_fields = ['id', 'created_by']
    fields = ['date_of_shipment', 'date_of_created', 'shipper', 'address', 'attachment', 'note'] 

class RecipientDocinline(admin.TabularInline):
    model = RecipientDoc
    extra = 0
    max_num = 0

    readonly_fields = ['number_of_wagon', 'supplier', 'sender_gross', 'sender_tara', 'sender_net', 'rec_gross', 'rec_tara', 'rec_net', 'rworder_by', 'note']

class SenderDocinline(admin.TabularInline):
    model = SenderDoc
    extra = 0
    max_num = 0

    readonly_fields = ['number_of_wagon', 'supplier', 'sender_gross', 'sender_tara', 'sender_net', 'rworder_by', 'note']


@admin.register(RecipientDoc)
class RecipientDocAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'note')
    fieldsets = (
        ('Информация', {
            'fields': (['number_of_wagon', 'supplier', 'note']) 
        }),
        ('Отправитель', {
            'fields': ([('sender_gross', 'sender_tara', 'sender_net')])
        }),
        ('Получатель', {
            'fields': ([('rec_gross', 'rec_tara', 'rec_net')])
        }),
        ('Техническая часть', {
            'fields': ([ 'difference', 'rworder_by']) 
        }),
    )

@admin.register(SenderDoc)
class SenderDoc(admin.ModelAdmin):
    
    list_display = ('supplier', 'note')
    fieldsets = (
        ('Информация', {
            'fields': (['number_of_wagon', 'supplier', 'note']) 
        }),
        ('Отправитель', {
            'fields': ([('sender_gross', 'sender_tara', 'sender_net')])
        }),
        ('Техническая часть', {
            'fields': (['rworder_by']) 
        }),
    )


@admin.register(RailwayOrder)
class RailwayOrderAdmin(admin.ModelAdmin):

    list_display = ('id', 'address', 'created_by', 'note')
    readonly_fields = ('id', 'created_by')
    fieldsets = (
        ('Основное', {
            'fields': ([('date_of_shipment', 'date_of_created'), 'type_railwayorder', 'shipper', 'created_by', 'address', 'note', 'attechment']) 
        }),
    )

    inlines = [RecipientDocinline, SenderDocinline]
    
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)




admin.site.register(Supplier)
admin.site.register(Shipper)
admin.site.register(Attechment)
admin.site.register(Address)
