# Generated by Django 4.2.1 on 2023-05-13 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brigada', '0047_remove_especial_servei_ptr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaTreball',
            fields=[
                ('Dia', models.DateField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipus_rol', models.CharField(choices=[('Responsable', 'Responsable'), ('Asistent', 'Asistent'), ('Comunicador', 'Comunicador')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Servei',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Carrer', models.CharField()),
                ('Numero', models.IntegerField()),
                ('Dia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigada.diatreball')),
            ],
        ),
        migrations.CreateModel(
            name='Treballador',
            fields=[
                ('DNI', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=30)),
                ('Cognom', models.CharField(max_length=30)),
                ('Tlf', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Especial',
            fields=[
                ('servei_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='brigada.servei')),
                ('profunditat', models.IntegerField()),
            ],
            bases=('brigada.servei',),
        ),
        migrations.CreateModel(
            name='Quotidia',
            fields=[
                ('servei_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='brigada.servei')),
                ('altura', models.IntegerField()),
            ],
            bases=('brigada.servei',),
        ),
        migrations.CreateModel(
            name='TipusDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipus', models.CharField(choices=[('Treballant', 'Treballant'), ('Personal', 'Personal'), ('Indisposicio', 'Indisposicio')], max_length=20)),
                ('dia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigada.diatreball')),
                ('treballador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigada.treballador')),
            ],
        ),
        migrations.AddField(
            model_name='servei',
            name='treballadors',
            field=models.ManyToManyField(through='brigada.Rol', to='brigada.treballador'),
        ),
        migrations.AddField(
            model_name='rol',
            name='servei',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigada.servei'),
        ),
        migrations.AddField(
            model_name='rol',
            name='treballador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigada.treballador'),
        ),
        migrations.CreateModel(
            name='MesVacances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Any', models.IntegerField()),
                ('Mes', models.CharField(choices=[('Juliol', 'Juliol'), ('Agost', 'Agost'), ('Septembre', 'Septembre')], max_length=20)),
                ('treballadors', models.ManyToManyField(to='brigada.treballador')),
            ],
        ),
        migrations.AddField(
            model_name='diatreball',
            name='treballadors',
            field=models.ManyToManyField(through='brigada.TipusDia', to='brigada.treballador'),
        ),
        migrations.AddConstraint(
            model_name='tipusdia',
            constraint=models.UniqueConstraint(fields=('treballador', 'dia'), name='unique_TipusDia'),
        ),
        migrations.AddConstraint(
            model_name='servei',
            constraint=models.UniqueConstraint(fields=('Carrer', 'Numero', 'Dia'), name='unique_Servei'),
        ),
        migrations.AddConstraint(
            model_name='rol',
            constraint=models.UniqueConstraint(fields=('servei', 'treballador'), name='unique_Rol'),
        ),
        migrations.AddConstraint(
            model_name='mesvacances',
            constraint=models.UniqueConstraint(fields=('Any', 'Mes'), name='unique_MesVacances'),
        ),
    ]
