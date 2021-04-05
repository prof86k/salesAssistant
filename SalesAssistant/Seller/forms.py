from django import forms

from .models import Product,ProductType

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_type",
            ]

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = [
            "type_name",
            ]