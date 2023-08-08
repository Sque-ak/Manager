from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Product(models.Model):
    """ Products our company like flour, molasses and etc.
    """

    name = models.CharField(max_length = 120, help_text = 'Напишите Названия Продукта', verbose_name = 'Наименнование')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        
    pass

class Transport(models.Model):
    """ Actually the model is transportation.
    """

    name = models.CharField(max_length = 120, help_text = 'Напишите назваиня Типа Транспортировки', verbose_name = 'Наименнование')
    controlling_transport = models.ManyToManyField(User, blank = True, help_text = 'Распоряжение получит', verbose_name = 'Распоряжение получит', related_name='controlling_transport')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Транспортировка'
        verbose_name_plural = 'Транспортировки'

    pass

class Shipment(models.Model):
    """ Model for shipments types.
    """

    name = models.CharField(max_length = 120, help_text = 'Напишите названия отгрузки', verbose_name = 'Наименнование')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Отгрузка груза'
        verbose_name_plural = 'Отгрузки груза'

    pass

class Company(models.Model):
    """ The company which will be added to the "order" list 
    and may for search by users any contacts information about company.
    """ 

    name = models.CharField(max_length = 120, help_text = 'Напишите названия Компании', verbose_name = 'Наименнование')
    contact_name = models.CharField(max_length = 120, help_text = 'Напишите Ф.И.О.', blank = True, verbose_name = 'Контактное Имя')
    contact_phone = models.CharField(max_length = 16, help_text = 'Напишите Номер Телефона', blank = True, verbose_name = 'Контактный Телефон')
    contact_email = models.EmailField(help_text = 'Укажите Адресс Электронной Почты', blank = True, verbose_name = 'Контактный Е-Майл')
    note = models.TextField(max_length = 1000, help_text = 'Введите Описание', blank = True, verbose_name = 'Заметки')

    class Meta:
        ordering = ['-name']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name

    def get_absoulute_url(self):
        return reverse('company-detail', args=[str(self.id)])

    pass

class OrderInstance(models.Model):
    """  This is model will be group up all the "orders" 
    to the alone "order" with tables, "controlling users" list and etc.
    """

    title = models.CharField(max_length = 120, help_text = 'Наименнование распоряжения', verbose_name = 'Наименнование')
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = 'Уникальный ID', verbose_name = 'Уникальный ID')
    id_document = models.IntegerField(help_text = 'Уникальный ID', verbose_name = 'Уникальный ID', blank = True, default = 0)
    due_back = models.DateField(null = True, blank = True, verbose_name = 'Дата подачи распоряжения') 
    date_allow = models.DateField(null = True, blank = True, verbose_name = 'Дата согласования распоряжения')
    date_finish = models.DateField(null = True, blank = True, verbose_name = 'Дата исполнения распоряжения')

    controlling = models.ManyToManyField(User, blank = True, help_text = 'Распоряжение получит', verbose_name = 'Распоряжение получит', related_name = 'controlling')
    controlling_allow = models.ManyToManyField(User, blank = True, help_text = 'Распоряжение одобрил', verbose_name = 'Распоряжение одобрил', related_name = 'controlling_allow')
    controlling_disallow = models.ManyToManyField(User, blank = True, help_text = 'Распоряжение неодбрил', verbose_name = 'Распоряжение неодбрил', related_name = 'controlling_disallow')

    created_by = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Исполнитель распоряжения', related_name = 'created_by')
    shipment_by = models.ForeignKey(Shipment, on_delete = models.CASCADE, help_text = 'Выберите отгрузку', blank = True, null=True, default=None, verbose_name = 'Отгрузка от', related_name = 'shipment_by')

    LOAN_STATUS = (
        ('p', 'В Процессе'),
        ('w', 'На согласование'),
        ('j', 'На исполнение'),
        ('a', 'Исполнено'),
        ('d', 'Отказано'),
    )

    LOAN_TYPE_ORDER = (
        ('kp', 'Паточный'),
        ('kz', 'Комбикормовый завод'),
        ('ml', 'Мельница'),
    )

    status = models.CharField(max_length = 16, choices = LOAN_STATUS, blank = True, default = 'p', verbose_name = 'Статус')
    type_order = models.CharField(max_length = 16, choices = LOAN_TYPE_ORDER, default = 'kp', verbose_name = 'Тип распоряжения')


    class Meta:
        ordering = ['-due_back', '-status']
        permissions = (("sign_order", "Can sign order"), ("sign_order_manager", "Sign order manager"),)
        verbose_name = 'Распоряжение'
        verbose_name_plural = 'Распоряжения'

    def display_created_by(self):
        self.full_name = '' #For if the user haven't name or last name.

        if self.created_by.last_login:
            self.full_name = self.full_name + f'{self.created_by.last_name}'
        if self.created_by.first_name:
            self.full_name = self.full_name + f' {self.created_by.first_name[0]}.'

        return self.full_name

    def __str__(self):
        return f'{self.title}'

    def get_absoulute_url(self):
        return reverse('order_detail', args=[str(self.id)])

    display_created_by.short_description = 'Создатель Распоряжения'
    pass

class Order(models.Model):
    """ This is class is table "order" it will be related to some "order instance",
    but mostly with one "order instance".
    """
    
    company = models.ForeignKey(Company, on_delete = models.CASCADE, verbose_name = 'Компания')
    products = models.ManyToManyField(Product, help_text = 'Выберите Продукт', verbose_name = 'Продукция')
    date_of_created = models.DateField(auto_now_add = True, verbose_name = 'Дата Создания')
    date_of_shipment = models.DateField(help_text = 'Укажите Дату Отгрузки', verbose_name = 'Дата Отгрузки')
    net_weight = models.DecimalField(max_digits = 19, decimal_places = 2, help_text = 'Введите вес', verbose_name = 'Вес Нетто, тн')
    transport_order = models.ForeignKey(Transport, on_delete = models.CASCADE, help_text = 'Выберите тип транспорортировки', verbose_name = 'Транспортировка')
    transport_number = models.IntegerField(blank = True, default = 0, help_text = 'Количество транспорта', verbose_name = 'Количество транспорта')
    note = models.TextField(max_length = 1000, help_text = 'Введите описание', blank = True, verbose_name = 'Заметки')
    order_by = models.ForeignKey(OrderInstance, on_delete = models.CASCADE, help_text = 'Выберите распоряжение', verbose_name = 'Распоряжение', related_name='orderInstanceBy')

    class Meta:
        ordering = ['date_of_created']
        verbose_name = 'Таблица распоряжения'
        verbose_name_plural = 'Таблиции распоряжений'

    def display_products(self):
        return ', '.join(products.name for products in self.products.all()[:3])

    def __str__(self):
        return f'Распоряжение ({self.order_by.id} - {self.company.name}) '

    display_products.short_description = 'Продукты'
    pass

class TimeExecutionUser(models.Model):
    """ This is model in base for remeber time when user accept and disaccept some order.
    """
    time = models.DateTimeField(null = True, blank = True, default=timezone.now, verbose_name = 'Дата и время подписания распоряжения')
    time_got_order = models.DateTimeField(null = True, blank = True, default=timezone.now, verbose_name = 'Дата и время получения распоряжения')
    user = models.ForeignKey(User, blank = True, on_delete = models.CASCADE, verbose_name = 'Подписывающий', related_name = 'execution_user')
    order_by = models.ForeignKey(OrderInstance, on_delete = models.CASCADE, help_text = 'Выберите распоряжение', verbose_name = 'Распоряжение', related_name='order_execution_user_time_by')
    got_order = models.BooleanField(default = False, help_text = 'Получил ли пользователь распоряжение', verbose_name = 'Получено ли распоряжение')

    class Meta:
        verbose_name = 'Время подписии'
        verbose_name_plural = 'Время подписей'

    def __str__(self):
        return f'Пользователь: {self.user} - Распоряжение: {self.order_by} '

    pass