from django.shortcuts import render
from .models import Treballador, Rol
from django.db.models import Count

def lista_trabajadores(request):
    # Obtener todos los trabajadores con la cantidad de roles que tienen
    trabajadores = Treballador.objects.annotate(cantidad_roles=Count('rol'))

    context = {
        'trabajadores': trabajadores
    }

    return render(request, 'Treballador/Treballador_list.html', context)
