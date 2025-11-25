from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'

        labels = {
            'name': 'Nombre del vehículo',
            'category': 'Categoría',
            'year': 'Año',
            'engine': 'Motor',
            'power': 'Potencia',
            'transmission': 'Transmisión',
            'fuel': 'Combustible',
            'price': 'Precio por día',
            'availability': 'Disponibilidad',
            'specs': 'Especificaciones',
            'image': 'Imagen del vehículo',
        }

        widgets = {
            'specs': forms.Textarea(attrs={'rows': 3}),
        }
