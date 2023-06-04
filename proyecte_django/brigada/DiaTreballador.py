from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import TipusDia, Treballador, DiaTreball

def asignar_tipus_dia(request):
    if request.method == 'POST':
        if 'dia_info' in request.POST:
            # Obtener el día seleccionado
            dia = request.POST['dia_info']
            
            # Obtener los tipos de día para el día seleccionado
            tipus_dia = TipusDia.objects.filter(dia__Dia=dia)
            
            # Obtener la lista de trabajadores para mostrar en el formulario
            treballadors = Treballador.objects.all()
            
            context = {'treballadors_dia': treballadors, 'dia_dia': dia, 'tipus_dia': tipus_dia}
            return render(request, 'Dias/Añadir_Dia_Treballador.html', context)
        else:
            # Obtener los datos del formulario
            dia = request.POST['dia']
            treballadors = request.POST.getlist('treballadors[]')
            tipus_dia = request.POST['tipus_dia']
             
            try:
                # Intentar crear el objeto DiaTreball
                dia_treball, created = DiaTreball.objects.get_or_create(Dia=dia)
                
                # Crear los roles para los trabajadores seleccionados
                for treballador_dni in treballadors:
                    treballador = Treballador.objects.get(DNI=treballador_dni)
                    TipusDia.objects.create(treballador=treballador, dia=dia_treball, tipus=tipus_dia)
                
                return redirect('diatreball')
            except IntegrityError:
                # Manejar el caso de duplicados
                # Aquí puedes mostrar un mensaje de error o realizar otra acción apropiada
                pass
        
    # Obtener la lista de trabajadores para mostrar en el formulario
    treballadors = Treballador.objects.all()
    context = {'treballadors': treballadors}
    return render(request, 'Dias/Añadir_Dia_Treballador.html', context)
