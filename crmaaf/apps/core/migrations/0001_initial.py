# Generated by Django 3.1 on 2020-11-30 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите названия Компании', max_length=120, verbose_name='Наименнование')),
                ('contact_name', models.CharField(blank=True, help_text='Напишите Ф.И.О.', max_length=120, verbose_name='Контактное Имя')),
                ('contact_phone', models.CharField(blank=True, help_text='Напишите Номер Телефона', max_length=16, verbose_name='Контактный Телефон')),
                ('contact_email', models.EmailField(blank=True, help_text='Укажите Адресс Электронной Почты', max_length=254, verbose_name='Контактный Е-Майл')),
                ('note', models.TextField(blank=True, help_text='Введите Описание', max_length=1000, verbose_name='Заметки')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='OrderInstance',
            fields=[
                ('title', models.CharField(help_text='Наименнование распоряжения', max_length=120, verbose_name='Наименнование')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID', primary_key=True, serialize=False, verbose_name='Уникальный ID')),
                ('due_back', models.DateField(blank=True, null=True, verbose_name='Дата подачи распоряжения')),
                ('date_allow', models.DateField(blank=True, null=True, verbose_name='Дата согласования распоряжения')),
                ('date_finish', models.DateField(blank=True, null=True, verbose_name='Дата исполнения распоряжения')),
                ('status', models.CharField(blank=True, choices=[('p', 'В Процессе'), ('w', 'На согласование'), ('j', 'На исполнение'), ('a', 'Исполнено'), ('d', 'Отказано')], default='p', max_length=16, verbose_name='Статус')),
                ('type_order', models.CharField(choices=[('kp', 'Паточный'), ('kz', 'Комбикормовый завод'), ('ml', 'Мельница')], default='kp', max_length=16, verbose_name='Тип распоряжения')),
                ('controlling', models.ManyToManyField(blank=True, help_text='Распоряжение получит', related_name='controlling', to=settings.AUTH_USER_MODEL, verbose_name='Распоряжение получит')),
                ('controlling_allow', models.ManyToManyField(blank=True, help_text='Распоряжение одобрил', related_name='controlling_allow', to=settings.AUTH_USER_MODEL, verbose_name='Распоряжение одобрил')),
                ('controlling_disallow', models.ManyToManyField(blank=True, help_text='Распоряжение неодбрил', related_name='controlling_disallow', to=settings.AUTH_USER_MODEL, verbose_name='Распоряжение неодбрил')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель распоряжения')),
            ],
            options={
                'verbose_name': 'Распоряжение',
                'verbose_name_plural': 'Распоряжения',
                'ordering': ['-status', '-due_back'],
                'permissions': (('sign_order', 'Can sign order'),),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите Названия Продукта', max_length=120, verbose_name='Наименнование')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите названия отгрузки', max_length=120, verbose_name='Наименнование')),
            ],
            options={
                'verbose_name': 'Отгрузка груза',
                'verbose_name_plural': 'Отгрузки груза',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Напишите назваиня Типа Транспортировки', max_length=120, verbose_name='Наименнование')),
                ('controlling_transport', models.ManyToManyField(blank=True, help_text='Распоряжение получит', related_name='controlling_transport', to=settings.AUTH_USER_MODEL, verbose_name='Распоряжение получит')),
            ],
            options={
                'verbose_name': 'Транспортировка',
                'verbose_name_plural': 'Транспортировки',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='TimeExecutionUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата и время подписания распоряжения')),
                ('time_got_order', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата и время получения распоряжения')),
                ('got_order', models.BooleanField(default=False, help_text='Получил ли пользователь распоряжение', verbose_name='Получено ли распоряжение')),
                ('order_by', models.ForeignKey(help_text='Выберите распоряжение', on_delete=django.db.models.deletion.CASCADE, related_name='order_execution_user_time_by', to='core.orderinstance', verbose_name='Распоряжение')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='execution_user', to=settings.AUTH_USER_MODEL, verbose_name='Подписывающий')),
            ],
            options={
                'verbose_name': 'Время подписии',
                'verbose_name_plural': 'Время подписей',
            },
        ),
        migrations.AddField(
            model_name='orderinstance',
            name='shipment_by',
            field=models.ForeignKey(blank=True, default=None, help_text='Выберите отгрузку', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipment_by', to='core.shipment', verbose_name='Отгрузка от'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_created', models.DateField(auto_now_add=True, verbose_name='Дата Создания')),
                ('date_of_shipment', models.DateField(help_text='Укажите Дату Отгрузки', verbose_name='Дата Отгрузки')),
                ('net_weight', models.DecimalField(decimal_places=2, help_text='Введите вес', max_digits=19, verbose_name='Вес Нетто, тн')),
                ('transport_number', models.IntegerField(blank=True, default=0, help_text='Количество транспорта', verbose_name='Количество транспорта')),
                ('note', models.TextField(blank=True, help_text='Введите описание', max_length=1000, verbose_name='Заметки')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.company', verbose_name='Компания')),
                ('order_by', models.ForeignKey(help_text='Выберите распоряжение', on_delete=django.db.models.deletion.CASCADE, related_name='orderInstanceBy', to='core.orderinstance', verbose_name='Распоряжение')),
                ('products', models.ManyToManyField(help_text='Выберите Продукт', to='core.Product', verbose_name='Продукция')),
                ('transport_order', models.ForeignKey(help_text='Выберите тип транспорортировки', on_delete=django.db.models.deletion.CASCADE, to='core.transport', verbose_name='Транспортировка')),
            ],
            options={
                'verbose_name': 'Таблица распоряжения',
                'verbose_name_plural': 'Таблиции распоряжений',
                'ordering': ['date_of_created'],
            },
        ),
    ]
