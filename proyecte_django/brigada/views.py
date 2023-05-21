from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import Servei, Treballador, Especial, Quotidia
from django.http import HttpResponse
from django.core.exceptions import BadRequest

def index(request):
    return render(
        request,
        'index.html',
        context={ 'num_Treballadors': Treballador.objects.all().count(),
        'num_Serveis': Servei.objects.all().count(),
        'num_Quotidia': Quotidia.objects.all().count() ,
        'num_Especial': Especial.objects.all().count()}
    )