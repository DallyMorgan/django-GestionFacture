# Generated by Django 4.2.4 on 2023-08-11 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('tel', models.CharField(max_length=20)),
                ('adresse', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Factures.client')),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=50)),
                ('stock', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProduitFacture',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantite', models.PositiveIntegerField(default=0, null=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=9)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=9)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Factures.facture')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Factures.produit')),
            ],
        ),
    ]
