from django.db import models
from django.core.validators import MinValueValidator
from django_countries.fields import CountryField
from django.utils import timezone
from datetime import date


VISA_TYPES = [
    (0, "C-2"),
    (1, "0-1"),
    (2, "D-2"),
    (3, "D-7"),
    (4, "D-10"),
    (5, "F-1"),
    (6, "A-7"),
    (7, "A-1"),
    (8, "A-2"),
    (9, "F-1"),
]


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
    ]

    fecha = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    residente_inmobiliario = models.BooleanField(default=False)
    visa = models.BooleanField(default=False)
    tipo_visa = models.IntegerField(
        choices=VISA_TYPES, default=0, blank=True, null=True
    )
    fecha_visa = models.DateField(blank=True, null=True)
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


class Propietario(models.Model):

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=50, primary_key=True)
    nacionalidad = CountryField(blank=False, default="CU")
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=100)
    representante = models.BooleanField(default=False)
    rep_nombre = models.CharField(max_length=50, blank=True, null=True)
    rep_apellidos = models.CharField(max_length=50, blank=True, null=True)
    rep_dni = models.CharField(max_length=50, blank=True, null=True)
    rep_nacionalidad = CountryField(blank=True, null=True, default="CU")
    rep_email = models.EmailField(max_length=50, blank=True, null=True)
    rep_telefono = models.CharField(max_length=50, blank=True, null=True)

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

    @property
    def tiene_movimientos(self):
        return self.movimientos.exists()

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
    cant_adeudo = models.FloatField(
        default=0, validators=[MinValueValidator(0.0)], blank=True, null=True
    )
    fecha_adeudo = models.DateField(blank=True, null=True)
    valla = models.BooleanField()
    numero_valla = models.IntegerField(
        validators=[MinValueValidator(1)], blank=True, null=True
    )
    mandato = models.BooleanField()
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    propietario = models.ForeignKey(
        Propietario, on_delete=models.CASCADE, related_name="apartamentos"
    )

    def __str__(self):
        return self.nombre


class Arrendatario(models.Model):

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=50, primary_key=True)
    nacionalidad = CountryField(blank=False)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    apartamento = models.ForeignKey(
        Apartamento, on_delete=models.CASCADE, related_name="arrendatarios"
    )
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

    @property
    def tiene_movimientos(self):
        return self.movimientos.exists()

    def registrar_movimiento(self, tipo, observaciones=None):
        """Método helper para registrar movimientos"""
        return MovimientoArrendatario.objects.create(
            arrendatario=self, tipo=tipo, observaciones=observaciones
        )


class MovimientoArrendatario(Movimiento):
    arrendatario = models.ForeignKey(
        "Arrendatario", on_delete=models.CASCADE, related_name="movimientos"
    )

    class Meta:
        verbose_name = "Movimiento de Arrendatario"
        verbose_name_plural = "Movimientos de Arrendatarios"

    def get_objeto_relacionado(self):
        return self.arrendatario.nombre


class Conviviente(models.Model):

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=50, primary_key=True)
    nacionalidad = CountryField(blank=False)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE)
    apartamento = models.ForeignKey(
        Apartamento, on_delete=models.CASCADE, related_name="convivientes"
    )
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

    @property
    def tiene_movimientos(self):
        return self.movimientos.exists()

    def registrar_movimiento(self, tipo, observaciones=None):
        """Método helper para registrar movimientos"""
        return MovimientoConviviente.objects.create(
            conviviente=self, tipo=tipo, observaciones=observaciones
        )


class MovimientoConviviente(Movimiento):
    conviviente = models.ForeignKey(
        "Conviviente", on_delete=models.CASCADE, related_name="movimientos"
    )

    class Meta:
        verbose_name = "Movimiento de Conviviente"
        verbose_name_plural = "Movimientos de Convivientes"

    def get_objeto_relacionado(self):
        return self.conviviente.nombre
