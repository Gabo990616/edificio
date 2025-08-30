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
