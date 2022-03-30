from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        exclude=['']


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

# class CoupanApplyForm(forms.Form):
#     code = forms.CharField()