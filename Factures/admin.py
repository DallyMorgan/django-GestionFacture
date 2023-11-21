from django.contrib import admin
from django.utils.safestring import mark_safe
from Factures.form import ProduitFactureForm, ProduitFactureFormSet
from .models import Facture, Produit, ProduitFacture, Client
from django.contrib.admin import AdminSite


class AdminProduit(admin.ModelAdmin):
   
    list_display = [ 'libelle','stock' ]

    search_fields = [ 'libele','stock']

    list_filter = [ 'libelle', 'stock']

    

# class ProduitFactureInline(admin.TabularInline):
#     model = ProduitFacture
#     extra = 0
   
    

class AdminClient(admin.ModelAdmin):
   
    list_display = [ 'nom', 'prenom', 'email', 'tel']

    search_fields = ['nom','prenom']

    list_filter = ['nom', 'prenom']


class ProduitFactureInline(admin.TabularInline):
    model = ProduitFacture
    formset = ProduitFactureFormSet
    extra = 1  
    def save_model(self, request, obj, form, change):
        obj.montant = obj.quantite * obj.prix  # Calcul automatique du montant
        super().save_model(request, obj, form, change)
    

class AdminFacture(admin.ModelAdmin):
    inlines = [ProduitFactureInline]
    
    list_display = ['__str__','date', 'status', 'Voir',]

    def Voir(self, obj):
        url = obj.get_absolute_url()
        return mark_safe(f'<a href="{url}">Voir</a>')
    Voir.short_description = 'Voir Facture'
    Voir.allow_tags = True
   
    search_fields = [ 'status']
   
    list_filter = [ 'status']

# class CustomAdminSite(AdminSite):
#     site_header = "Mon Super Site d'Administration"
#     site_title = "Mon Site d'Admin"
#     index_title = "Bienvenue sur Mon Site d'Admin"

admin.site.site_header = 'Gestion de Factures'    




admin.site.register(Produit, AdminProduit)
admin.site.register(Facture,AdminFacture)
admin.site.register(Client,AdminClient)
# admin.site.register(ProduitFacture)






