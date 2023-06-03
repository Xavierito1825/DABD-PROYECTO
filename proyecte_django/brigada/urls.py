from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views, treballadors, DiaTreballador

urlpatterns = [
    path('', views.index, name='index'),
    
    #Treballadors
    path(r'treballadors', treballadors.lista_trabajadores, name="treballadors"),
    path(r'treballadors/<str:dni>/', treballadors.treballador_info, name='treballador_info'),

    #DiasTreball
    path(r'diatreball', DiaTreballador.asignar_tipus_dia, name="diatreball"),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
