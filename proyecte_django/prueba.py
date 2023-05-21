import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecte_django.settings')
django.setup()

from faker import Faker
from random import randint, sample
import random
from datetime import timedelta
from collections import defaultdict
from brigada.models import Treballador, MesVacances, DiaTreball, TipusDia, Servei, Rol, Especial, Quotidia

fake = Faker('es_ES')
treballadors = Treballador.objects.all()
treballadors = Treballador.objects.all()
serveis = []

# Crear servicios
while len(serveis) < 400:
    carrer = fake.street_name()
    numero = random.randint(1, 100)
    dia = random.choice(DiaTreball.objects.all())
    tipus_servei = random.choice([Especial, Quotidia])
    if tipus_servei == Especial:
        profunditat = random.randint(1, 4)
        servei = Especial(Carrer=carrer, Numero=numero, Dia=dia, profunditat=profunditat)
    else:
        altura = random.randint(1, 7)
        servei = Quotidia(Carrer=carrer, Numero=numero, Dia=dia, altura=altura)

    # Seleccionar trabajadores disponibles
    treballadors_disponibles = Treballador.objects.filter(
        tipusdia__dia=dia,
        tipusdia__tipus='Treballant',
    ).exclude(
        mesvacances__any=dia.Dia.year,
        mesvacances__mes=dia.Dia.strftime('%B'),
    ).distinct()

    # Asignar trabajadores al azar
    num_treballadors = random.randint(3, 5)
    if len(treballadors_disponibles) >= num_treballadors and num_treballadors > 0:
        servei.treballadors.set(random.sample(list(treballadors_disponibles), num_treballadors))
        serveis.append(servei)

# Guardar servicios en la base de datos
Especial.objects.bulk_create([s for s in serveis if isinstance(s, Especial)])
Quotidia.objects.bulk_create([s for s in serveis if isinstance(s, Quotidia)])


# dies = DiaTreball.objects.all()
# tipus = ['Treballant', 'Personal', 'Indisposicio']

# for dia in dies:
#     treballadors_disponibles = []
#     # Selecciona los trabajadores que no están en MesVacances
#     print(dia.Dia.year)
#     print(dia.Dia.strftime('%B'))
#     mes_catala = ""
#     if dia.Dia.strftime('%B') == "July":
#         mes_catala = "Juliol"
#     elif dia.Dia.strftime('%B') == "August":
#         mes_catala = "Agost"
#     elif dia.Dia.strftime('%B') == "September":
#         mes_catala = "Septembre"
#     for treballador in treballadors:
#         if not dia.Dia.strftime('%B') == "July" or not dia.Dia.strftime('%B') == "August" or not dia.Dia.strftime('%B') == "September":
#             if not MesVacances.objects.filter(Any=dia.Dia.year, Mes=mes_catala, treballadors=treballador).exists():
#                 treballadors_disponibles.append(treballador)
#                 #print(treballador.Nom)
#             else:
#                 print("nooo "+treballador.Nom)
#     # Asigna entre 3 y 8 trabajadores al azar al día
#     treballadors_assignats = sample(treballadors_disponibles, randint(3,5))
#     # Asegura que haya al menos 3 TipusDia con el tipo "Treballant" para cada día
#     num_treballants_assignats = 0
#     for treballador in treballadors_assignats:
#         if num_treballants_assignats < 3:
#             tipus_dia = TipusDia(treballador=treballador, dia=dia, tipus="Treballant")
#             num_treballants_assignats += 1
#         else:
#             tipus_dia = TipusDia(treballador=treballador, dia=dia, tipus=tipus[randint(1,2)])
#         # tipus_dia.save()
#         # print("------")
#         # print(tipus_dia.treballador.Nom)
#         # print(tipus_dia.dia)
#         # print(tipus_dia.tipus)
#         # print("------")

