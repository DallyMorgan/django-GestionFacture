from decimal import Decimal
from django.urls import reverse
from django.db import models
from simple_history.models import HistoricalRecords

class Produit(models.Model):
    

    COULEUR_CHOICES = [
        ('BLANC', 'Blanc'),
        ('AUTRE', 'Autre'),
        ('Null', 'null'),
]
    POSITION_CHOICES = [
        ('AVANT', 'avant'),
        ('ARRIERE', 'arriere'),
        ('Null', 'null'),
]

    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    couleur = models.CharField(choices=COULEUR_CHOICES, max_length=20, default="null")
    position = models.CharField(choices=POSITION_CHOICES, max_length=20, default="null")
    history = HistoricalRecords()

    def __str__(self):
        return str (self.libelle)

class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    tel = models.CharField(max_length=20)
    adresse = models.CharField(null=True, blank=True, max_length=80)
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.nom} {self.prenom} '
    



class Facture(models.Model):
    choice_status = [
        ( 'Impayé','IMPAYE'),
        ( 'Payé','PAYE')
    ]
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client,on_delete= models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.CharField(choices=choice_status,max_length=20)
    history = HistoricalRecords()
   
    def __str__(self):
        return f'Facture de {self.client.nom} {self.client.prenom} '
    
    # def totaux(self):
    #     total = 0
    #     for produit_facture in self.produit.all():
    #         total += produit_facture.get_montant()
    #     return total 
    def totaux(self):
        total = 0
        for produit_facture in self.produitfacture_set.all():
            total += produit_facture.montant
        return total
    
    def get_absolute_url(self):
        return reverse('detail_facture', args=[str(self.id)])
    
    def ttc(self):
        return self.totaux() * Decimal('0.03')



    
class ProduitFacture(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=0, null=True)
    prix = models.DecimalField(max_digits=9, decimal_places=2)
    montant = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'Facture de {self.facture.client.nom} {self.facture.client.prenom}  '
    
    def save(self, *args, **kwargs):
        # Calcul automatique du montant lors de la sauvegarde
        self.montant = self.calculer_montant()

        # # Vérifier si la quantité spécifiée ne dépasse pas le stock disponible
        # if self.quantite > self.produit.stock:
        #     raise IntegrityError("Quantité non disponible en stock.")

        super().save(*args, **kwargs)

        # # Mettre à jour le stock du produit
        # self.produit.stock -= self.quantite
        # self.produit.save()


    def calculer_montant(self):
        return self.quantite * self.prix

