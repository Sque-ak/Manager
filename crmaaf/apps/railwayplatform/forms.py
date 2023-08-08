from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from .models import *
from crmaaf.apps.core.services.widgets import *


__all__ = ['RailWayOrderForm', 'SenderFormset', 'RecipientFormset', 'RailwayAdressForm', 'RailwayShipperForm', 'RailwaySupplierForm']

class RailWayOrderForm(BSModalModelForm):
    """ This is form will created new order to the instance order table,
    but actually it will made individual order and then 
    connected via Forgive Key to the instance order.
    """

    def __init__(self, *args, **kwargs):
        super(RailWayOrderForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not instance.type_railwayorder == 'p':
            self.fields['address'].required = False
            self.fields['shipper'].required = False
            self.fields['address'].widget.attrs['disabled'] = 'disabled'
            self.fields['shipper'].widget.attrs['disabled'] = 'disabled'
        
        if instance and  instance.type_railwayorder == 'r':
            self.fields['note'].disabled = True
    

    
    def clean_address(self):
        instance = getattr(self, 'instance', None)
        if instance and not instance.type_railwayorder == 'p':
            return instance.address
        else:
            return self.cleaned_data.get('address', None)

    def clean_shipper(self):
        instance = getattr(self, 'instance', None)
        if instance and not instance.type_railwayorder == 'p':
            return instance.shipper
        else:
            return self.cleaned_data.get('shipper', None)



    class Meta:
        model = RailwayOrder
        fields = '__all__' 
        widgets = {
            'date_of_shipment' : DateInput(
                                 format=('%Y-%m-%d'),
                                 attrs={'type': 'date'}
                                 ),}
        exclude = ('created_by',
                   'date_of_created',
                   'type_railwayorder'
                  )
    pass


class RailwayAdressForm(forms.ModelForm):
    """ This's form for add button and edit button.
    """

    class Meta:
        model = Address
        fields = '__all__'

    pass

class RailwayShipperForm(forms.ModelForm):
    """ This's form for add button and edit button.
    """

    class Meta:
        model = Shipper
        fields = '__all__'

    pass

class RailwaySupplierForm(forms.ModelForm):
    """ This's form for add button and edit button.
    """

    class Meta:
        model = Supplier
        fields = '__all__'

    pass

class RecipientForm(forms.ModelForm):
    """ This is form for inlineformset factory
    RecipientFormset
    """

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and  instance.rworder_by.type_railwayorder == 'r':
            self.fields['rec_gross'].disabled = True
            self.fields['rec_tara'].disabled = True
            self.fields['rec_net'].disabled = True
            self.fields['note'].disabled = True
            self.fields['difference'].disabled = True
    

    class Meta:
        models = RecipientDoc
        exclude = ['number_of_wagon','sender_gross','sender_tara','sender_net','supplier']
        fields = '__all__'
        
    pass

SenderFormset = forms.inlineformset_factory(RailwayOrder, SenderDoc, fields = '__all__', extra = 1, can_delete = True)
RecipientFormset = forms.inlineformset_factory(RailwayOrder, RecipientDoc, form = RecipientForm, extra = 0, can_delete = False)

