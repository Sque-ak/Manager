from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from crmaaf.settings import TG_BOT, GROUP_ID_TG
from .forms import ContactWithUsForm, ContactWithUsFormProduct


def index(request):
    if request.method == "POST" and "contact" in request.POST:
        form_contact_with_us = ContactWithUsForm(request.POST) 
        form_product_contact = ContactWithUsFormProduct()

        if form_contact_with_us.is_valid():
            context = (
                "<pre>Сообщение от посетителя сайта:</pre> \n" +
                '<b>Имя:</b> ' + form_contact_with_us['name_user'].value() + '\n' +
                '<b>Телефон:</b> ' + form_contact_with_us['phone_user'].value() + '\n' +
                '<b>Сообщение:</b> ' + form_contact_with_us['message_user'].value())
        
            TG_BOT.send_message(GROUP_ID_TG, str(context), parse_mode='HTML')
            return HttpResponseRedirect('')
    elif request.method == "POST" and "order" in request.POST:
        form_contact_with_us = ContactWithUsForm() 
        form_product_contact = ContactWithUsFormProduct(request.POST)
        
        if form_product_contact.is_valid():
            context = (
                "\n<b>Заказ продукта:</b> \n" + 
                '<b>Имя:</b> ' + form_product_contact['name_user'].value() + '\n' +
                '<b>Телефон:</b> ' + form_product_contact['phone_user'].value() + '\n' +
                '<b>Сообщение:</b> ' + form_product_contact['message_user'].value() + '\n' +
                '<b>Наименование продукта:</b> ' + form_product_contact['order_product'].value() + '\n' +
                '<b>Количество:</b> ' + form_product_contact['count_product'].value() + '\n')

            TG_BOT.send_message(GROUP_ID_TG, str(context), parse_mode='HTML')
            return HttpResponseRedirect('')
    else:
        form_contact_with_us = ContactWithUsForm()
        form_product_contact = ContactWithUsFormProduct()
    return render(request, 'main_page.html', {'form_contact': form_contact_with_us, 'form_product_contact': form_product_contact})

def dontwork(request):
    return render(request, 'site_dont_work.html')

def contacts(request):
    form_contact_with_us = ContactWithUsForm()
    return render(request, 'contacts.html', {'form_contact': form_contact_with_us})

def shareholder(request):
    return render(request, 'shareholder.html')

def about_us(request):
    return render(request, 'about_us.html')

def history_us(request):
    return render(request, 'history_us.html')

def group(request):
    return render(request, 'group.html')