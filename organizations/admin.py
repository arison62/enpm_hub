# organizations/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from organizations.models import Organisation, MembreOrganisation, AbonnementOrganisation

# ==========================================
# 1. INLINE POUR MEMBRE ORGANISATION DANS ORGANISATION ADMIN
# ==========================================
class MembreOrganisationInline(admin.TabularInline):
    model = MembreOrganisation
    extra = 1
    fields = ('profil', 'role_organisation', 'poste', 'est_actif')
    readonly_fields = ('date_joindre',)
    verbose_name_plural = _('Membres de l\'organisation')

# ==========================================
# 2. ADMIN ORGANISATION
# ==========================================
@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Organisation.
    Les membres sont gérés via inline.
    """
    list_display = (
        'nom_organisation', 'type_organisation', 'statut_badge',
        'pays', 'created_at', 'deleted_badge'
    )
    list_filter = (
        'type_organisation', 'statut', 'pays', 'deleted',
        'created_at'
    )
    search_fields = ('nom_organisation', 'secteur_activite__nom', 'email_general')
    ordering = ('-created_at',)
    list_per_page = 25
    list_display_links = ('nom_organisation',)

    inlines = [MembreOrganisationInline]

    actions = ['activate_organisations', 'deactivate_organisations', 'soft_delete_organisations', 'restore_organisations']

    fieldsets = (
        (_('Informations générales'), {
            'fields': ('nom_organisation', 'type_organisation', 'secteur_activite', 'description')
        }),
        (_('Coordonnées'), {
            'fields': ('adresse', 'ville', 'pays', 'email_general', 'telephone_general')
        }),
        (_('Visuel et statut'), {
            'fields': ('logo_preview', 'logo', 'statut', 'date_creation')
        }),
        (_('Métadonnées'), {
            'fields': ('id', 'created_at', 'updated_at', 'deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at', 'logo_preview')

    # ======================================
    # Méthodes personnalisées
    # ======================================
    @admin.display(description='Statut', boolean=False)
    def statut_badge(self, obj):
        colors = {
            'active': '#28a745',
            'inactive': '#dc3545',
            'en_attente': '#ffc107',
        }
        color = colors.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_statut_display()
        )

    @admin.display(description='Supprimé', boolean=True)
    def deleted_badge(self, obj):
        return obj.deleted

    @admin.display(description=_('Aperçu du logo'))
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: contain;" />', obj.logo.url)
        return _('Aucun logo')

    # ======================================
    # Actions personnalisées
    # ======================================
    @admin.action(description='Activer les organisations sélectionnées')
    def activate_organisations(self, request, queryset):
        updated = queryset.update(statut='active')
        self.message_user(request, f'{updated} organisation(s) activée(s).')

    @admin.action(description='Désactiver les organisations sélectionnées')
    def deactivate_organisations(self, request, queryset):
        updated = queryset.update(statut='inactive')
        self.message_user(request, f'{updated} organisation(s) désactivée(s).')

    @admin.action(description='Supprimer logiquement les organisations')
    def soft_delete_organisations(self, request, queryset):
        count = 0
        for org in queryset.filter(deleted=False):
            org.soft_delete()
            count += 1
        self.message_user(request, f'{count} organisation(s) supprimée(s) logiquement.')

    @admin.action(description='Restaurer les organisations supprimées')
    def restore_organisations(self, request, queryset):
        count = 0
        for org in queryset.filter(deleted=True):
            org.restore()
            count += 1
        self.message_user(request, f'{count} organisation(s) restaurée(s).')

    # ======================================
    # Optimisations
    # ======================================
    def get_queryset(self, request):
        return Organisation.all_objects.select_related('secteur_activite').all()

# ==========================================
# 3. ADMIN MEMBRE ORGANISATION
# ==========================================
@admin.register(MembreOrganisation)
class MembreOrganisationAdmin(admin.ModelAdmin):
    """
    Administration pour les membres des organisations.
    """
    list_display = (
        'profil_link', 'organisation_link', 'role_organisation_badge',
        'poste', 'est_actif_badge', 'date_joindre'
    )
    list_filter = ('role_organisation', 'est_actif', 'date_joindre')
    search_fields = ('profil__nom_complet', 'organisation__nom_organisation', 'poste__nom')
    ordering = ('-date_joindre',)
    list_per_page = 50

    fieldsets = (
        (_('Informations principales'), {
            'fields': ('profil', 'organisation', 'role_organisation', 'poste')
        }),
        (_('Statut'), {
            'fields': ('est_actif',)
        }),
        (_('Dates'), {
            'fields': ('date_joindre', 'created_at', 'updated_at')
        }),
        (_('Métadonnées'), {
            'fields': ('deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('date_joindre', 'created_at', 'updated_at', 'deleted_at')

    # ======================================
    # Méthodes d'affichage personnalisées
    # ======================================
    @admin.display(description='Profil')
    def profil_link(self, obj):
        if obj.profil:
            url = f'/admin/users/profil/{obj.profil.id}/change/'  # Assuming core app has ProfilAdmin
            return format_html('<a href="{}">{}</a>', url, obj.profil.nom_complet)
        return '-'

    @admin.display(description='Organisation')
    def organisation_link(self, obj):
        if obj.organisation:
            url = f'/admin/organizations/organisation/{obj.organisation.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.organisation.nom_organisation)
        return '-'

    @admin.display(description='Rôle')
    def role_organisation_badge(self, obj):
        colors = {
            'employe': '#17a2b8',
            'administrateur_page': '#28a745',
        }
        color = colors.get(obj.role_organisation, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_role_organisation_display()
        )

    @admin.display(description='Actif', boolean=True)
    def est_actif_badge(self, obj):
        return obj.est_actif

    def get_queryset(self, request):
        return MembreOrganisation.all_objects.select_related('profil', 'organisation', 'poste').all()

# ==========================================
# 4. ADMIN ABONNEMENT ORGANISATION
# ==========================================
@admin.register(AbonnementOrganisation)
class AbonnementOrganisationAdmin(admin.ModelAdmin):
    """
    Administration pour les abonnements aux organisations.
    """
    list_display = (
        'profil_link', 'organisation_link', 'date_abonnement'
    )
    list_filter = ('date_abonnement',)
    search_fields = ('profil__nom_complet', 'organisation__nom_organisation')
    ordering = ('-date_abonnement',)
    list_per_page = 50

    fieldsets = (
        (_('Informations'), {
            'fields': ('profil', 'organisation', 'date_abonnement')
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at', 'deleted', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('date_abonnement', 'created_at', 'updated_at', 'deleted_at')

    # ======================================
    # Méthodes d'affichage personnalisées
    # ======================================
    @admin.display(description='Profil')
    def profil_link(self, obj):
        if obj.profil:
            url = f'/admin/users/profil/{obj.profil.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.profil.nom_complet)
        return '-'

    @admin.display(description='Organisation')
    def organisation_link(self, obj):
        if obj.organisation:
            url = f'/admin/organizations/organisation/{obj.organisation.id}/change/'
            return format_html('<a href="{}">{}</a>', url, obj.organisation.nom_organisation)
        return '-'

    def get_queryset(self, request):
        return AbonnementOrganisation.all_objects.select_related('profil', 'organisation').all()

    def has_add_permission(self, request): return True  # Allow adding, but perhaps restrict in production
    def has_change_permission(self, request, obj=None): return True
    def has_delete_permission(self, request, obj=None): return True