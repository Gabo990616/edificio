from django import forms
from .models import *


class EdificioForm(forms.ModelForm):

    class Meta:
        model = Edificio
        fields = "__all__"


class ApartamentoForm(forms.ModelForm):

    class Meta:
        model = Apartamento
        fields = "__all__"


class PropietarioForm(forms.ModelForm):

    class Meta:
        model = Propietario
        fields = "__all__"


class MovimientoBaseForm(forms.ModelForm):
    class Meta:
        fields = ["fecha", "tipo", "observaciones"]
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formatear la fecha para el input datetime-local
        if self.instance and self.instance.fecha:
            self.initial["fecha"] = self.instance.fecha.strftime("%Y-%m-%dT%H:%M")


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
