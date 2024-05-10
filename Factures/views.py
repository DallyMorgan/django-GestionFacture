
from collections import defaultdict
import json
import re
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.views import View
from Factures.form import ClientForm, FactureForm, ProduitFactureFormSet, ProduitForm
from django.contrib import messages
from .models import Produit, Client, Facture, ProduitFacture
from django.db.utils import IntegrityError
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.db.models import Count



#fonctions liées  ux statistiques



def calcul_recette_totale(factures):
    factures = Facture.objects.all()  # Notez l'appel de méthode '()'
    total = 0
    for facture in factures:
        total += facture.totaux()
    return total

def calcul_taxe_totale(factures):
    factures = Facture.objects.all()  # Notez l'appel de méthode '()'
    total = 0
    for facture in factures:
        total += facture.ttc()
    return total


def calcul_pourcentage_croissance_par_semaine(factures):
    # Calculez le pourcentage de croissance par semaine
    # Assurez-vous que vos factures ont une date
    if factures and factures[0].date:
        date_min = min(facture.date for facture in factures)
        date_max = max(facture.date for facture in factures)
        duree_en_semaines = Decimal((date_max - date_min).days) / Decimal(7)
        recette_totale = Decimal(calcul_recette_totale(factures))
        pourcentage_croissance = ((recette_totale - Decimal(factures[0].totaux())) / Decimal(factures[0].totaux())) * 100
        pourcentage_par_semaine = round(pourcentage_croissance / duree_en_semaines, 0)
        return pourcentage_par_semaine
    else:
        return 0  # Aucune facture avec une date
    

def calcul_pourcentage_croissance_par_semaine_taxe(factures):
    # Calculez le pourcentage de croissance par semaine
    # Assurez-vous que vos factures ont une date
    if factures and factures[0].date:
        date_min = min(facture.date for facture in factures)
        date_max = max(facture.date for facture in factures)
        duree_en_semaines = Decimal((date_max - date_min).days) / Decimal(7)
        taxe_totale = Decimal(calcul_taxe_totale(factures))
        pourcentage_croissance = ((taxe_totale - Decimal(factures[0].totaux())) / Decimal(factures[0].totaux())) * 100
        pourcentage_par_semaine_taxe = round(pourcentage_croissance / duree_en_semaines, 0)
        return pourcentage_par_semaine_taxe
    else:
        return 0  # Aucune facture avec une date
    

def recette_mois(request):
    # Obtenez toutes les factures
    factures = Facture.objects.all()

    # Initialisez un dictionnaire pour stocker les recettes par mois
    recettes_par_mois = {}

    # Itérez sur les factures et calculez les recettes par mois
    for facture in factures:
        mois = facture.date.strftime('%Y-%m')  # Utilisez la date de la facture pour obtenir l'année et le mois
        montant_total = facture.totaux()  # Appelez la méthode totaux pour obtenir le montant total de la facture

        # Si le mois n'existe pas encore dans le dictionnaire, ajoutez-le
        if mois not in recettes_par_mois:
            recettes_par_mois[mois] = 0

        # Ajoutez le montant total au mois correspondant
        recettes_par_mois[mois] += montant_total

    # Convertissez le dictionnaire en une liste de dictionnaires JSON
    recettes_json = [{'mois': mois, 'total_recettes': total} for mois, total in recettes_par_mois.items()]

    return JsonResponse(recettes_json, safe=False)


@login_required
def index(request):
    user = request.user
    produits = Produit.objects.all()
    factures = Facture.objects.all()
    clients = Client.objects.all()

    recette_totale = calcul_recette_totale(factures)
    taxe_totale = calcul_taxe_totale(factures)
    pourcentage_par_semaine = calcul_pourcentage_croissance_par_semaine(factures)
    pourcentage_par_semaine_taxe = calcul_pourcentage_croissance_par_semaine_taxe(factures)
    recette_totale_formatee = round(recette_totale, 0)
    taxe_totale_formatee = round(taxe_totale, 0)
    recette_ht = recette_totale_formatee - taxe_totale_formatee

    # Calcul des données pour le graphique
    data = Facture.objects.annotate(
        mois=TruncMonth('date')
    ).values('mois').annotate(
        total_factures=Count('id')
    ).order_by('mois')

    mois = [entry['mois'].strftime('%b %Y') for entry in data]
    total_factures = [entry['total_factures'] for entry in data]

    # Appel de la fonction recette_mois pour obtenir les données par mois
    # recettes_mois = recette_mois()

    context = {
        'user': user,
        'produits': produits,
        'clients': clients,
        'factures': factures,
        'recette_totale_formatee': recette_totale_formatee,
        'taxe_totale_formatee': taxe_totale_formatee,
        'pourcentage_par_semaine': pourcentage_par_semaine,
        'pourcentage_par_semaine_taxe': pourcentage_par_semaine_taxe,
        'recette_ht': recette_ht,
        'mois': mois,
        'total_factures': total_factures,
        # 'recettes_mois': recettes_mois,  # Assurez-vous que cette variable est correcte
    }

    return render(request, 'Statistique/stat.html', context)




@login_required
def detail_facture (request, id):
    user = request.user
    facture = Facture.objects.get(pk=id)


    return render(request, 'Facture/detail_facture.html',{'user':user, 'facture':facture})

# def client (request):
#     user = request.user

#     return render(request, 'Client/index.html',{'user':user})




#fonctions liées au modele Produit
@login_required
def produit(request):
    user = request.user
    produits = Produit.objects.all
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid() :
            form.save()
            
            messages.success(request, "Produit enregistré avec succes.")
            return redirect('produit')
    else :
        form = ProduitForm()
        

    context = {
        'form': form,
        'produits': produits,
        'user': user,
    }
    return render(request, 'Produit/index.html', context)


@login_required
@require_http_methods(['GET'])
def liste_produit(request):
    query = request.GET.get("p")
    produits = Produit.objects.all()
    if query:
        produits = produits.filter(
            Q(libelle__icontains=query) |
            Q(couleur__icontains=query) |
            Q(position__icontains=query)
        )

    context = {
        "produits": produits,
        "query": query,       
    }
    return render(request, "Produit/table.html", context)


@login_required
@require_http_methods(['DELETE'])
def sup_produit(request, id):
    try:
        produit = Produit.objects.get(pk=id)
        produit.delete()
        
        return HttpResponse('')
    except Facture.DoesNotExist:
        return HttpResponse(status=404)




@login_required
@require_http_methods(['GET'])
def afficher_produit(request, id):

    produit = Produit.objects.get(id=id)

    return render(request, 'Produit/forms.html', { 'produit': produit, })


@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    produits= Produit.objects.all

    if request.method == 'POST':
        # Récupérez les données du formulaire POST
        libelle = request.POST['libelle']
        stock = request.POST['stock']
        couleur = request.POST['couleur']
        position = request.POST['position']

        # Mettez à jour les données du produit
        produit.libelle = libelle
        produit.stock = stock
        produit.couleur = couleur
        produit.position = position
        produit.save()

        messages.success(request, "Produit modifié avec succes.")
        context = {
        'produit': produit,
        'produits': produits,
    }

        html_fragment = render_to_string('Produit/table.html', context)
        return HttpResponse(html_fragment)

        # return redirect('Produit/table.html') 

    
    return render(request, 'Produit/index.html', context)













#fonctions liés a la table Fcature
@login_required
@require_http_methods(['DELETE'])
def sup_fact(request, id):
    try:
        facture = Facture.objects.get(pk=id)
        facture.delete()
        
        return HttpResponse('')
    except Facture.DoesNotExist:
        return HttpResponse(status=404)








@login_required
@require_http_methods(['GET'])
def liste_facture(request):
    query = request.GET.get("q")
    factures = Facture.objects.all()
    if query:
        factures = factures.filter(
            Q(client__nom__icontains=query) |
            Q(client__prenom__icontains=query) |
            Q(status__icontains=query)
        )

    context = {
        "factures": factures,
        "query": query,       
    }
    return render(request, "Facture/table.html", context)


@require_http_methods(['GET'])
def tri_facture(request):
    date = request.GET.get("date")
  
    if date:
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
            factures = Facture.objects.filter(date=date)
        except ValueError:
            # Gérer une date invalide ici si nécessaire
            factures = Facture.objects.all()[:5]
    else:
        factures = Facture.objects.all()[:5]

    context = {
        "factures": factures,
        "date": date,
    }

    return render(request, "Facture/table.html", context)

#fin des fonctions liés la table facture



#debut des fonctions liés a la table client
@login_required
def client(request):
    user = request.user
    clients = Client.objects.all
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid() :
            form.save()
            
            return redirect('client')
    else :
        form = ClientForm()
        

    context = {
        'form': form,
        'clients': clients,
        'user': user,
    }
    return render(request, 'Client/index.html', context)

@login_required
@require_http_methods(['GET'])
def liste_client(request):
    query = request.GET.get("c")
    clients = Client.objects.all()
    if query:
        clients = clients.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(adresse__icontains=query)
        )

    context = {
        "clients": clients,
        "query": query,       
    }
    return render(request, "Client/table.html", context)


@login_required
@require_http_methods(['DELETE'])
def sup_client(request, id):
    try:
        clients = Client.objects.get(pk=id)
        clients.delete()
        
        return HttpResponse('')
    except Client.DoesNotExist:
        return HttpResponse(status=404)
    

def facture(request):
    clients = Client.objects.all()
    factures = Facture.objects.all().order_by('-date')[:5]
    # facture = Facture.objects.all()
    produits = Produit.objects.all()
    user = request.user

    # if request.method == 'POST':
    #     client = request.POST.get("client")
    #     status = request.POST.get("status")
    #     produits = request.POST.getlist("produit")
    #     print(produits)

    #     # Faites quelque chose avec les données récupérées...

    context = {
        'clients': clients,
        'factures': factures,
        # 'facture': facture,
        'produits': produits,
        'user': user,
    }

    return render(request, "Facture/facture.html", context)


def facture_cree(request):
    user = request.user

    if request.method == 'POST':
        client_id = request.POST.get("client")
        status = request.POST.get("status")
        produits = request.POST.getlist("produit")
        prix_list = request.POST.getlist("prix")
        quantite_list = request.POST.getlist("quantite")

        # Créer un objet Facture
        facture = Facture.objects.create(
            client_id=client_id,
            status=status
        )

        produit_facture_list = []

        # Parcourir les produits, prix et quantités
        for produit_id, prix_produit, quantite_produit in zip(produits, prix_list, quantite_list):
            # Récupérer l'objet Produit existant avec l'ID donné
            produit = Produit.objects.get(id=produit_id)

            # Initialiser la variable prix
            prix = 0.0

            try:
                # Convertir la chaîne en un nombre
                prix = float(prix_produit)
            except ValueError:
                # La conversion a échoué, peut-être gérer cette situation d'une manière appropriée
                # Vous pouvez laisser la valeur par défaut 0.0 ou gérer différemment
                print("erreur lors de la coonversion")
            
            montant = prix * float(quantite_produit)

            produit_facture = ProduitFacture(
                facture=facture,
                produit=produit,
                prix=prix,
                quantite=quantite_produit,
                montant=montant
            )

            produit_facture_list.append(produit_facture)

        # Utiliser bulk_create pour enregistrer tous les objets ProduitFacture en une seule requête
        ProduitFacture.objects.bulk_create(produit_facture_list)
        return redirect ('facture')

        # Faites quelque chose avec les données récupérées...

    context = {
        'user': user,
    }

    return render(request, "Facture/facture.html", context)


