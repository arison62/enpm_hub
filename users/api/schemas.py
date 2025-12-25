# users/api/schemas.py
from math import ceil
from typing import Annotated, Dict, Optional, List
from ninja import Schema, Field, ModelSchema
from pydantic import UUID4, EmailStr, field_validator
from datetime import datetime
from core.models import User
from users.models import Profil, LienReseauSocialProfil
from core.api.schemas import PaginationMetaSchema
from core.api.schemas import (
    AnneePromotionSimple, DomaineSimple, TitreHonorifiqueSimple,
    SecteurActiviteSimple, PosteSimple, DeviseSimple, ReseauSocialSimple
)

class ProfilBaseOut(ModelSchema):
    """Schéma de base pour Profil (sans réseaux sociaux)"""
    photo_profil: Optional[str] = None
    titre : Optional[TitreHonorifiqueSimple] = None
    domaine : Optional[DomaineSimple] = None
    pays : Optional[str]
    pays_nom : Optional[str]
    annee_sortie : Optional[AnneePromotionSimple] = None

    class Meta:
        model = Profil
        fields = [
            'id', 'nom_complet', 'matricule', 'titre', 'statut_global', 'travailleur',
            'annee_sortie', 'adresse', 'telephone', 'ville', 'pays', 'domaine', 'bio',
            'slug', 'created_at', 'updated_at'
        ]

    @staticmethod
    def resolve_photo_profil(obj):
        return obj.photo_profil.url if obj.photo_profil else None
    
    @staticmethod
    def resolve_titre(obj):
        """Retourne l'objet TitreHonorifique complet"""
        if obj.titre:
            return {
                "id": obj.titre.id,
                "titre": obj.titre.titre,
                "nom_complet": obj.titre.nom_complet
            }
        return None
    
    @staticmethod
    def resolve_domaine(obj):
        """Retourne l'objet Domaine complet"""
        if obj.domaine:
            return {
                "id": obj.domaine.id,
                "nom": obj.domaine.nom,
                "code": obj.domaine.code
            }
        return None
    
    @staticmethod
    def resolve_annee_sortie(obj):
        """Retourne l'objet AnneePromotion complet"""
        if obj.annee_sortie:
            return {
                "id": obj.annee_sortie.id,
                "annee": obj.annee_sortie.annee,
                "libelle": obj.annee_sortie.libelle
            }
        return None
    
    @staticmethod
    def resolve_pays(obj):
        """Retourne le code ISO du pays"""
        return obj.pays.code if obj.pays else None
    
    @staticmethod
    def resolve_pays_nom(obj):
        """Retourne le nom du pays"""
        return obj.pays.name if obj.pays else None

class ProfilCompleteOut(ProfilBaseOut):
    """Schéma complet pour Profil avec réseaux sociaux (étend ProfilBaseOut)"""
    liens_reseaux: List['LienReseauSocialOut'] = []

    @staticmethod
    def resolve_liens_reseaux(obj):
        """Retourne les liens réseaux actifs"""
        return list(obj.liens_reseaux.filter(est_actif=True).select_related('reseau'))


# ==========================================
# SCHÉMAS CRÉATION/MISE À JOUR PROFIL
# ==========================================
# Pas de redondance: Un pour create (requis), un pour update (optionnel).

class ProfilCreate(Schema):
    """Schéma pour création Profil (champs requis/minimaux)"""
    nom_complet: str = Field(..., description="Nom complet")
    matricule: Optional[str] = None
    titre_id: Optional[UUID4] = None  # FK vers TitreHonorifique
    statut_global: str = 'etudiant'
    travailleur: bool = False
    annee_sortie_id: Optional[UUID4] = None  # FK vers AnneePromotion
    adresse: Optional[str] = Field(None, description="Adresse", max_length=255)
    telephone: Optional[str] = Field(None, description="N° de tél.", max_length=20)
    ville: Optional[str] = Field(None, description="Ville", max_length=100)
    pays: Optional[str] = None  # Code pays ISO
    domaine_id: Optional[UUID4] = None  # FK vers Domaine
    bio: Optional[str] = None

    @field_validator('statut_global')
    def validate_statut(cls, v):
        if v not in [choice[0] for choice in Profil.STATUT_GLOBAL_CHOICES]:
            raise ValueError('Statut global invalide')
        return v

class ProfilUpdate(ModelSchema):
    """Schéma pour mise à jour partielle Profil"""
    titre_id: Optional[str] = None  # FK vers TitreHonorifique
    annee_sortie_id: Optional[str] = None  # FK vers AnneePromotion
    domaine_id:Optional[str] = None
    class Meta:
        model = Profil
        fields = [
            'nom_complet', 'matricule', 'statut_global', 'travailleur',
             'adresse', 'telephone', 'ville', 'pays', 'bio'
        ]
        fields_optional = '__all__'

    @field_validator('statut_global', check_fields=False)
    def validate_statut(cls, v):
        if v not in [choice[0] for choice in Profil.STATUT_GLOBAL_CHOICES]:
            raise ValueError('Statut global invalide')
        return v


# ==========================================
# SCHÉMAS POUR LIEN RÉSEAU SOCIAL
# ==========================================

class LienReseauSocialOut(ModelSchema):
    """Schéma sortie pour LienReseauSocialProfil"""
    reseau: ReseauSocialSimple
    class Meta:
        model = LienReseauSocialProfil
        fields = ['id', 'reseau', 'url', 'est_actif', 'created_at', 'updated_at']

    @staticmethod
    def resolve_reseau(obj):
        """Retourne l'objet ReseauSocial complet"""
        return {
            "id": obj.reseau.id,
            "nom": obj.reseau.nom,
            "code": obj.reseau.code,
            "url_base": obj.reseau.url_base
        }
class LienReseauSocialCreate(Schema):
    """Schéma création lien réseau social"""
    reseau: UUID4
    url: str

class LienReseauSocialUpdate(Schema):
    """Schéma mise à jour lien réseau social"""
    url: Optional[str] = None
    est_actif: Optional[bool] = None


# ==========================================
# SCHÉMAS UTILISATEUR
# ==========================================
# Consolidation: UserBaseOut pour infos basiques, étendu pour détail/complet.

class UserBaseOut(ModelSchema):
    """Schéma base pour User (sans profil)"""
    class Meta:
        model = User
        fields = ['id', 'email', 'role_systeme', 'est_actif', 'last_login', 'created_at', 'updated_at']
        # Exclusion sensible: mot_de_passe, groups, user_permissions

class UserDetailOut(UserBaseOut):
    """Schéma détail User avec profil base"""
    profil: Optional[ProfilBaseOut] = None

class UserCompleteOut(UserBaseOut):
    """Schéma complet User avec profil étendu (inclut réseaux sociaux)"""
    profil: Optional[ProfilCompleteOut] = None



# ==========================================
# SCHÉMAS CRÉATION/MISE À JOUR UTILISATEUR
# ==========================================

class UserCreate(Schema):
    """Schéma création User (public/self-register)"""
    email: EmailStr
    password: Annotated[int, Field(..., min_length=8, description="Mot de passe (min. 8 caractères)")]
    profil: ProfilCreate

class UserCreateAdmin(Schema):
    """Schéma création User par admin (password optionnel)"""
    email: EmailStr
    password: Optional[str] = Field(..., min_length=8, description="Mot de passe (min. 8 caractères)")
    role_systeme: str = 'user'
    est_actif: bool = True
    profil: ProfilCreate

    @field_validator('role_systeme')
    def validate_role(cls, v):
        if v not in [choice[0] for choice in User.ROLE_SYSTEME_CHOICES]:
            raise ValueError('Rôle système invalide')
        return v

class UserUpdate(ModelSchema):
    """Schéma mise à jour User (self ou admin)"""
    profil: Optional[ProfilUpdate] = None
    class Meta:
        model = User
        fields = ['email', 'role_systeme', 'est_actif']
        fields_optional = '__all__'


    

# ==========================================
# SCHÉMAS MOT DE PASSE
# ==========================================

class ChangePassword(Schema):
    """Changement mot de passe par user"""
    old_password: str
    new_password: str = Field(..., min_length=8)

class ResetPassword(Schema):
    """Réinitialisation mot de passe par admin"""
    new_password: Optional[str] = None  # Généré si None

class PasswordResponse(Schema):
    """Réponse après reset/changement"""
    message: str
    temporary_password: Optional[str] = None

# ==========================================
# SCHÉMAS PHOTO PROFIL
# ==========================================

class PhotoUploadResponse(Schema):
    message: str = "Photo mise à jour"
    photo_url: Optional[str] = None

class PhotoDeleteResponse(Schema):
    message: str = "Photo supprimée"



# ==========================================
# SCHÉMAS LISTE
# ==========================================
# Cohérent: Meta générique, utilisé pour listes paginées.

class UserCompleteListResponse(Schema):
    """Liste paginée Users (utilise UserCompleteOut pour détail)"""
    items: List[UserCompleteOut]
    meta: PaginationMetaSchema

class UserListResponse(Schema):
    """Liste paginée Users (utilise UserDetailOut pour détail)"""
    items: List[UserDetailOut]
    meta: PaginationMetaSchema

# ==========================================
# SCHÉMAS FILTRES ET STATISTIQUES
# ==========================================

class UserFilter(Schema):
    search: Optional[str] = None  # Nom, email, matricule, etc.
    role_systeme: Optional[str] = None
    statut_global: Optional[str] = None
    est_actif: Optional[bool] = None


class UserStatistics(Schema):
    total_users: int
    active_users: int
    inactive_users: int
    deleted_users: int
    by_role: Dict[str, int]
    by_status: Dict[str, int]

# ==========================================
# SCHÉMAS GESTION COMPTE
# ==========================================

class ToggleStatus(Schema):
    est_actif: bool

class SlugUpdate(Schema):
    slug: str

# ==========================================
# SCHÉMAS ERREURS (STANDARDISÉS)
# ==========================================

class FieldError(Schema):
    field: str
    message: str

class ValidationErrorResponse(Schema):
    detail: str = "Erreur de validation"
    errors: List[FieldError]

class MessageResponse(Schema):
    detail: str
