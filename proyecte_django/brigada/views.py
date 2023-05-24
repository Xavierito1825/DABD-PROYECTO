from django.shortcuts import render
from .models import Servei, Treballador, Especial, Quotidia
from django.db.models import Count
import json
from datetime import date, timedelta

def date_serializer(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')

def index(request):
    # Obtener la fecha actual
    today = date.today()

    # Calcular la fecha de inicio hace 30 días
    start_date = today - timedelta(days=29)

    # Obtener los datos necesarios de tu modelo para los últimos 30 días
    serveis_por_dia = Servei.objects.filter(Dia__gte=start_date, Dia__lte=today).values('Dia').annotate(total=Count('Dia'))

    # Crear una lista de todos los días en el rango
    dias = [start_date + timedelta(days=i) for i in range(30)]

    # Inicializar la lista de cantidades con ceros
    cantidades = [0] * 30

    # Actualizar las cantidades correspondientes a los días con servicios
    for servei in serveis_por_dia:
        dia = servei['Dia']
        index = (dia - start_date).days
        cantidades[index] = servei['total']

    context = {
        'num_Treballadors': Treballador.objects.all().count(),
        'num_Serveis': Servei.objects.all().count(),
        'num_Quotidia': Quotidia.objects.all().count(),
        'num_Especial': Especial.objects.all().count(),
        'dias': json.dumps(dias, default=date_serializer),
        'cantidades': json.dumps(cantidades),
    }

    return render(request, 'index.html', context)
