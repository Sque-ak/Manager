# Generated by Django 3.1 on 2020-11-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railwayplatform', '0004_auto_20201130_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='railwayorder',
            name='type_railwayorder',
            field=models.CharField(blank=True, choices=[('s', 'Отправка'), ('r', 'Приемка')], default='r', max_length=16, verbose_name='Тип документа'),
        ),
    ]