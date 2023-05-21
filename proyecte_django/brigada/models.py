from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Treballador(models.Model):
    DNI = models.CharField(primary_key=True ,max_length=9)
    Nom = models.CharField(max_length=30)
    Cognom = models.CharField(max_length=30)
    Tlf = models.CharField()
    
    
    def __str__(self):
        return '{} , {} , {} , {} , {} , {}'.format(self.DNI, self.Nom, self.Cognom, self.Tlf)

class MesVacances(models.Model):
    JULIOL = 'Juliol'
    AGOST = 'Agost' 
    SEPTEMBRE = 'Septembre'
    TIPUS_CHOICES = [
        (JULIOL, 'Juliol'),
        (AGOST, 'Agost'),
        (SEPTEMBRE, 'Septembre'),
    ]
    Any = models.IntegerField()
    Mes = models.CharField(max_length=20, choices=TIPUS_CHOICES)
    treballadors = models.ManyToManyField('Treballador')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Any', 'Mes'], name='unique_MesVacances'
            )
        ]
    
    def __str__(self):
        return 'Any: {}, Mes: {}'.format(self.Any, self.Mes)

class DiaTreball(models.Model):
    Dia = models.DateField(primary_key=True)
    treballadors = models.ManyToManyField('Treballador', through='TipusDia')
    
    def __str__(self):
        return 'Dia: {}'.format(self.Dia)

class TipusDia(models.Model):
    TREBALLANT = 'Treballant'
    PERSONAL = 'Personal'
    INDISPOSICIO = 'Indisposicio'
    TIPUS_CHOICES = [
        (TREBALLANT, 'Treballant'),
        (PERSONAL, 'Personal'),
        (INDISPOSICIO, 'Indisposicio'),
    ]
    treballador = models.ForeignKey(Treballador, on_delete=models.CASCADE)
    dia = models.ForeignKey(DiaTreball, on_delete=models.CASCADE)
    tipus = models.CharField(max_length=20, choices=TIPUS_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['treballador', 'dia'], name='unique_TipusDia'
            )
        ]

    def __str__(self):
        return 'Tipus: {} , Treballador: {} , Dia: {}'.format(self.tipus, self.treballador, self.dia)


class Servei(models.Model):
    Carrer = models.CharField()
    Numero = models.IntegerField()
    Dia = models.ForeignKey(DiaTreball, on_delete=models.CASCADE)
    treballadors = models.ManyToManyField(Treballador, through='Rol')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['Carrer', 'Numero', 'Dia'], name='unique_Servei'
            )
        ]

    def __str__(self):
        return 'Carrer: {} , Numero: {} , Dia: {}'.format(self.Carrer, self.Numero, self.Dia)
    
class Rol(models.Model):
    RESPONSABLE = 'Responsable'
    ASISTENT = 'Asistent'
    COMUNICADOR = 'Comunicador'
    TIPUS_CHOICES = [
        (RESPONSABLE, 'Responsable'),
        (ASISTENT, 'Asistent'),
        (COMUNICADOR, 'Comunicador'),
    ]
    servei = models.ForeignKey(Servei, on_delete=models.CASCADE)
    treballador = models.ForeignKey(Treballador, on_delete=models.CASCADE)
    tipus_rol = models.CharField(max_length=20, choices=TIPUS_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['servei', 'treballador'], name='unique_Rol'
            )
        ]

    def save(self, *args, **kwargs):
        # Verificar que un Servei te minim 3 treballadors
        if self.servei.treballadors.count() >= 3:
            super(Rol, self).save(*args, **kwargs)
        else:
            raise ValueError('El servei ha de tenir al menys 3 treballadors.')
        
    def __str__(self):
        return 'Servei: {} , Treballador: {}'.format(self.servei, self.treballador)
    
class Especial(Servei):
    profunditat = models.IntegerField()

    def clean(self):
        if self.profunditat < 1 or self.profunditat > 4:
            raise ValidationError("La profunditat ha d'estar entre 1 y 4.")

    def __str__(self):
        return 'Carrer: {} , Numero: {} , Dia: {} , Profunditat: {}'.format(self.Carrer, self.Numero, self.Dia, self.profunditat)
    
class Quotidia(Servei):
    altura = models.IntegerField()

    def clean(self):
        if self.altura < 1 or self.altura > 7:
            raise ValidationError("L'altura ha d'estar entre 1 y 7.")

    def __str__(self):
        return 'Carrer: {} , Numero: {} , Dia: {} , Profunditat: {}'.format(self.Carrer, self.Numero, self.Dia, self.altura)

