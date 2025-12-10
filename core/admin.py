from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from core.models import User, AuditLog

# ==========================================
# 1. CONFIGURATION ADMIN UTILISATEUR
# ==========================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle User.
    Affiche tous les champs pertinents avec filtres et recherche optimisée.
    """
    
    # Champs affichés dans la liste
    list_display = (
        'email', 'nom', 'prenom', 'matricule', 
        'statut', 'role', 'est_actif_badge', 
        'travailleur_badge', 'photo_thumbnail', 
        'created_at'
    )
    
    # Filtres latéraux
    list_filter = (
        'role', 'statut', 'est_actif', 'travailleur', 
        'deleted', 'is_staff', 'is_superuser',
        'created_at', 'updated_at'
    )
    
    # Champs de recherche
    search_fields = (
        'email', 'nom', 'prenom', 'matricule', 
        'telephone', 'domaine'
    )
    
    # Ordre par défaut
    ordering = ('-created_at',)
    
    # Nombre d'éléments par page
    list_per_page = 25
    
    # Champs cliquables pour accéder au détail
    list_display_links = ('email', 'nom', 'prenom')
    
    # Actions disponibles
    actions = ['activate_users', 'deactivate_users', 'soft_delete_users', 'restore_users']
    
    # Organisation des champs dans le formulaire de détail
    fieldsets = (
        (_('Informations de connexion'), {
            'fields': ('email', 'password')
        }),
        (_('Informations personnelles'), {
            'fields': (
                'titre', 'nom', 'prenom', 'matricule', 
                'telephone', 'bio', 'photo_profile'
            )
        }),
        (_('Informations académiques/professionnelles'), {
            'fields': (
                'statut', 'domaine', 'annee_sortie', 'travailleur'
            )
        }),
        (_('Permissions et Rôles'), {
            'fields': (
                'role', 'est_actif', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
            'classes': ('collapse',)  # Section repliable
        }),
        (_('Métadonnées'), {
            'fields': (
                'id', 'created_at', 'updated_at', 
                'deleted', 'deleted_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = (
        'id', 'created_at', 'updated_at', 
        'deleted_at', 'last_login'
    )
    
    # Configuration pour la création d'utilisateur
    add_fieldsets = (
        (_('Informations de connexion'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Informations personnelles'), {
            'fields': ('nom', 'prenom', 'matricule', 'telephone')
        }),
        (_('Statut et Rôle'), {
            'fields': ('statut', 'role', 'est_actif')
        }),
    )
    
    # ==========================================
    # Méthodes personnalisées pour l'affichage
    # ==========================================
    
    @admin.display(description='Actif', boolean=True)
    def est_actif_badge(self, obj):
        """Affiche un badge coloré pour le statut actif."""
        return obj.est_actif and not obj.deleted
    
    @admin.display(description='Travailleur', boolean=True)
    def travailleur_badge(self, obj):
        """Affiche un badge pour le statut travailleur."""
        return obj.travailleur
    
    @admin.display(description='Photo')
    def photo_thumbnail(self, obj):
        """Affiche une miniature de la photo de profil."""
        if obj.photo_profile:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; '
                'border-radius: 50%; object-fit: cover;" />',
                obj.photo_profile.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 50%; '
            'background-color: #e0e0e0; display: flex; align-items: center; '
            'justify-content: center; color: #666;">N/A</div>'
        )
    
    # ==========================================
    # Actions personnalisées
    # ==========================================
    
    @admin.action(description='Activer les utilisateurs sélectionnés')
    def activate_users(self, request, queryset):
        """Active les utilisateurs sélectionnés."""
        updated = queryset.update(est_actif=True)
        self.message_user(
            request, 
            f'{updated} utilisateur(s) activé(s) avec succès.'
        )
    
    @admin.action(description='Désactiver les utilisateurs sélectionnés')
    def deactivate_users(self, request, queryset):
        """Désactive les utilisateurs sélectionnés."""
        updated = queryset.update(est_actif=False)
        self.message_user(
            request, 
            f'{updated} utilisateur(s) désactivé(s) avec succès.'
        )
    
    @admin.action(description='Supprimer (soft delete) les utilisateurs sélectionnés')
    def soft_delete_users(self, request, queryset):
        """Effectue une suppression logique des utilisateurs."""
        count = 0
        for user in queryset:
            if not user.deleted:
                user.soft_delete()
                count += 1
        self.message_user(
            request, 
            f'{count} utilisateur(s) supprimé(s) (soft delete) avec succès.'
        )
    
    @admin.action(description='Restaurer les utilisateurs supprimés')
    def restore_users(self, request, queryset):
        """Restaure les utilisateurs supprimés."""
        count = 0
        for user in queryset:
            if user.deleted:
                user.restore()
                count += 1
        self.message_user(
            request, 
            f'{count} utilisateur(s) restauré(s) avec succès.'
        )
    
    # ==========================================
    # Surcharge pour afficher les utilisateurs supprimés
    # ==========================================
    
    def get_queryset(self, request):
        """
        Affiche tous les utilisateurs, y compris ceux supprimés (soft delete).
        Utilise all_objects au lieu de objects.
        """
        return User.all_objects.all()
    
    # ==========================================
    # Permissions personnalisées
    # ==========================================
    
    def has_delete_permission(self, request, obj=None):
        """
        Empêche la suppression permanente depuis l'admin.
        Utiliser l'action soft_delete à la place.
        """
        return False  # Désactiver la suppression permanente


# ==========================================
# 2. CONFIGURATION ADMIN AUDIT LOG
# ==========================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Administration pour le journal d'audit.
    En lecture seule pour préserver l'intégrité de l'audit.
    """
    
    # Champs affichés dans la liste
    list_display = (
        'created_at', 'user_link', 'action_badge', 
        'entity_type', 'entity_id', 'ip_address'
    )
    
    # Filtres latéraux
    list_filter = (
        'action', 'entity_type', 'created_at'
    )
    
    # Champs de recherche
    search_fields = (
        'user__email', 'user__nom', 'user__prenom',
        'entity_type', 'entity_id', 'ip_address'
    )
    
    # Ordre par défaut (plus récent en premier)
    ordering = ('-created_at',)
    
    # Nombre d'éléments par page
    list_per_page = 50
    
    # Tous les champs en lecture seule
    readonly_fields = (
        'id', 'user', 'action', 'entity_type', 'entity_id',
        'old_values', 'new_values', 'ip_address', 'user_agent',
        'created_at', 'updated_at'
    )
    
    # Organisation des champs
    fieldsets = (
        (_('Informations générales'), {
            'fields': (
                'id', 'created_at', 'user', 'action'
            )
        }),
        (_('Entité concernée'), {
            'fields': (
                'entity_type', 'entity_id'
            )
        }),
        (_('Modifications'), {
            'fields': (
                'old_values', 'new_values'
            )
        }),
        (_('Informations de connexion'), {
            'fields': (
                'ip_address', 'user_agent'
            )
        }),
    )
    
    # ==========================================
    # Méthodes personnalisées pour l'affichage
    # ==========================================
    
    @admin.display(description='Utilisateur')
    def user_link(self, obj):
        """Affiche un lien cliquable vers l'utilisateur."""
        if obj.user:
            url = f'/admin/core/user/{obj.user.id}/change/'
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.user.email
            )
        return '-'
    
    @admin.display(description='Action')
    def action_badge(self, obj):
        """Affiche l'action avec un badge coloré."""
        colors = {
            'CREATE': '#28a745',  # Vert
            'UPDATE': '#ffc107',  # Jaune
            'DELETE': '#dc3545',  # Rouge
            'VIEW': '#17a2b8',    # Bleu
            'ACCESS_DENIED': '#6c757d',  # Gris
        }
        color = colors.get(obj.action, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_action_display()
        )
    
    # ==========================================
    # Surcharge pour afficher tous les logs
    # ==========================================
    
    def get_queryset(self, request):
        """
        Affiche tous les logs, y compris ceux supprimés.
        Optimise avec select_related pour les foreign keys.
        """
        return AuditLog.all_objects.select_related('user').all()
    
    # ==========================================
    # Désactiver toutes les modifications
    # ==========================================
    
    def has_add_permission(self, request):
        """Les logs d'audit ne peuvent pas être créés manuellement."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Les logs d'audit ne peuvent pas être modifiés."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Les logs d'audit ne peuvent pas être supprimés."""
        return False


# ==========================================
# 3. PERSONNALISATION DU SITE ADMIN
# ==========================================

admin.site.site_header = "ENSPM Hub - Administration"
admin.site.site_title = "ENSPM Hub Admin"
admin.site.index_title = "Bienvenue sur l'interface d'administration ENSPM Hub"