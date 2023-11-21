from Factures import views
from django.urls import path
from .views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #statistiques
    path('', index, name="index"),
    path('recette_mois/', views.recette_mois, name='recette_mois'),


    #routes pour facture
    path('creer_facture/', views.facture, name='facture'),
    path('liste_facture/', views.liste_facture, name='liste_facture'),
    path('tri_facture/', views.tri_facture, name='tri_facture'),
    path('detail-facture/<int:id>', views.detail_facture, name='detail_facture'),
    path('suprimer_facture/<int:id>/', views.sup_fact, name='sup_fact'),

    #routes pour client
    path('creer_client/', views.client, name='client'),
    path('liste_client/', views.liste_client, name='liste_client'),
    path('suprimer_client/<int:id>/', views.sup_client, name='sup_client'),

    #route pour produit
    path('creer_produit/', views.produit, name='produit'),
    path('liste_produit/', views.liste_produit, name='liste_produit'),
    path('suprimer_produit/<int:id>/', views.sup_produit, name='sup_produit'),
    path('afficher_produit/<int:id>/', views.afficher_produit, name='afficher_produit'),
    path('modifier_produit/<int:id>/', views.modifier_produit, name='modifier_produit'),

   

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

