#Este archivo sirve para que los administradores puedan agregar,
# editar o eliminar vehículos fácilmente con formularios automáticos de Django
from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "name",
            "category",
            "year",
            "engine",
            "power",
            "transmission",
            "fuel",
            "price",
            "availability",
            "specs",
            "image",
            ]