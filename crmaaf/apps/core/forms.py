from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from crmaaf.apps.core.services.widgets import DateInput
from crmaaf.apps.core.services.user_controlling_worker import add_users_controlling_by_group_to_order
import datetime  


class NewOrderInstanceForm(BSModalModelForm):
    """ This is form will created new order.
    For created order-instance need to only title, date of created and type order,
    other fields must auto will filled itself.
    """

    class Meta:
        model = OrderInstance
        fields = ('title', 'type_order', 'shipment_by')
        exclude = ('due_back',)
        

    def save(self, commit=True): # Auto filled controlling list with users when it will saved.

        self.object = super(BSModalModelForm, self).save(commit=False)

        if not self.request.is_ajax():

            if (self.object.id_document == 0):

                self.object_list = OrderInstance.objects.order_by('id_document')
                if len(self.object_list) == 0:  # if there are no objects
                    self.object.id_document = int(f'1')
                else:
                    self.object.id_document =  int(f'{int(len(self.object_list)) + 1}')

            if self.object.status == 'p':
                self.object.created_by = self.request.user
                self.object.due_back = datetime.date.today()    

            self.object.save()

            add_users_controlling_by_group_to_order(self.object)

            self.transport_pks  = self.object.orderInstanceBy.values_list('transport_order', flat=True)

            for i in Transport.objects.filter(pk__in=self.transport_pks).all():
                for j in i.controlling_transport.all():
                    self.object.controlling.add(j)

        return self.object


class NewinOrderForm(BSModalModelForm):
    """ This is form will created new order to the instance order table,
    but actually it will made individual order and then 
    connected via Forgive Key to the instance order.
    """

    class Meta:
        model = Order
        fields = ('company', 'products', 'date_of_shipment', 
                  'net_weight', 'transport_order', 'transport_number', 'note')
        widgets = {
            'date_of_shipment' : DateInput(
                                        format=('%Y-%m-%d'),
                                        attrs={'type': 'date',
                                               'value': datetime.date.today()}
                                        ),
        }

    def save(self, commit=True): # Auto filled controlling list with users when it will saved.

        self.object = super(BSModalModelForm, self).save(commit=True)

        if not self.request.is_ajax():

            add_users_controlling_by_group_to_order(self.object.order_by)

            for i in self.object.transport_order.controlling_transport.all():
                self.object.order_by.controlling.add(i)

            self.object.save()

        return self.object


class NewCompanyForm(BSModalModelForm):

    class Meta:
        model = Company
        fields = '__all__'
    pass

class NewProductForm(BSModalModelForm):

    class Meta:
        model = Product
        fields = '__all__'
    pass

class NewTransportForm(BSModalModelForm):

    class Meta:
        model = Transport
        fields = ('name', 'controlling_transport')
    pass

class NewShipmentForm(BSModalModelForm):

    class Meta:
        model = Shipment
        fields = ('name',)
    pass