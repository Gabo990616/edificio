from django.db import models


class Edificio(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    cant_aptos = models.IntegerField()
    cant_bloques = models.IntegerField()
    cant_pisos = models.IntegerField()
    nombre_admin = models.CharField(max_length=50)
    piscina = models.BooleanField()

    def __str__(self):
        return self.nombre


VISA_TYPES = [
    (0, "Turista"),
    (1, "Familiar"),
    (2, "Periodista"),
    (3, "Estudiante"),
    (4, "Negocios"),
    (5, "Tratamiento medico"),
]


class Propietario(models.Model):

    nombre = models.CharField(max_length=50)
    dni = models.CharField(max_length=50, primary_key=True)
    nacionalidad = models.CharField(max_length=50)
    visa = models.IntegerField(choices=VISA_TYPES, default="0")
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)

    def __str__(self):
        return self.nombre


class Apartamento(models.Model):
    nombre = models.CharField(max_length=50)
    bloque = models.CharField(max_length=50)
    piso = models.CharField(max_length=50)
    cant_habitaciones = models.IntegerField()
    adeudo = models.BooleanField()
    valla = models.BooleanField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
