from django.shortcuts import render
from .models import Rol, Servei, Especial, Quotidia

def lista_serveis(request):
   if request.method == 'POST':
      if 'dia_servei' in request.POST:
         # Obtener el día seleccionado
         dia = request.POST['dia_servei']
         if dia:
               # Obtener los tipos de día para el día seleccionado
               servei_dia = Servei.objects.filter(Dia__Dia=dia)
               roles = Rol.objects.filter(servei__in=servei_dia)
               especial = Especial.objects.filter(servei_ptr_id__in=servei_dia)
               quotidia = Quotidia.objects.filter(servei_ptr_id__in=servei_dia)


               context = {'dia_servei': dia, 'serveis_dia': servei_dia, 'roles': roles, 'especial': especial, 'quotidia': quotidia}
               return render(request, 'Serveis/Serveis_list.html', context)

   return render(request, 'Serveis/Serveis_list.html')
