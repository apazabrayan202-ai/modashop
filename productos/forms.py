from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos.
    Se usa en el panel de administración personalizado.
    """

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'precio',
            'imagen',
            'categoria',
            'tallas',
            'colores',
            'stock',
            'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'campo',
                'placeholder': 'Ej: Camiseta Oversize',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'campo',
                'rows': 4,
                'placeholder': 'Describe la prenda, material, estilo...',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'campo',
                'min': '0',
                'step': '0.01',
                'placeholder': '150.00',
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'campo',
            }),
            'categoria': forms.Select(attrs={
                'class': 'campo',
            }),
            'tallas': forms.TextInput(attrs={
                'class': 'campo',
                'placeholder': 'M, L, XL',
            }),
            'colores': forms.TextInput(attrs={
                'class': 'campo',
                'placeholder': 'Negro, Blanco, Rojo',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'campo',
                'min': '0',
                'placeholder': '10',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'checkbox',
            }),
        }

    def clean_precio(self):
        """Validar que el precio sea positivo."""
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que 0.')
        return precio

    def clean_stock(self):
        """Validar que el stock no sea negativo."""
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock


class CambiarPasswordForm(PasswordChangeForm):
    """Formulario personalizado para cambiar la contraseña."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'campo',
            'placeholder': 'Contraseña actual',
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'campo',
            'placeholder': 'Nueva contraseña',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'campo',
            'placeholder': 'Confirmar nueva contraseña',
        })