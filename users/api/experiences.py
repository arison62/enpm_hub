from typing import List, Optional
from uuid import UUID
from ninja import Router
from django.http import HttpRequest
from core.services.auth_service import jwt_auth

from users.api.schemas import (
    ExperienceProfessionnelleOut,
    ExperienceProfessionnelleCreate,
    ExperienceProfessionnelleUpdate
)

from users.services.experience_service import experience_service

experience_router = Router(tags=["Expériences Professionnelles"])

@experience_router.get("/", response=List[ExperienceProfessionnelleOut], auth=jwt_auth)
def list_experiences(request: HttpRequest, profil_id: Optional[UUID] = None):
    """
    Liste les expériences professionnelles.
    - Si profil_id est fourni : renvoie les expériences de ce profil (si public).
    - Sinon : renvoie les expériences de l'utilisateur connecté.
    """
    return experience_service.list_experiences(user=request.auth, profil_id=profil_id) # type: ignore

@experience_router.post("/{profil_id}/", response={201: ExperienceProfessionnelleOut}, auth=jwt_auth)
def create_experience(request: HttpRequest, profil_id: UUID, payload: ExperienceProfessionnelleCreate):
    """
    Ajoute une nouvelle expérience au profil de l'utilisateur connecté.
    Gère automatiquement la logique 'Poste actuel'.
    """
    # L'audit est géré dans le service via transaction.atomic
    return experience_service.create_experience(acting_user=request.auth, profil_id=profil_id, data=payload) # type: ignore

@experience_router.put("/{experience_id}/", response=ExperienceProfessionnelleOut, auth=jwt_auth)
def update_experience(request: HttpRequest, experience_id: UUID, payload: ExperienceProfessionnelleUpdate):
    """
    Met à jour une expérience existante.
    Vérifie que l'expérience appartient bien à l'utilisateur.
    """
    return experience_service.update_experience(
        acting_user=request.user,  # type: ignore
        experience_id=experience_id, 
        data=payload
    )

@experience_router.delete("/{experience_id}", response={204: None}, auth=jwt_auth)
def delete_experience(request: HttpRequest, experience_id: UUID):
    """
    Supprime une expérience.
    """
    experience_service.delete_experience(acting_user=request.user, experience_id=experience_id) # type: ignore
    return 204, None