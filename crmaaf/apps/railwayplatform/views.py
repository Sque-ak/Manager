from crmaaf.apps.railwayplatform.services.railwayorders.logic_order import change_train_doc_status, create_new_railway_order
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import *
from .filters import *
from .forms import *

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class RailwayOrderView(LoginRequiredMixin, generic.ListView):
    """ Railway Order is showing table with itself orders. 
    """
    model = RailwayOrder
    context_object_name = 'context_rw_order'
    template_name = "railway_index.html"
    paginate_by = 50

    def get_context_data(self):
        # This for search engine.
        self.railway_filter = RailwayOrderFilter(self.request.GET, queryset=RailwayOrder.objects.all())
        return {'railway_order_filter': self.railway_filter}

    pass

class RailwayOrderUpdateView(LoginRequiredMixin, BSModalUpdateView):
    """ This class is DetailView and UpdateView at the same time.
    """
    form_class = RailWayOrderForm
    formset_class = SenderFormset, RecipientFormset
    model = RailwayOrder
    template_name = "railway/forms/railway_update_modal_form.html"
    success_url = reverse_lazy('railway_order_page')

    def get_context_data(self, **kwargs):
        context = super(RailwayOrderUpdateView, self).get_context_data(**kwargs)
        formset = SenderFormset(instance=self.get_object())
        formset2 = RecipientFormset(instance=self.get_object())
        context['recipient_formset'] = formset2
        context['sender_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formsets = SenderFormset(self.request.POST, instance=self.object)
        formsets2 = RecipientFormset(self.request.POST, instance=self.object)

        if form.is_valid() and not self.request.is_ajax():
            if formsets.is_valid():
                formsets.save()
            else:
                print("Formsets sender invalid;")
                print(formsets.errors)
            
            if formsets2.is_valid():
                formsets2.save()
            else:
                print("Formsets recipient invalid;")
                print(formsets2.errors)

            return self.form_valid(form)
        return self.form_invalid(form)


@login_required
@user_passes_test(lambda u: u.has_perm('core.can_add_railwayorder'))
def NewRailwayOrder(request):
    """ Create new railway order by blank
    """
    create_new_railway_order(request)
    return redirect('railway_order_page')

@login_required
@user_passes_test(lambda u: u.has_perm('core.sign_order'))
def SendTrain(request, pk):
    """ When user will clicked to button,
    doc will change status to train on it way.
    """
    self__railway_order_obj = RailwayOrder.objects.get(pk=pk)
    change_train_doc_status(request, self__railway_order_obj)

    return redirect('railway_order_page')


### ADDRESS FORM ###
def RailwayAddressCreatePopup(request):
	form = RailwayAdressForm(request.POST or None)
	if form.is_valid():
		instance = form.save()
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_address");</script>' % (instance.pk, instance))
	
	return render(request, "railway/forms/popup_form.html", {"form" : form})

def RailwayAddressEditPopup(request, pk = None):
	instance = get_object_or_404(Address, pk = pk)
	form = RailwayAdressForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save()
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_address");</script>' % (instance.pk, instance))

	return render(request, "railway/forms/popup_form.html", {"form" : form})
### ADDRESS FORM END ###

### SHIPPER FORM ###
def RailwayShipperCreatePopup(request):
	form = RailwayShipperForm(request.POST or None)
	if form.is_valid():
		instance = form.save()
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_shipper");</script>' % (instance.pk, instance))
	
	return render(request, "railway/forms/popup_form.html", {"form" : form})

def RailwayShipperEditPopup(request, pk = None):
	instance = get_object_or_404(Shipper, pk = pk)
	form = RailwayShipperForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save()
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_shipper");</script>' % (instance.pk, instance))

	return render(request, "railway/forms/popup_form.html", {"form" : form})
### SHIPPER FORM END ###

### SUPPLIER FORM ###
def RailwaySupplierCreatePopup(request):
	form = RailwaySupplierForm(request.POST or None)
	if form.is_valid():
		instance = form.save()
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_supplier");</script>' % (instance.pk, instance))
	
	return render(request, "railway/forms/popup_form.html", {"form" : form})
### SUPPLIER FORM END ###