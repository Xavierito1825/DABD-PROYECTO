from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import TipusDia, Treballador, DiaTreball

def asignar_tipus_dia(request):
    treballadors = Treballador.objects.all()
    context = {'treballadors': treballadors}
    if request.method == 'POST':
        if 'dia_info' in request.POST:
            # Obtener el día seleccionado
            dia = request.POST['dia_info']
            if dia:
                # Obtener los tipos de día para el día seleccionado
                tipus_dia = TipusDia.objects.filter(dia__Dia=dia)
                
                # Obtener la lista de trabajadores para mostrar en el formulario
                treballadors_dia = Treballador.objects.all()
                context = {'treballadors': treballadors, 'treballadors_dia': treballadors_dia, 'dia_dia': dia, 'tipus_dia': tipus_dia}
                return render(request, 'Dias/Añadir_Dia_Treballador.html', context)

        elif 'tipus_dia' in request.POST:
            # Obtener los datos del formulario
            dia = request.POST['dia']
            treballadors_envia = request.POST.getlist('treballadors[]')
            tipus_dia = request.POST['tipus_dia']
             
            try:
                # Intentar crear el objeto DiaTreball
                dia_treball, created = DiaTreball.objects.get_or_create(Dia=dia)
                
                # Crear los roles para los trabajadores seleccionados
                for treballador_dni in treballadors_envia:
                    treballador = Treballador.objects.get(DNI=treballador_dni)
                    TipusDia.objects.create(treballador=treballador, dia=dia_treball, tipus=tipus_dia)
                
                return redirect('diatreball')
            except IntegrityError:
                # Manejar el caso de duplicados
                # Aquí puedes mostrar un mensaje de error o realizar otra acción apropiada
                pass
        else:
            dia_str = request.POST['dia']
            fecha_str = dia_str.split(":")[1].strip()

            treballador = request.POST['treballador']
            valores = treballador.split(",")  # Dividir la cadena por las comas
            dni = valores[0].strip()

            dia_treball = DiaTreball.objects.get(Dia=fecha_str)
            treballador = Treballador.objects.get(DNI=dni)
            elimina_tipus = TipusDia.objects.get(treballador=treballador, dia=fecha_str)
            elimina_tipus.delete()
        
    # Obtener la lista de trabajadores para mostrar en el formulario
    
    return render(request, 'Dias/Añadir_Dia_Treballador.html', context)
