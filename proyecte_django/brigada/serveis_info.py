from django.shortcuts import render
from .models import DiaTreball, Rol, Servei, Especial, Quotidia, TipusDia, Treballador

from django import forms


# class ServeiForm(forms.Form):
#     dia = forms.DateField(label='Día', widget=forms.DateInput(attrs={'class': 'form-control', 'required': True}))
#     Carrer = forms.CharField(label='Carrer', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Av. ...'}))
#     Numero = forms.IntegerField(label='Numero', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '123 ...'}))
#     Alt_Prof = forms.IntegerField(label='Altura / Profunditat', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '[0-7]'}))
#     tipus_Servei = forms.ChoiceField(label='Tipus de servei', choices=[('Especial', 'Especial'), ('Quotidia', 'Quotidia')], widget=forms.Select(attrs={'class': 'form-control', 'required': True}))

def lista_serveis(request):
    if request.method == 'POST':
            print('POST')
            print(request.POST)
            if 'dia_servei' in request.POST:
                print('dia_servei')
                # Obtener el día seleccionado
                dia = request.POST['dia_servei']
                if dia:
                    # Obtener los tipos de día para el día seleccionado
                    servei_dia = Servei.objects.filter(Dia__Dia=dia)
                    roles = Rol.objects.filter(servei__in=servei_dia)
                    especial = Especial.objects.filter(servei_ptr_id__in=servei_dia)
                    quotidia = Quotidia.objects.filter(servei_ptr_id__in=servei_dia)

                    treballadors_dia = TipusDia.objects.filter(tipus='Treballant', dia=dia)
                    treballadors_list = []
                    for treballador in treballadors_dia:
                        treballadors_list.append(treballador.treballador)

                    context = {'dia_servei': dia, 'serveis_dia': servei_dia, 'roles': roles, 'especial': especial, 'quotidia': quotidia, 'treballadors_list': treballadors_list}

                    return render(request, 'Serveis/Serveis_list.html', context)
            
        # Obtener la lista de trabajadores para mostrar en el formulario
            elif 'trabajador' in request.POST:
                treballadors_escollits = request.POST.getlist('trabajador')
                servei = request.POST.get('servei')
                servei_escollit = Servei.objects.get(id=servei)
                for treballador in treballadors_escollits:
                    tipus_rol_escollit = request.POST.get('tipus_dia_' + treballador)
                    treballador_escollit = Treballador.objects.get(DNI=treballador)
                    print(tipus_rol_escollit)
                    print(treballador_escollit)
                    print(servei_escollit)
                    rol = Rol(treballador=treballador_escollit, servei=servei_escollit, tipus_rol=tipus_rol_escollit)
                    rol.save()                    

            else:     
                print('servei_form')   
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
