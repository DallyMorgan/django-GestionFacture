# # forms.py
# from django import forms
# from .models import Client, Facture, Produit, ProduitFacture
# from django.forms import inlineformset_factory

# class FactureForm(forms.ModelForm):
#     class Meta:
#         model = Facture
#         fields = ['client', 'status']
        

# class ProduitFactureForm(forms.ModelForm):
#     class Meta:
#         model = ProduitFacture
#         fields = ['produit', 'quantite', 'prix']

# ProduitFactureFormSet = inlineformset_factory(
#     Facture,
#     ProduitFacture,
#     form=ProduitFactureForm,
#     extra=5,  # Nombre initial de formulaires à afficher
#     can_delete=False,
# )




from django import forms
from .models import Client, Facture, Produit, ProduitFacture
from django.forms import inlineformset_factory

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client', 'status']

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client  # Utilisez un seul égal ici, pas deux points
        fields = ['nom', 'prenom', 'email', 'tel', 'adresse',]
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit  # Utilisez un seul égal ici, pas deux points
        fields = ['libelle', 'stock', 'couleur', 'position',]
    
    def __init__(self, *args, **kwargs):
        super(ProduitForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'



class ProduitFactureForm(forms.ModelForm):
    class Meta:
        model = ProduitFacture
        fields = ['produit', 'quantite', 'prix']

    def __init__(self, *args, **kwargs):
        super(ProduitFactureForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

ProduitFactureFormSet = inlineformset_factory(
    Facture,
    ProduitFacture,
    form=ProduitFactureForm,
    extra=3,  # Nombre initial de formulaires à afficher
    can_delete=False,
)
