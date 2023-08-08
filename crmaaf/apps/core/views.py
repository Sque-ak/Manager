from django.shortcuts import render, redirect
from django.views import generic
from django_filters.views import FilterView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView

from .models import *
from .forms import *
from .serializers import *
from .filters import OrderFilter

from crmaaf.apps.core.services.order_manager import * 

from rest_framework.response import Response
from rest_framework.views import APIView




@login_required
def index(request):

    last_order_instance_allow = OrderInstance.objects.filter(status__exact = 'a').first()
    last_order_instance_consideration = OrderInstance.objects.filter(status__exact = 'w').first()


    #Orders are proccessing
    num_order_instance_allow = OrderInstance.objects.filter(status__exact = 'a').count()
    num_order_instance_disallow = OrderInstance.objects.filter(status__exact = 'd').count()
    num_order_instance_consideration = OrderInstance.objects.filter(status__exact = 'w').count()
    

    


    CONTEXT = {

        'num_order_instance_allow': num_order_instance_allow,
        'num_order_instance_disallow': num_order_instance_disallow,
        'num_order_instance_consideration': num_order_instance_consideration,
        'last_order_instance_consideration': last_order_instance_consideration,
        'last_order_instance_allow': last_order_instance_allow,
        'last_order_instance_disallow': last_order_instance_allow,
        
    }

    #Status
    for i in request.user.groups.all():
        if i.name == "Controlling":
            CONTEXT['num_order_instance_consideration'] = OrderInstance.objects.filter(status = 'w').filter(controlling = request.user.id).count()
            CONTEXT['num_order_instance_allow'] = OrderInstance.objects.filter(status = 'a').filter(controlling_allow = request.user.id).count()
            CONTEXT['num_order_instance_disallow'] = OrderInstance.objects.filter(status = 'd').filter(controlling_disallow = request.user.id).count()
            CONTEXT['last_order_instance_consideration'] = OrderInstance.objects.filter(status = 'w').filter(controlling = request.user.id).first()
            CONTEXT['last_order_instance_allow'] = OrderInstance.objects.filter(status = 'a').filter(controlling_allow = request.user.id).first()
            CONTEXT['last_order_instance_disallow'] = OrderInstance.objects.filter(status = 'd').filter(controlling_disallow = request.user.id).first()

    return render(request, 'index.html', context = CONTEXT)

class ChartAPIView(APIView):
    """ Simple API for chart;
    """
    def get(self, request):
        self.instance_product = Order.objects.filter(products = '1').order_by('-date_of_created')
        self.serializer = OrderListSerializer(self.instance_product, many=True)
        return Response(self.serializer.data)


# ORDER MANIPULATION

class OrdersListView(LoginRequiredMixin, FilterView):

    model = OrderInstance
    template_name = "core/order/order_list.html"
    paginate_by = 35
    success_url = 'orders'
    filterset_class = OrderFilter

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['order_filter'] = OrderFilter(self.request.GET)

        return context

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = OrderInstance
    context_object_name = 'orders_detail'
    template_name = "core/order/order_detail.html"

    def dispatch(self, *args, **kwargs):
        in_order_obj = OrderInstance.objects.get(pk=self.kwargs["pk"])
        check_time_execution_have(self.request, in_order_obj)
        return super(OrderDetailView, self).dispatch( *args, **kwargs)

class PrintOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = OrderInstance
    context_object_name = 'orders_detail'
    template_name = "core/order/order_detail_print.html"

#Order actions
class OrderCreateView(LoginRequiredMixin, BSModalCreateView): #CREATE ORDER
    form_class = NewOrderInstanceForm
    template_name = 'core/form/create_form.html'
    success_url = reverse_lazy('orders')

    #def get_success_url(self):
    #    return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})

class OrderDeleteView(LoginRequiredMixin, BSModalDeleteView): #DELETE ORDER
    model = OrderInstance
    template_name = "core/form/delete_form.html"
    success_message = "Распоряжение удаленно"
    success_url = reverse_lazy('orders')

class OrderUpdateView(LoginRequiredMixin, BSModalUpdateView): #UPDATE ORDER
    model = OrderInstance
    form_class = NewOrderInstanceForm
    template_name = "core/form/update_form.html"
    success_url = reverse_lazy('orders')

class inOrderDeleteView(LoginRequiredMixin, BSModalDeleteView): #DELETE IN-ORDER
    model = Order
    template_name = "core/form/delete_form.html"
    success_message = "Инстанц Распоряжение Удаленно"
    
    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order_by.id})

class inOrderUpdateView(LoginRequiredMixin, BSModalUpdateView): #UPDATE IN-ORDER
    model = Order
    form_class = NewinOrderForm
    template_name = "core/form/update_form.html"

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.order_by.id})

class inOrderCreateView(LoginRequiredMixin, BSModalCreateView): #CREATE IN-ORDER
    form_class = NewinOrderForm
    template_name = 'core/form/create_form.html'

    def form_valid(self, form):
        form.instance.order_by = OrderInstance.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.kwargs["pk"]})

@login_required
@user_passes_test(lambda u: u.has_perm('core.add_order'))
def inSendOrder(request, pk):
    """ Send the order to the controller users
    or just change the status.
    """

    in_order_obj = OrderInstance.objects.get(pk=pk)
    in_order_obj.status = "w"
    
    email_controlling = in_order_obj.controlling.filter(groups__name='BOSS').all()

    send_email_new_order('core/message/send_order.html', f'Поступило распоряжение "{ in_order_obj.title }" на согласование.', email_controlling, in_order_obj)

    in_order_obj.save()

    return redirect('order_detail',  in_order_obj.pk)

@login_required
@user_passes_test(lambda u: u.has_perm('core.sign_order'))
def allowOrder(request, pk):
    """ Move user pack to group allow. 
    """
    self__in_order_obj = OrderInstance.objects.get(pk=pk)
    controlling_pack = self__in_order_obj.controlling.filter(groups__name='BOSS').all()

    move_users_to_allow_group(request, self__in_order_obj, controlling_pack, request.user)

    return redirect('order_detail',  self__in_order_obj.pk)

@login_required
@user_passes_test(lambda u: u.has_perm('core.sign_order_manager'))
def allowOrderManager(request, pk):
    """ Move user pack to group allow by manager. 
    """
    self__in_order_obj = OrderInstance.objects.get(pk=pk)
    self__user_id = User.objects.get(id=request.GET['user_id'])
    controlling_pack = self__in_order_obj.controlling.filter(groups__name='BOSS').all()
    move_users_to_allow_group(request, self__in_order_obj, controlling_pack, self__user_id)

    return redirect('order_detail',  self__in_order_obj.pk)

@login_required
@user_passes_test(lambda u: u.has_perm('core.sign_order'))
def disallowOrder(request, pk):
    """ When user will clicked to button disallow order,
    from controller group user move to disallow group.
    """
    self__in_order_obj = OrderInstance.objects.get(pk=pk)
    move_users_to_disallow_group(request, self__in_order_obj)

    return redirect('order_detail',  self__in_order_obj.pk)

# ORDER MANIPULATION

# COMPANY MANIPULATION
    
class companyListView(LoginRequiredMixin, generic.ListView):
    model = Company
    context_object_name = 'company'
    template_name = "core/company/company_list.html"
    paginate_by = 20
    success_url = 'company'

class companyCreateView(LoginRequiredMixin, BSModalCreateView): #CREATE COMPANY
    form_class = NewCompanyForm
    template_name = 'core/form/create_form.html'
    success_url = reverse_lazy('company')

class companyUpdateView(LoginRequiredMixin, BSModalUpdateView): #UPDATE COMPANY
    model = Company
    form_class = NewCompanyForm
    template_name = "core/form/update_form.html"
    success_url = reverse_lazy('company')

class companyDeleteView(LoginRequiredMixin, BSModalDeleteView): #DELETE COMPANY
    model = Company
    template_name = "core/form/delete_form.html"
    success_message = "Компания удалена"
    success_url = reverse_lazy('company')

# COMPANY MANIPULATION

# PRODUCT MANIPULATION
    
class productListView(LoginRequiredMixin, generic.ListView):
    model = Product
    context_object_name = 'product'
    template_name = "core/product/product_list.html"
    paginate_by = 20
    success_url = 'product'

class productCreateView(LoginRequiredMixin, BSModalCreateView): #CREATE PRODUCT
    form_class = NewProductForm
    template_name = 'core/form/create_form.html'
    success_url = reverse_lazy('product')

class productUpdateView(LoginRequiredMixin, BSModalUpdateView): #UPDATE PRODUCT
    model = Product
    form_class = NewProductForm
    template_name = "core/form/update_form.html"
    success_url = reverse_lazy('product')

class productDeleteView(LoginRequiredMixin, BSModalDeleteView): #DELETE PRODUCT
    model = Product
    template_name = "core/form/delete_form.html"
    success_message = "Продукт удален"
    success_url = reverse_lazy('product')

# PRODUCT MANIPULATION 

# TRANSPORT MANIPULATION
    
class transportListView(LoginRequiredMixin, generic.ListView):
    model = Transport
    context_object_name = 'transport'
    template_name = "core/transport/transport_list.html"
    paginate_by = 20
    success_url = 'transport'

class transportCreateView(LoginRequiredMixin, BSModalCreateView): #CREATE TRANSPORT
    form_class = NewTransportForm
    template_name = 'core/form/create_form.html'
    success_url = reverse_lazy('transport')

class transportUpdateView(LoginRequiredMixin, BSModalUpdateView): #UPDATE TRANSPORT
    model = Transport
    form_class = NewTransportForm
    template_name = "core/form/update_form.html"
    success_url = reverse_lazy('transport')

class transportDeleteView(LoginRequiredMixin, BSModalDeleteView): #DELETE TRANSPORT
    model = Transport
    template_name = "core/form/delete_form.html"
    success_message = "Транспорт удален"
    success_url = reverse_lazy('transport')

# TRANSPORT MANIPULATION

# SHIPMENT MANIPULATION
    
class shipmentListView(LoginRequiredMixin, generic.ListView):
    model = Shipment
    context_object_name = 'shipment'
    template_name = "core/shipment/shipment_list.html"
    paginate_by = 20
    success_url = 'shipment'

class shipmentCreateView(LoginRequiredMixin, BSModalCreateView): #CREATE SHIPMENT
    form_class = NewShipmentForm
    template_name = 'core/form/create_form.html'
    success_url = reverse_lazy('shipment')

class shipmentUpdateView(LoginRequiredMixin, BSModalUpdateView): #UPDATE SHIPMENT
    model = Shipment
    form_class = NewShipmentForm
    template_name = "core/form/update_form.html"
    success_url = reverse_lazy('shipment')

class shipmentDeleteView(LoginRequiredMixin, BSModalDeleteView): #DELETE SHIPMENT
    model = Shipment
    template_name = "core/form/delete_form.html"
    success_message = "Отгрузка удалена"
    success_url = reverse_lazy('shipment')

# SHIPMENT MANIPULATION 