from django import forms
from django.shortcuts import render
from .models import MesVacances, Treballador, Rol
from django.db.models import Count
from django.shortcuts import redirect
from django.db.models import Q

def lista_trabajadores(request):
    query = request.GET.get('q')
    trabajadores = Treballador.objects.annotate(cantidad_roles=Count('rol'))

    if query:
        trabajadores = trabajadores.filter(Q(Nom__icontains=query) | Q(Cognom__icontains=query))

    context = {
        'trabajadores': trabajadores,
        'query': query
    }

    return render(request, 'Treballador/Treballador_list.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Treballador

def treballador_info(request, dni):
    # Obtener el trabajador utilizando el DNI proporcionado
    trabajador = get_object_or_404(Treballador, DNI=dni)

    cantidad_especiales = Rol.objects.filter(treballador=trabajador, servei__especial__isnull=False).count()
    cantidad_quotidians = Rol.objects.filter(treballador=trabajador, servei__quotidia__isnull=False).count()
    ultimos_meses_vacaciones = MesVacances.objects.filter(treballadors=trabajador).order_by('Any', 'Mes')[4:]


    context = {
        'trabajador': trabajador,
        'especials': cantidad_especiales,
        'quotidians': cantidad_quotidians,
        'mes_vacances': ultimos_meses_vacaciones
    }

    return render(request, 'Treballador/Treballador_info.html', context)



def actualizar_telefono(request, dni):
    trabajador = get_object_or_404(Treballador, DNI=dni)

    if request.method == 'POST':
        if 'Tlf' in request.POST:
            trabajador.Tlf = request.POST['Tlf']
            trabajador.save()
            return redirect('treballador_info', dni=dni)

    return redirect('treballador_info', dni=dni)

def mes_vacances(request, dni):
    trabajador = get_object_or_404(Treballador, DNI=dni)

    if request.method == 'POST':
        if 'any' in request.POST:
            any = request.POST['any']
            mes = request.POST['mes']
            mes_vacaciones, created = MesVacances.objects.get_or_create(Any=any, Mes=mes)
            mes_vacaciones.treballadors.set([trabajador])

            return redirect('treballador_info', dni=dni)

    return redirect('treballador_info', dni=dni)
