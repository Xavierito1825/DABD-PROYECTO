from django.shortcuts import render
from .models import Treballador, Rol
from django.db.models import Count
from django.shortcuts import redirect

def lista_trabajadores(request):
    # Obtener todos los trabajadores con la cantidad de roles que tienen
    trabajadores = Treballador.objects.annotate(cantidad_roles=Count('rol'))

    context = {
        'trabajadores': trabajadores
    }

    return render(request, 'Treballador/Treballador_list.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Treballador

def treballador_info(request, dni):
    # Obtener el trabajador utilizando el DNI proporcionado
    trabajador = get_object_or_404(Treballador, DNI=dni)

    cantidad_especiales = Rol.objects.filter(treballador=trabajador, servei__especial__isnull=False).count()
    cantidad_quotidians = Rol.objects.filter(treballador=trabajador, servei__quotidia__isnull=False).count()

    context = {
        'trabajador': trabajador,
        'especials': cantidad_especiales,
        'quotidians': cantidad_quotidians
    }

    return render(request, 'Treballador/Treballador_info.html', context)



def actualizar_telefono(request, dni):
    trabajador = get_object_or_404(Treballador, DNI=dni)

    if request.method == 'POST':
        trabajador.Tlf = request.POST['Tlf']
        trabajador.save()
        return redirect('treballador_info', dni=dni)

    return redirect('treballador_info', dni=dni)

