from django import forms
from .models import *
from django_countries.widgets import CountrySelectWidget


class EdificioForm(forms.ModelForm):

    class Meta:
        model = Edificio
        fields = "__all__"


class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        exclude = ["edificio"]
        widgets = {
            "cant_adeudo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),
            "fecha_adeudo": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "placeholder": "Seleccione una fecha",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si el propietario viene en los datos iniciales, hacer el campo readonly
        if "initial" in kwargs and "propietario" in kwargs["initial"]:
            self.fields["propietario"].widget.attrs.update(
                {"readonly": "readonly", "class": "form-control bg-light"}
            )
            # También hacer el campo disabled para que no se envíe en el POST
            self.fields["propietario"].disabled = True

        self.fields["cant_adeudo"].required = False
        self.fields["fecha_adeudo"].required = False
        self.fields["numero_valla"].required = False

        if self.instance and self.instance.adeudo:
            self.fields["cant_adeudo"].required = True
            self.fields["fecha_adeudo"].required = True
        if self.instance and self.instance.valla:
            self.fields["numero_valla"].required = True

    def clean(self):
        cleaned_data = super().clean()
        adeudo = cleaned_data.get("adeudo")
        cant_adeudo = cleaned_data.get("cant_adeudo")
        fecha_adeudo = cleaned_data.get("fecha_adeudo")
        valla = cleaned_data.get("valla")
        numero_valla = cleaned_data.get("numero_valla")

        # Si hay adeudo, validar que tenga cantidad
        if adeudo:
            if cant_adeudo is None or cant_adeudo <= 0:
                self.add_error("cant_adeudo", "Debe especificar la cantidad del adeudo")
            if not fecha_adeudo:
                self.add_error("fecha_adeudo", "Debe especificar la fecha del adeudo")
        else:
            cleaned_data["cant_adeudo"] = None
            cleaned_data["fecha_adeudo"] = None

        if valla:
            if numero_valla is None or numero_valla < 1:
                self.add_error("numero_valla", "Debe especificar el número de la valla")
        else:
            cleaned_data["numero_valla"] = None
        return cleaned_data


class PropietarioForm(forms.ModelForm):

    class Meta:
        model = Propietario
        exclude = ["edificio"]
        widgets = {
            "nacionalidad": CountrySelectWidget(
                attrs={
                    "class": "form-select",
                    "data-placeholder": "Seleccione una nacionalidad",
                    "style": "width: 100%; height: 38px;",
                }
            )
        }
        labels = {
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "dni": "Documento de Identidad",
            "nacionalidad": "País de nacionalidad",
            "telefono": "Teléfono",
            "correo": "Correo electrónico",
            "observaciones": "Observaciones",
            "rep_nombre": "Nombre del representante",
            "rep_apellidos": "Apellidos del representante",
            "rep_dni": "DNI del representante",
            "rep_nacionalidad": "Nacionalidad del representante",
            "rep_email": "Email del representante",
            "rep_telefono": "Teléfono del representante",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar la etiqueta si lo deseas
        self.fields["rep_nombre"].required = False
        self.fields["rep_apellidos"].required = False
        self.fields["rep_dni"].required = False
        self.fields["rep_nacionalidad"].required = False
        self.fields["rep_email"].required = False
        self.fields["rep_telefono"].required = False
        self.fields["observaciones"].required = False

        if self.instance and self.instance.representante:
            self.fields["rep_nombre"].required = True
            self.fields["rep_apellidos"].required = True
            self.fields["rep_dni"].required = True
            self.fields["rep_nacionalidad"].required = True
            self.fields["rep_email"].required = True
            self.fields["rep_telefono"].required = True

    def clean(self):
        cleaned_data = super().clean()
        representante = cleaned_data.get("representante")
        rep_nombre = cleaned_data.get("rep_nombre")
        rep_apellidos = cleaned_data.get("rep_apellidos")
        rep_dni = cleaned_data.get("rep_dni")
        rep_nacionalidad = cleaned_data.get("rep_nacionalidad")
        rep_email = cleaned_data.get("rep_email")
        rep_telefono = cleaned_data.get("rep_telefono")

        if representante:
            if not rep_nombre:
                self.add_error(
                    "rep_nombre", "Debe especificar el nombre del representante"
                )
            if not rep_apellidos:
                self.add_error(
                    "rep_apellidos", "Debe especificar los apellidos del representante"
                )
            if not rep_dni:
                self.add_error("rep_dni", "Debe especificar el DNI del representante")
            if not rep_nacionalidad:
                self.add_error(
                    "rep_nacionalidad",
                    "Debe especificar la nacionalidad del representante",
                )
            if not rep_email:
                self.add_error(
                    "rep_email", "Debe especificar el email del representante"
                )
            if not rep_telefono:
                self.add_error(
                    "rep_telefono", "Debe especificar el teléfono del representante"
                )

        else:
            cleaned_data["rep_nombre"] = None
            cleaned_data["rep_apellidos"] = None
            cleaned_data["rep_dni"] = None
            cleaned_data["rep_nacionalidad"] = None
            cleaned_data["rep_email"] = None
            cleaned_data["rep_telefono"] = None

        return cleaned_data


class MovimientoBaseForm(forms.ModelForm):
    class Meta:
        fields = [
            "fecha",
            "tipo",
            "visa",
            "tipo_visa",
            "fecha_visa",
            "residente_inmobiliario",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "Seleccione fecha y hora",
                }
            ),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones opcionales...",
                }
            ),
            "fecha_visa": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "placeholder": "Seleccione una fecha",
                }
            ),
        }
        labels = {
            "fecha_visa": "Fecha de expedición de la visa",
            "tipo_visa": "Tipo de visa",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formatear la fecha para el input datetime-local
        if self.instance and self.instance.fecha:
            self.initial["fecha"] = self.instance.fecha.strftime("%Y-%m-%dT%H:%M")

        self.fields["tipo_visa"].required = False
        self.fields["fecha_visa"].required = False

        if self.instance and self.instance.visa:
            self.fields["tipo_visa"].required = True
            self.fields["fecha_visa"].required = True

        if self.instance and self.instance.residente_inmobiliario:
            self.fields["tipo_visa"].required = False
            self.fields["fecha_visa"].required = False

    def clean(self):
        cleaned_data = super().clean()
        visa = cleaned_data.get("visa")
        tipo_visa = cleaned_data.get("tipo_visa")
        fecha_visa = cleaned_data.get("fecha_visa")
        residente_inmobiliario = cleaned_data.get("residente_inmobiliario")

        if visa and residente_inmobiliario:
            self.add_error(
                "visa",
                "No puede seleccionar ambas opciones: 'Posee visa' y 'Residente Inmobiliario'.",
            )
            self.add_error(
                "residente_inmobiliario",
                "No puede seleccionar ambas opciones: 'Posee visa' y 'Residente Inmobiliario'.",
            )
        if visa:
            if not tipo_visa:
                self.add_error("tipo_visa", "Debe especificar el tipo de visa")
                cleaned_data["residente_inmobiliario"] = False
            if not fecha_visa:
                self.add_error(
                    "fecha_visa", "Debe especificar la fecha de expedicion de la visa"
                )
                cleaned_data["residente_inmobiliario"] = False
        else:
            cleaned_data["tipo_visa"] = None
            cleaned_data["fecha_visa"] = None

        if residente_inmobiliario:
            cleaned_data["tipo_visa"] = None
            cleaned_data["fecha_visa"] = None
            cleaned_data["visa"] = False

        return cleaned_data


class MovimientoPropietarioForm(MovimientoBaseForm):
    class Meta(MovimientoBaseForm.Meta):
        model = MovimientoPropietario


class MovimientoRapidoForm(forms.Form):
    TIPO_CHOICES = [
        ("entrada", "Registrar Entrada"),
        ("salida", "Registrar Salida"),
    ]

    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        initial=timezone.now,
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Observaciones opcionales",
            }
        ),
    )


class ArrendatarioForm(forms.ModelForm):

    class Meta:
        model = Arrendatario
        exclude = ["edificio"]
        widgets = {
            "nacionalidad": CountrySelectWidget(
                attrs={
                    "class": "form-select",
                    "data-placeholder": "Seleccione una nacionalidad",
                    "style": "width: 100%; height: 38px;",
                }
            ),
        }
        labels = {
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "dni": "Documento de Identidad",
            "nacionalidad": "País de nacionalidad",
            "telefono": "Teléfono",
            "correo": "Correo electrónico",
            "observaciones": "Observaciones",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar la etiqueta si lo deseas
        self.fields["observaciones"].required = False


class MovimientoArrendatarioForm(MovimientoBaseForm):
    class Meta(MovimientoBaseForm.Meta):
        model = MovimientoArrendatario


class ConvivienteForm(forms.ModelForm):

    class Meta:
        model = Conviviente
        exclude = ["edificio"]
        widgets = {
            "nacionalidad": CountrySelectWidget(
                attrs={
                    "class": "form-select",
                    "data-placeholder": "Seleccione una nacionalidad",
                    "style": "width: 100%; height: 38px;",
                }
            ),
        }
        labels = {
            "nombre": "Nombre",
            "apellidos": "Apellidos",
            "dni": "Documento de Identidad",
            "nacionalidad": "País de nacionalidad",
            "telefono": "Teléfono",
            "correo": "Correo electrónico",
            "observaciones": "Observaciones",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar la etiqueta si lo deseas
        self.fields["observaciones"].required = False


class MovimientoConvivienteForm(MovimientoBaseForm):
    class Meta(MovimientoBaseForm.Meta):
        model = MovimientoConviviente
