import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecte_django.settings')
django.setup()

from faker import Faker
from random import randint, sample
import random
from datetime import datetime, timedelta
from collections import defaultdict
from brigada.models import Treballador, MesVacances, DiaTreball, TipusDia, Servei, Rol, Especial, Quotidia

fake = Faker('es_ES')

letras='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

print("Introduciendo trabajadores...")
# Crea 50 trabajadores
for i in range(50):
    id = randint(10000000,99999999)
    id = str(id) + random.choice(letras)
    DNI = id
    Nom = fake.first_name()
    Cognom = fake.last_name()
    Tlf = fake.unique.phone_number()
    treballador = Treballador(DNI=DNI, Nom=Nom, Cognom=Cognom, Tlf=Tlf)
    treballador.save()

print("Introduciendo Meses de vacaciones...")
# Crea 10 MesVacances
anys = list(range(2022, 2030))
mesos = ['Juliol', 'Agost', 'Septembre']
for any in anys:
    for mes in mesos:
        mes_vacances = MesVacances(Any=any, Mes=mes)
        mes_vacances.save()


print("Asignando meses de vacaciones a los trabajadores...")

#Recorre todos los años
for any in range(2022, 2030):
    for treballador in Treballador.objects.all():
        mes = random.choices(mesos)
        # Asigna el mes al trabajador
        mes_vacances = MesVacances.objects.get(Any=any, Mes=''.join(mes))
        mes_vacances.treballadors.add(treballador)
 #asignar treballadors als mesos

print("Introduciendo dias de trabajo...")
# Crea 365 dias treballables a partir del 1 de gener de 2022
data = datetime.strptime('2023-01-01', '%Y-%m-%d')
for i in range(365):
    dia = DiaTreball(Dia=data.date())
    dia.save()
    data += timedelta(days=1)

print("Introduciendo creando tipus dia para los trabajadores...")

# Crea TipusDia per cada Treballador 
treballadors = Treballador.objects.all()
dies = DiaTreball.objects.all()
tipus = ['Treballant', 'Personal', 'Indisposicio']

for dia in dies:
    treballadors_disponibles = []
    # Selecciona los trabajadores que no están en MesVacances
    mes_catala = ""
    if dia.Dia.strftime('%B') == "July":
        mes_catala = "Juliol"
    elif dia.Dia.strftime('%B') == "August":
        mes_catala = "Agost"
    elif dia.Dia.strftime('%B') == "September":
        mes_catala = "Septembre"
    for treballador in treballadors:
        if not dia.Dia.strftime('%B') == "July" or not dia.Dia.strftime('%B') == "August" or not dia.Dia.strftime('%B') == "September":
            if not MesVacances.objects.filter(Any=dia.Dia.year, Mes=mes_catala, treballadors=treballador).exists():
                treballadors_disponibles.append(treballador)
    # Asigna entre 3 y 7 trabajadores al azar al día
    treballadors_assignats = sample(treballadors_disponibles, randint(3,7))
    # Asegura que haya al menos 3 TipusDia con el tipo "Treballant" para cada día
    num_treballants_assignats = 0
    for treballador in treballadors_assignats:
        if num_treballants_assignats < 3:
            tipus_dia = TipusDia(treballador=treballador, dia=dia, tipus="Treballant")
            num_treballants_assignats += 1
        else:
            tipus_dia = TipusDia(treballador=treballador, dia=dia, tipus=tipus[randint(0,2)])
        tipus_dia.save()


print("Introduciendo servicios")
        
# for day in dies:
#     rand = random.randint(0, 5)
#     for i in range(rand):
#         carrer = fake.street_name()
#         numero = random.randint(1, 100)
#         dia = day
#         tipus_servei = random.choice([Especial, Quotidia])
#         if tipus_servei == Especial:
#             profunditat = random.randint(1, 4)
#             servei = Especial(Carrer=carrer, Numero=numero, Dia=dia, profunditat=profunditat)
#             servei.save()
#         else:
#             altura = random.randint(1, 7)
#             servei = Quotidia(Carrer=carrer, Numero=numero, Dia=dia, altura=altura)
#             servei.save()
        
#         treballadors_disponibles = []
#         # Selecciona los trabajadores que no están en MesVacances y tienen el tipo "Treballant"
#         for treballador in treballadors:
#             if not MesVacances.objects.filter(Any=dia.Dia.year, Mes=dia.Dia.strftime('%B'), treballadors=treballador).exists():
#                 tipus_dia = TipusDia.objects.filter(treballador=treballador, dia=dia, tipus='Treballant').exists()
#                 if tipus_dia:
#                     treballadors_disponibles.append(treballador)
#         # Asigna entre 3 y 5 trabajadores al azar al día
#         num_treballadors = random.randint(3, 5)

#         if len(treballadors_disponibles) >= num_treballadors and num_treballadors > 0:
#             servei.treballadors.set(random.sample(treballadors_disponibles, num_treballadors))
#         else: 
#             servei.delete()

for day in dies:
    treballadors_disponibles = []
    # Selecciona los trabajadores que no están en MesVacances y tienen el tipo "Treballant"
    for treballador in treballadors:
        if not MesVacances.objects.filter(Any=day.Dia.year, Mes=day.Dia.strftime('%B'), treballadors=treballador).exists():
            tipus_dia = TipusDia.objects.filter(treballador=treballador, dia=day, tipus='Treballant').exists()
            if tipus_dia:
                treballadors_disponibles.append(treballador)
    rand = random.randint(0, 5)
    for i in range(rand):
        carrer = fake.street_name()
        numero = random.randint(1, 100)
        dia = day
        tipus_servei = random.choice([Especial, Quotidia])
        if tipus_servei == Especial:
            profunditat = random.randint(1, 4)
            servei = Especial(Carrer=carrer, Numero=numero, Dia=dia, profunditat=profunditat)
            servei.save()
        else:
            altura = random.randint(1, 7)
            servei = Quotidia(Carrer=carrer, Numero=numero, Dia=dia, altura=altura)
            servei.save()
        
        # Asigna entre 3 y 5 trabajadores al azar al día
        num_treballadors = random.randint(3, 5)

        if len(treballadors_disponibles) >= num_treballadors and num_treballadors > 0:
            servei.treballadors.set(random.sample(treballadors_disponibles, num_treballadors))
        elif  len(treballadors_disponibles) == 3 and num_treballadors > 0:
            servei.treballadors.set(random.sample(treballadors_disponibles, 3))
        else: 
            servei.delete()


print("Introduciendo roles en los servicios a trabajadores...")
# Asignar roles aleatorios a los trabajadores en los Servicios
serveis = Servei.objects.all()
tipus_rol = [Rol.RESPONSABLE, Rol.ASISTENT, Rol.COMUNICADOR]
for servei in serveis:
    treballadors = list(servei.treballadors.all())
    for i, treballador in enumerate(treballadors):
        if i == 0:
            tipus = Rol.RESPONSABLE
        elif i == 1:
            tipus = Rol.COMUNICADOR
        else:
            tipus = Rol.ASISTENT
        rol_existente = Rol.objects.get(servei=servei, treballador=treballador)
        rol_existente.tipus_rol = tipus
        rol_existente.save()


