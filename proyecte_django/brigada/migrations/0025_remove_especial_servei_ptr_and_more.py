# Generated by Django 4.2.1 on 2023-05-08 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brigada', '0024_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especial',
            name='servei_ptr',
        ),
        migrations.RemoveField(
            model_name='mesvacances',
            name='treballadors',
        ),
        migrations.RemoveField(
            model_name='quotidia',
            name='servei_ptr',
        ),
        migrations.RemoveField(
            model_name='rol',
            name='servei',
        ),
        migrations.RemoveField(
            model_name='rol',
            name='treballador',
        ),
        migrations.RemoveField(
            model_name='servei',
            name='Dia',
        ),
        migrations.RemoveField(
            model_name='servei',
            name='treballadors',
        ),
        migrations.RemoveField(
            model_name='tipusdia',
            name='dia',
        ),
        migrations.RemoveField(
            model_name='tipusdia',
            name='treballador',
        ),
        migrations.DeleteModel(
            name='DiaTreball',
        ),
        migrations.DeleteModel(
            name='Especial',
        ),
        migrations.DeleteModel(
            name='MesVacances',
        ),
        migrations.DeleteModel(
            name='Quotidia',
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
        migrations.DeleteModel(
            name='Servei',
        ),
        migrations.DeleteModel(
            name='TipusDia',
        ),
        migrations.DeleteModel(
            name='Treballador',
        ),
    ]
