from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views, treballadors, DiaTreballador, serveis_info

urlpatterns = [
    path('', views.index, name='index'),
    
    #Treballadors
    path(r'treballadors', treballadors.lista_trabajadores, name="treballadors"),
    path(r'treballadors/<str:dni>/', treballadors.treballador_info, name='treballador_info'),
    path(r'treballador/<str:dni>/actualizar-telefono/', treballadors.actualizar_telefono, name='actualizar_telefono'),
    path(r'treballador/<str:dni>/afegir-mes/', treballadors.mes_vacances, name='afegir_mes'),

    #DiasTreball
    path(r'diatreball', DiaTreballador.asignar_tipus_dia, name="diatreball"),

    #Serveis
    path(r'serveis', serveis_info.lista_serveis, name="serveis"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
