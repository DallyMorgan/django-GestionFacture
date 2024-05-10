from django.contrib import admin
from django.utils.safestring import mark_safe
from Factures.form import  ProduitFactureFormSet
from .models import Facture, Produit, ProduitFacture, Client
from simple_history.admin import SimpleHistoryAdmin

class AdminProduitMixin(SimpleHistoryAdmin,admin.ModelAdmin ):
   
    list_display = [ 'libelle','stock' ]

    search_fields = [ 'libele','stock']

    list_filter = [ 'libelle', 'stock']

    list_per_page = 10

    

# class ProduitFactureInline(admin.TabularInline):
#     model = ProduitFacture
#     extra = 0
   
    

class AdminClientMixin(SimpleHistoryAdmin,admin.ModelAdmin):
   
    list_display = [ 'nom', 'prenom', 'email', 'tel']

    search_fields = ['nom','prenom']

    list_filter = ['nom', 'prenom']
    list_per_page = 10


class ProduitFactureInline(admin.TabularInline):
    model = ProduitFacture
    formset = ProduitFactureFormSet
    extra = 1  
    def save_model(self, request, obj, form, change):
        obj.montant = obj.quantite * obj.prix  # Calcul automatique du montant
        super().save_model(request, obj, form, change)
    

class AdminFactureMixin(SimpleHistoryAdmin,admin.ModelAdmin):
    inlines = [ProduitFactureInline]
    
    list_display = ['__str__','date', 'status', 'Voir',]

    def Voir(self, obj):
        url = obj.get_absolute_url()
        return mark_safe(f'<a href="{url}">Voir la facture</a>')
    Voir.short_description = 'Voir Facture'
    Voir.allow_tags = True
   
    search_fields = [ 'status']
   
    list_filter = [ 'status']
    
    list_per_page = 10

# class CustomAdminSite(AdminSite):
#     site_header = "Mon Super Site d'Administration"
#     site_title = "Mon Site d'Admin"
#     index_title = "Bienvenue sur Mon Site d'Admin"

admin.site.site_header = 'Gestion de Factures'    




admin.site.register(Produit, AdminProduitMixin)
admin.site.register(Facture,AdminFactureMixin)
admin.site.register(Client,AdminClientMixin)
# admin.site.register(ProduitFacture)






