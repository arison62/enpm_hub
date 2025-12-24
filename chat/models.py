from django.db import models
from core.models import ENSPMHubBaseModel


# ==========================================
# 8. GROUPES & MESSAGERIE
# ==========================================
class Groupe(ENSPMHubBaseModel):
    TYPE_GROUPE_CHOICES = [
        ('public', 'Public'),
        ('prive', 'Privé'), 
        ('administratif', 'Administratif')
    ]

    createur_profil = models.ForeignKey('users.Profil', on_delete=models.SET_NULL, null=True, related_name='groupes_crees')
    nom_groupe = models.CharField(max_length=150, unique=True)
    photo_groupe = models.ImageField(upload_to="photos_groups/", null=True, blank=True)
    description = models.TextField()
    est_valide = models.BooleanField(default=False)
    type_groupe = models.CharField(max_length=20, choices=TYPE_GROUPE_CHOICES, default='prive')
    max_membres = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'groupe'


class MembreGroupe(ENSPMHubBaseModel):
    ROLE_MEMBRE_CHOICES = [('membre', 'Membre'), ('moderateur', 'Modérateur'), ('admin', 'Admin')]

    profil = models.ForeignKey('users.Profil', on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='membres')
    role_membre = models.CharField(max_length=20, choices=ROLE_MEMBRE_CHOICES, default='membre')
    date_adhesion = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    est_actif = models.BooleanField(default=True)

    class Meta:
        db_table = 'membre_groupe'
        unique_together = ('profil', 'groupe')


class Message(ENSPMHubBaseModel):
    TYPE_FICHIER_CHOICES = [
        ('image', 'Image'), ('pdf', 'PDF'), ('word', 'Word'), ('excel', 'Excel'),
        ('powerpoint', 'PowerPoint'), ('video', 'Vidéo')
    ]

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='messages')
    profil = models.ForeignKey('users.Profil', on_delete=models.CASCADE)
    texte = models.TextField(null=True, blank=True)
    fichier= models.FileField(upload_to="messages_fichier/", null=True, blank=True)
    type_fichier = models.CharField(max_length=20, choices=TYPE_FICHIER_CHOICES, null=True, blank=True)
    est_supprime = models.BooleanField(default=False)

    class Meta:
        db_table = 'message'
        ordering = ['created_at']


class ValidationGroupe(ENSPMHubBaseModel):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='validations')
    validateur_profil = models.ForeignKey('users.Profil', on_delete=models.CASCADE)
    est_approuve = models.BooleanField()
    commentaire = models.TextField(null=True, blank=True)
    date_validation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'validation_groupe'