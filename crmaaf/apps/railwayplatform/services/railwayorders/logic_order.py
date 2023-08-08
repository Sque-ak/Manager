from datetime import datetime
from crmaaf.apps import railwayplatform
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from crmaaf.apps.railwayplatform.models import Address, RailwayOrder, Shipper, SenderDoc, RecipientDoc, Supplier
from crmaaf.apps.railwayplatform.forms import RecipientFormset

### GET AJAX ###

@csrf_exempt
def get_address_id(request):
	if request.is_ajax():
		self__address_name = request.GET['address_name']
		self__address_id = Address.objects.get(name = self__address_name).id
		data = {'address_id':self__address_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

@csrf_exempt
def get_shipper_id(request):
	if request.is_ajax():
		self__shipper_name = request.GET['shipper_name']
		self__shipper_id = Shipper.objects.get(name = self__shipper_name).id
		data = {'shipper_id':self__shipper_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

@csrf_exempt
def get_supplier_id(request):
	if request.is_ajax():
		self__supplier_name = request.GET['supplier_name']
		self__supplier_id = Supplier.objects.get(name = self__supplier_name).id
		data = {'supplier_id':self__supplier_id,}
		return HttpResponse(json.dumps(data), content_type='application/json')
	return HttpResponse("/")

### GOT AJAX ###

def change_train_doc_status(request, railway_order_obj) -> None:
	""" This is def will changed status to the order
	when train will be arrived or on it way.
	"""
	
	self__sender_doc_obj = SenderDoc.objects.filter(rworder_by = railway_order_obj)
	
	if railway_order_obj.type_railwayorder == 'p':
		railway_order_obj.type_railwayorder = 's'

		for i in self__sender_doc_obj.all():
			self__new_rd = RecipientDoc(number_of_wagon = i.number_of_wagon, 
									sender_gross = i.sender_gross,
									sender_tara = i.sender_tara,
									sender_net = i.sender_net,
									rec_gross = 0,
									rec_tara = 0,
									rec_net = 0,
									difference = 0,
									supplier = i.supplier,
									note = i.note,
									rworder_by = i.rworder_by) #Will be maked new recipient document for this document;
			self__new_rd.save()

	else: 
		railway_order_obj.type_railwayorder = 'r'


		

	railway_order_obj.save()
	pass

def create_new_railway_order(request):
	""" Create new railway order
	"""
	self__new_rd = RailwayOrder(date_of_shipment = datetime.now(),
								date_of_created = datetime.now(),
								address = Address.objects.get(name = 'Пусто'),
								created_by = request.user,
								shipper = Shipper.objects.get(name = 'Пусто'),
								type_railwayorder = 'p')
	self__new_rd.save()
	return self__new_rd.pk