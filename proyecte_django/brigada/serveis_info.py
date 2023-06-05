from django.shortcuts import render
from .models import DiaTreball, Rol, Servei, Especial, Quotidia

from django import forms


class ServeiForm(forms.Form):
    dia = forms.DateField(label='Día', widget=forms.DateInput(attrs={'class': 'form-control', 'required': True}))
    Carrer = forms.CharField(label='Carrer', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Av. ...'}))
    Numero = forms.IntegerField(label='Numero', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '123 ...'}))
    Alt_Prof = forms.IntegerField(label='Altura / Profunditat', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '[0-7]'}))
    tipus_Servei = forms.ChoiceField(label='Tipus de servei', choices=[('Especial', 'Especial'), ('Quotidia', 'Quotidia')], widget=forms.Select(attrs={'class': 'form-control', 'required': True}))

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
         
      # Obtener la lista de trabajadores para mostrar en el formulario
      else:        
        carrer = request.POST.get('Carrer')
        numero = request.POST.get('Numero')
        dia = request.POST.get('dia')
        tipus_servei = request.POST.get('tipus_Servei')
        dia_treball, created = DiaTreball.objects.get_or_create(Dia=dia) 
        if tipus_servei == 'Especial':
            profunditat = request.POST.get('Alt/Prof')
            
            servei = Especial(Carrer=carrer, Numero=numero, Dia=dia_treball, profunditat=profunditat)
            servei.save()
        else:
            altura = request.POST.get('Alt/Prof')
            servei = Quotidia(Carrer=carrer, Numero=numero, Dia=dia_treball, altura=altura)
            servei.save()
            
   return render(request, 'Serveis/Serveis_list.html')
