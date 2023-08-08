from django.db import models
from django.db.models.fields import related
from django.urls import reverse 
from django.contrib.auth.models import User


class Shipper(models.Model):
    """Shipper are users which to do something,
    i made it for list items on editable form.
    """

    name = models.CharField(max_length = 86, help_text = 'Ф.И.О. или Название', verbose_name = 'Ф.И.О. или Название')

    class Meta:
        verbose_name = 'Груза отправитель'
        verbose_name_plural = 'Груза отправители'

    def __str__(self):
        return f'{self.name}'

class Address(models.Model):
    """Address for history to editable form.
    """

    name = models.CharField(max_length = 120, help_text = 'Адрес отправки', verbose_name = 'Адрес отправки')

    class Meta:
        verbose_name = 'Адрес отправки'
        verbose_name_plural = 'Адреса отправки'

    def __str__(self):
        return f'{self.name}'

class Attechment(models.Model):
    """Attechment like filemanager.
    """

    attechment = models.FileField(upload_to='uploads/%Y/%m/%d/')

    class Meta:
        verbose_name = 'Вложение ЖД документа'
        verbose_name_plural = 'Вложения ЖД документов'

    def __str__(self):
        return f'№{self.id}'

    def get_absoulute_url(self):
        return reverse('attechment-detail', args=[str(self.id)]) 

class Supplier(models.Model):
    """Address for history to editable form.
    """

    name = models.CharField(max_length = 86, help_text = 'Ф.И.О. или Название', verbose_name = 'Ф.И.О. или Название')

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return f'{self.name}'

########################################################################################
#Main Railway block start

class RailwayOrder(models.Model):
    """This is main model of railway order. All RW orders will be made by the model,
    i hope it will be worked.
    """
    
    date_of_shipment = models.DateField(verbose_name = 'Дата')
    date_of_created = models.DateField(verbose_name = 'Дата создания')

    address = models.ForeignKey(Address, on_delete = models.CASCADE, verbose_name = 'Адрес отправки', related_name='rw_address')
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Автор документа', related_name='rw_created_by')
    note = models.TextField(max_length = 324, help_text = 'Комментарий', blank = True, verbose_name = 'Комментарий')

    shipper = models.ForeignKey(Shipper, on_delete = models.CASCADE, verbose_name = 'Груза отправитель', related_name='shipper_rworder')
    attechment = models.ManyToManyField(Attechment, blank = True, verbose_name = 'Вложения', related_name='attechment_rworder')

    id = models.AutoField(primary_key=True, editable=False, verbose_name = 'Номер документа')

    TYPE_RAILWAY_ORDER = {
        ('p', 'Готовится к отправке'),
        ('s', 'В пути'),
        ('r', 'Прибыл'),
    }

    type_railwayorder = models.CharField(max_length = 16, choices = TYPE_RAILWAY_ORDER, blank = True, default = 'p', verbose_name = 'Тип документа')

    class Meta:
        ordering = ['-date_of_created']
        verbose_name = 'ЖД документ'
        verbose_name_plural = 'ЖД документы'

    def __str__(self):
        return f'№{self.id}'

    def get_absoulute_url(self):
        return reverse('railway_update_page', args=[str(self.id)])

#Main Railway block end
########################################################################################

########################################################################################
#Sub Railway block start

class RecipientDoc(models.Model):
    """Model template for table by document.
    """
    
    number_of_wagon = models.IntegerField(help_text = 'Номер вагона', verbose_name = 'Номер вагона')

    sender_gross = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Брутто', verbose_name = 'Брутто')
    sender_tara = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Тара', verbose_name = 'Тара')
    sender_net = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Нетто', verbose_name = 'Нетто')

    rec_gross = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Брутто', verbose_name = 'Брутто')
    rec_tara = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Тара', verbose_name = 'Тара')
    rec_net = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Нетто', verbose_name = 'Нетто')

    difference = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Разница', verbose_name = 'Разница')
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, verbose_name = 'Поставщик', related_name='supplier_rcdoc')

    note = models.TextField(max_length = 160, help_text = 'Прочие', blank = True, verbose_name = 'Прочие')
    rworder_by = models.ForeignKey(RailwayOrder, on_delete = models.CASCADE, verbose_name = 'ЖД Заявка', related_name='recipientdoc_rworder')

    class Meta:
        verbose_name = 'Прибывший вагон'
        verbose_name_plural = 'Прибывшие вагоны'

    def __str__(self):
        return f'№{self.id}'


class SenderDoc(models.Model):
    """Model template for table by document.
    """
    
    number_of_wagon = models.IntegerField(help_text = 'Номер вагона', verbose_name = 'Номер вагона')

    sender_gross = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Брутто', verbose_name = 'Брутто')
    sender_tara = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Тара', verbose_name = 'Тара')
    sender_net = models.DecimalField(max_digits = 11, decimal_places = 2, help_text = 'Нетто', verbose_name = 'Нетто')

    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, verbose_name = 'Поставщик', related_name='supplier_sendoc')

    note = models.TextField(max_length = 160, help_text = 'Прочие', blank = True, verbose_name = 'Прочие')
    rworder_by = models.ForeignKey(RailwayOrder, on_delete = models.CASCADE, verbose_name = 'ЖД Заявка', related_name='senderdoc_rworder')

    class Meta:
        verbose_name = 'Убывший вагон'
        verbose_name_plural = 'Убывшие вагоны'

    def __str__(self):
        return f'№{self.id}'

#Sub Railway block end
########################################################################################