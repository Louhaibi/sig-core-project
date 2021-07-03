from django.db import models
from django.contrib.auth.models import Group, Permission, User


class Secteur(models.Model):
    """ Secteur
    """

    nom = models.CharField('Secteur', max_length=200)

    class Meta:
        verbose_name = ('Secteur')
        verbose_name_plural = ('Secteurs')

    def __str__(self):
        return '%s' % self.nom


class Commune(models.Model):
    """ Commune
    """

    nom = models.CharField('Commune', max_length=200)

    def __str__(self):
        return '%s' % self.nom


class Projet(models.Model):
    """ Projet
    """
    ETAT_AVANCEMENT = (
        ('PREPARATION', 'En phase de préparation'),
        ('LANCEMENT', 'En phase de lancement'),
        ('DEMARRAGE', 'En phase de démarrage'),
        ('ENCOURS', 'Opérationnel en cours d\'exécution'),
        ('ENRETARD', 'En retard en cours d\'exécution'),
        ('ENARRET', 'En arrêt en cours d\'exécution'),
        ('ARESILIER', 'A résilier'),
        ('TERMINE', 'Terminé')
    )

    RECEPTIONS = (
        ('PROVISOIRE', 'Provisoire'),
        ('DEFINITIVE', 'Définitive'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    # Aspect administratif
    intitule = models.CharField('Intitulé du projet', max_length=512)
    responsable = models.CharField('Responsable', max_length=64)
    convention = models.CharField('N° Convention', max_length=64, null=True, blank=True)

    communes = models.ManyToManyField(Commune)

    date_ouverture_plis = models.DateField(null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    delais = models.IntegerField(default=1, help_text='Délais en mois')
    date_fin = models.DateField(null=True, blank=True)
    date_reception_provisoire = models.DateField(null=True, blank=True)
    date_reception_definitive = models.DateField(null=True, blank=True)

    secteur = models.ForeignKey(Secteur, null=True, on_delete=models.SET_NULL)

    # Aspect financier
    titulaire = models.CharField('Titulaire du marché', max_length=128, null=True, blank=True)
    marche = models.CharField('N° Marché', max_length=64, null=True, blank=True)
    cout_global = models.FloatField('Côut global', null=True, blank=True)

    # Aspect technique
    etat_avancement = models.IntegerField('Etat d\'avancement physique (%)', default=0)
    etat = models.CharField('Etat projet', choices=ETAT_AVANCEMENT, max_length=64, default='PREPARATION')
    reception = models.CharField('Réception', choices=RECEPTIONS, max_length=64, null=True, blank=True)
    etat_lieu = models.TextField('Etat des lieux', help_text='Etat des lieux à l\'instant T', blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
    observations = models.TextField('Observations', blank=True, null=True)

    def __str__(self):
        return ' %s' % self.intitule
