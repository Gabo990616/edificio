from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
    ]

    fecha = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.get_objeto_relacionado()} - {self.tipo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

    def get_objeto_relacionado(self):
        """Método abstracto que debe ser implementado por las clases hijas"""
        raise NotImplementedError("Las subclases deben implementar este método")


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
    observaciones = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    @property
    def ultima_entrada(self):
        return self.movimientos.filter(tipo="entrada").order_by("-fecha").first()

    @property
    def ultima_salida(self):
        return self.movimientos.filter(tipo="salida").order_by("-fecha").first()

    @property
    def esta_en_propiedad(self):
        ultima_entrada = self.ultima_entrada
        ultima_salida = self.ultima_salida

        if not ultima_entrada:
            return False
        if not ultima_salida:
            return True
        return ultima_entrada.fecha > ultima_salida.fecha

    def registrar_movimiento(self, tipo, observaciones=None):
        """Método helper para registrar movimientos"""
        return MovimientoPropietario.objects.create(
            propietario=self, tipo=tipo, observaciones=observaciones
        )


class MovimientoPropietario(Movimiento):
    propietario = models.ForeignKey(
        "Propietario", on_delete=models.CASCADE, related_name="movimientos"
    )

    class Meta:
        verbose_name = "Movimiento de Propietario"
        verbose_name_plural = "Movimientos de Propietarios"

    def get_objeto_relacionado(self):
        return self.propietario.nombre


class Apartamento(models.Model):
    nombre = models.CharField(max_length=50)
    bloque = models.CharField(max_length=50)
    piso = models.CharField(max_length=50)
    cant_habitaciones = models.IntegerField()
    adeudo = models.BooleanField()
    cant_adeudo = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    fecha_adeudo = models.DateField()
    valla = models.BooleanField()
    numero_valla = models.IntegerField()
    mandato = models.BooleanField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
