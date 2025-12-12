# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from core.models import User, Profil, AuditLog


# ==========================================
# 1. INLINE POUR PROFIL DANS USER ADMIN
# ==========================================
class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = _('Profil')
    fk_name = 'user'
    fields = (
        'nom_complet', 'matricule', 'titre', 'statut_global',
        'travailleur', 'annee_sortie', 'telephone', 'domaine',
        'bio', 'photo_profil'
    )
    readonly_fields = ('id', 'created_at', 'updated_at')


# ==========================================
# 2. ADMIN UTILISATEUR (AUTHENTIFICATION)
# ==========================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration pour le modèle User (authentification).
    Le Profil est géré via inline.
    """
    list_display = (
        'email', 'role_systeme', 'est_actif_badge',
        'last_login', 'created_at', 'deleted_badge'
    )
    list_filter = (
        'role_systeme', 'est_actif', 'deleted',
        'is_staff', 'is_superuser', 'created_at'
    )
    search_fields = ('email',)
    ordering = ('-created_at',)
    list_per_page = 25
    list_display_links = ('email',)

    inlines = [ProfilInline]

    actions = ['activate_users', 'deactivate_users', 'soft_delete_users', 'restore_users']

    fieldsets = (
        (_('Informations de connexion'), {
            'fields': ('email', 'password')
        }),
        (_('Rôle et permissions'), {
            'fields': ('role_systeme', 'est_actif', 'is_staff', 'is_superuser'),
        }),
        (_('Métadonnées'), {
            'fields': ('id', 'last_login', 'created_at', 'updated_at', 'deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (_('Informations de connexion'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role_systeme'),
        }),
    )

    readonly_fields = ('id', 'last_login', 'created_at', 'updated_at', 'deleted_at')

    # ======================================
    # Méthodes personnalisées
    # ======================================
    @admin.display(description='Actif', boolean=True)
    def est_actif_badge(self, obj):
        return obj.est_actif and not obj.deleted

    @admin.display(description='Supprimé', boolean=True)
    def deleted_badge(self, obj):
        return obj.deleted

    # ======================================
    # Actions personnalisées
    # ======================================
    @admin.action(description='Activer les utilisateurs sélectionnés')
    def activate_users(self, request, queryset):
        updated = queryset.update(est_actif=True)
        self.message_user(request, f'{updated} utilisateur(s) activé(s).')

    @admin.action(description='Désactiver les utilisateurs sélectionnés')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(est_actif=False)
        self.message_user(request, f'{updated} utilisateur(s) désactivé(s).')

    @admin.action(description='Supprimer logiquement les utilisateurs')
    def soft_delete_users(self, request, queryset):
        count = 0
        for user in queryset.filter(deleted=False):
            user.soft_delete()
            if hasattr(user, 'profil'):
                user.profil.soft_delete()
            count += 1
        self.message_user(request, f'{count} utilisateur(s) supprimé(s) logiquement.')

    @admin.action(description='Restaurer les utilisateurs supprimés')
    def restore_users(self, request, queryset):
        count = 0
        for user in queryset.filter(deleted=True):
            user.restore()
            if hasattr(user, 'profil'):
                user.profil.restore()
            count += 1
        self.message_user(request, f'{count} utilisateur(s) restauré(s).')

    # ======================================
    # Afficher tous les users (y compris soft-deleted)
    # ======================================
    def get_queryset(self, request):
        return User.all_objects.all()

    # Désactiver suppression permanente
    def has_delete_permission(self, request, obj=None):
        return False


# ==========================================
# 3. ADMIN PROFIL (DONNÉES MÉTIER)
# ==========================================
@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = (
        'nom_complet', 'user_email', 'matricule', 'statut_global',
        'travailleur_badge', 'photo_thumbnail', 'created_at'
    )
    list_filter = ('statut_global', 'travailleur', 'created_at', 'deleted')
    search_fields = ('nom_complet', 'matricule', 'user__email', 'telephone', 'domaine')
    ordering = ('-created_at',)
    list_per_page = 25
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    fieldsets = (
        (_('Lien utilisateur'), {
            'fields': ('user',)
        }),
        (_('Informations personnelles'), {
            'fields': ('nom_complet', 'matricule', 'titre', 'telephone', 'bio', 'photo_profil')
        }),
        (_('Statut et domaine'), {
            'fields': ('statut_global', 'domaine', 'annee_sortie', 'travailleur')
        }),
        (_('Métadonnées'), {
            'fields': ('id', 'created_at', 'updated_at', 'deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email if obj.user else '-'
    user_email.short_description = _('Email')

    @admin.display(description='Travailleur', boolean=True)
    def travailleur_badge(self, obj):
        return obj.travailleur

    @admin.display(description='Photo')
    def photo_thumbnail(self, obj):
        if obj.photo_profil:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.photo_profil
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 50%; '
            'background-color: #e0e0e0; display: flex; align-items: center; '
            'justify-content: center; color: #666; font-size: 12px;">N/A</div>'
        )
    photo_thumbnail.short_description = _('Photo')

    def get_queryset(self, request):
        return Profil.all_objects.select_related('user').all()

    def has_delete_permission(self, request, obj=None):
        return False


# ==========================================
# 4. ADMIN AUDIT LOG (VERSION CORRIGÉE)
# ==========================================
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Administration du journal d'audit - Lecture seule.
    """
    list_display = (
        'created_at', 'user_link', 'action_badge', 'entity_type', 'entity_id_short', 'ip_address'
    )
    list_filter = ('action', 'entity_type', 'created_at')
    search_fields = ('user__email', 'entity_type', 'entity_id', 'ip_address', 'user_agent')
    ordering = ('-created_at',)
    list_per_page = 50

    readonly_fields = (
        'id', 'user', 'action', 'entity_type', 'entity_id',
        'old_values', 'new_values', 'ip_address', 'user_agent',
        'created_at', 'updated_at'
    )

    fieldsets = (
        (_('Informations générales'), {
            'fields': ('id', 'created_at', 'user', 'action')
        }),
        (_('Entité concernée'), {
            'fields': ('entity_type', 'entity_id')
        }),
        (_('Modifications'), {
            'fields': ('old_values', 'new_values'),
            'classes': ('collapse',)
        }),
        (_('Contexte technique'), {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    # ======================================
    # Méthodes d'affichage personnalisées
    # ======================================
    @admin.display(description='Utilisateur')
    def user_link(self, obj):
        if obj.user:
            url = f'/admin/core/user/{obj.user.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return '-'

    @admin.display(description='Action')
    def action_badge(self, obj):
        colors = {
            'CREATE': '#28a745',
            'UPDATE': '#ffc107',
            'DELETE': '#dc3545',
            'VIEW': '#17a2b8',
            'ACCESS_DENIED': '#6c757d',
        }
        color = colors.get(obj.action, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_action_display()
        )

    @admin.display(description='ID Entité')
    def entity_id_short(self, obj):
        return str(obj.entity_id)[:8] + '...'

    # ======================================
    # Optimisations et sécurité
    # ======================================
    def get_queryset(self, request):
        return AuditLog.all_objects.select_related('user').all()

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
    
    
# ==========================================
# 5. PERSONNALISATION GLOBALE DU SITE ADMIN
# ==========================================
admin.site.site_header = "ENSPM Hub - Administration"
admin.site.site_title = "ENSPM Hub Admin"
admin.site.index_title = "Bienvenue sur l'interface d'administration ENSPM Hub"