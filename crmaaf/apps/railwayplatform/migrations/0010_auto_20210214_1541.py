# Generated by Django 3.0.8 on 2021-02-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railwayplatform', '0009_auto_20210110_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='railwayorder',
            name='type_railwayorder',
            field=models.CharField(blank=True, choices=[('s', 'В пути'), ('p', 'Готовится к отправке'), ('r', 'Прибыл')], default='p', max_length=16, verbose_name='Тип документа'),
        ),
    ]
