"""
core/management/commands/populate_references.py
Commande Django pour remplir les données de référence
Usage: python manage.py populate_references
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    AnneePromotion, Domaine, Filiere, SecteurActivite,
    Poste, Devise, TitreHonorifique, ReseauSocial
)


class Command(BaseCommand):
    help = 'Remplit les tables de référence avec des données initiales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--table',
            type=str,
            help='Remplir une table spécifique (all, annees, domaines, filieres, secteurs, postes, devises, titres, reseaux)',
            default='all'
        )

    def handle(self, *args, **options):
        table = options['table']

        if table == 'all' or table == 'annees':
            self.populate_annees_promotion()

        if table == 'all' or table == 'domaines':
            self.populate_domaines()

        if table == 'all' or table == 'filieres':
            self.populate_filieres()

        if table == 'all' or table == 'secteurs':
            self.populate_secteurs_activite()

        if table == 'all' or table == 'postes':
            self.populate_postes()

        if table == 'all' or table == 'devises':
            self.populate_devises()

        if table == 'all' or table == 'titres':
            self.populate_titres_honorifiques()

        if table == 'all' or table == 'reseaux':
            self.populate_reseaux_sociaux()

        self.stdout.write(self.style.SUCCESS('✅ Données de référence chargées avec succès!'))

    @transaction.atomic
    def populate_annees_promotion(self):
        """Remplit les années de promotion (2000-2030)"""
        self.stdout.write('📅 Remplissage des années de promotion...')
        
        annees_data = []
        for annee in range(2009, 2025):
            annees_data.append(
                AnneePromotion(
                    annee=annee,
                    libelle=f"Promotion {annee}",
                    description=f"Promotion sortante de l'année {annee}",
                    est_active=True,
                    ordre_affichage=-annee  # Plus récent en premier
                )
            )
        
        AnneePromotion.objects.bulk_create(annees_data, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(annees_data)} années créées'))

    @transaction.atomic
    def populate_domaines(self):
        """Remplit les domaines d'études"""
        self.stdout.write('🎓 Remplissage des domaines...')
        
        domaines_data = [
            # Génie
            {'nom': 'Génie Civil', 'code': 'GCI', 'categorie': 'Génie', 'ordre': 1},
            {'nom': 'Génie Informatique', 'code': 'GIM', 'categorie': 'Génie', 'ordre': 2},
            {'nom': 'Génie Électrique', 'code': 'GEL', 'categorie': 'Génie', 'ordre': 3},
            {'nom': 'Génie Mécanique', 'code': 'GME', 'categorie': 'Génie', 'ordre': 4},
            {'nom': 'Génie Industriel', 'code': 'GIN', 'categorie': 'Génie', 'ordre': 5},
            {'nom': 'Génie Chimique', 'code': 'GCH', 'categorie': 'Génie', 'ordre': 6},
            {'nom': 'Génie des Mines', 'code': 'GMN', 'categorie': 'Génie', 'ordre': 7},
            {'nom': 'Génie Pétrolier', 'code': 'GPE', 'categorie': 'Génie', 'ordre': 8},
            {'nom': 'Génie Biomédical', 'code': 'GBM', 'categorie': 'Génie', 'ordre': 9},
            {'nom': 'Génie Environnemental', 'code': 'GEN', 'categorie': 'Génie', 'ordre': 10},
            
            # Santé
            {'nom': 'Médecine', 'code': 'MED', 'categorie': 'Santé', 'ordre': 11},
            {'nom': 'Pharmacie', 'code': 'PHA', 'categorie': 'Santé', 'ordre': 12},
            {'nom': 'Sciences Infirmières', 'code': 'INF', 'categorie': 'Santé', 'ordre': 13},
            
            # Sciences
            {'nom': 'Mathématiques', 'code': 'MAT', 'categorie': 'Sciences', 'ordre': 14},
            {'nom': 'Physique', 'code': 'PHY', 'categorie': 'Sciences', 'ordre': 15},
            {'nom': 'Chimie', 'code': 'CHI', 'categorie': 'Sciences', 'ordre': 16},
            {'nom': 'Biologie', 'code': 'BIO', 'categorie': 'Sciences', 'ordre': 17},
            
            # Gestion
            {'nom': 'Administration des Affaires', 'code': 'ADA', 'categorie': 'Gestion', 'ordre': 18},
            {'nom': 'Comptabilité', 'code': 'COM', 'categorie': 'Gestion', 'ordre': 19},
            {'nom': 'Finance', 'code': 'FIN', 'categorie': 'Gestion', 'ordre': 20},
            {'nom': 'Marketing', 'code': 'MAR', 'categorie': 'Gestion', 'ordre': 21},
            
            # Sciences Sociales
            {'nom': 'Droit', 'code': 'DRT', 'categorie': 'Sciences Sociales', 'ordre': 22},
            {'nom': 'Économie', 'code': 'ECO', 'categorie': 'Sciences Sociales', 'ordre': 23},
            {'nom': 'Sociologie', 'code': 'SOC', 'categorie': 'Sciences Sociales', 'ordre': 24},
        ]
        
        for data in domaines_data:
            Domaine.objects.get_or_create(
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'categorie': data['categorie'],
                    'est_actif': True,
                    'ordre_affichage': data['ordre']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(domaines_data)} domaines créés'))

    @transaction.atomic
    def populate_filieres(self):
        """Remplit les filières par domaine"""
        self.stdout.write('📚 Remplissage des filières...')
        
        # Filières pour Génie Informatique
        gim = Domaine.objects.get(code='GIM')
        filieres_gim = [
            {'nom': 'Intelligence Artificielle', 'code': 'IA', 'niveau': 'master', 'duree': 2},
            {'nom': 'Cybersécurité', 'code': 'CYB', 'niveau': 'master', 'duree': 2},
            {'nom': 'Développement Web', 'code': 'WEB', 'niveau': 'licence', 'duree': 3},
            {'nom': 'Data Science', 'code': 'DS', 'niveau': 'master', 'duree': 2},
            {'nom': 'Réseaux et Télécommunications', 'code': 'RT', 'niveau': 'licence', 'duree': 3},
        ]
        
        for idx, data in enumerate(filieres_gim, 1):
            Filiere.objects.get_or_create(
                domaine=gim,
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'niveau': data['niveau'],
                    'duree_annees': data['duree'],
                    'est_actif': True,
                    'ordre_affichage': idx
                }
            )
        
        # Filières pour Génie Civil
        gci = Domaine.objects.get(code='GCI')
        filieres_gci = [
            {'nom': 'Structures', 'code': 'STR', 'niveau': 'ingenieur', 'duree': 5},
            {'nom': 'Géotechnique', 'code': 'GEO', 'niveau': 'ingenieur', 'duree': 5},
            {'nom': 'Hydraulique', 'code': 'HYD', 'niveau': 'ingenieur', 'duree': 5},
            {'nom': 'Routes et Transports', 'code': 'RT', 'niveau': 'ingenieur', 'duree': 5},
        ]
        
        for idx, data in enumerate(filieres_gci, 1):
            Filiere.objects.get_or_create(
                domaine=gci,
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'niveau': data['niveau'],
                    'duree_annees': data['duree'],
                    'est_actif': True,
                    'ordre_affichage': idx
                }
            )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Filières créées'))

    @transaction.atomic
    def populate_secteurs_activite(self):
        """Remplit les secteurs d'activité"""
        self.stdout.write('🏢 Remplissage des secteurs d\'activité...')
        
        secteurs_data = [
            # Secteurs principaux
            {'nom': 'Technologie', 'code': 'TECH', 'parent': None, 'ordre': 1},
            {'nom': 'BTP & Construction', 'code': 'BTP', 'parent': None, 'ordre': 2},
            {'nom': 'Santé', 'code': 'SANTE', 'parent': None, 'ordre': 3},
            {'nom': 'Finance & Banque', 'code': 'FIN', 'parent': None, 'ordre': 4},
            {'nom': 'Éducation & Formation', 'code': 'EDU', 'parent': None, 'ordre': 5},
            {'nom': 'Énergie & Mines', 'code': 'ENER', 'parent': None, 'ordre': 6},
            {'nom': 'Agriculture & Agroalimentaire', 'code': 'AGRI', 'parent': None, 'ordre': 7},
            {'nom': 'Transport & Logistique', 'code': 'TRANS', 'parent': None, 'ordre': 8},
            {'nom': 'Commerce & Distribution', 'code': 'COM', 'parent': None, 'ordre': 9},
            {'nom': 'Télécommunications', 'code': 'TELCO', 'parent': None, 'ordre': 10},
        ]
        
        # Créer les secteurs principaux
        for data in secteurs_data:
            SecteurActivite.objects.get_or_create(
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'est_actif': True,
                    'ordre_affichage': data['ordre']
                }
            )
        
        # Sous-secteurs de Technologie
        tech = SecteurActivite.objects.get(code='TECH')
        sous_secteurs_tech = [
            {'nom': 'Développement Logiciel', 'code': 'TECH-DEV'},
            {'nom': 'Intelligence Artificielle', 'code': 'TECH-IA'},
            {'nom': 'Cybersécurité', 'code': 'TECH-CYB'},
            {'nom': 'Cloud Computing', 'code': 'TECH-CLOUD'},
        ]
        
        for idx, data in enumerate(sous_secteurs_tech, 1):
            SecteurActivite.objects.get_or_create(
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'categorie_parent': tech,
                    'est_actif': True,
                    'ordre_affichage': idx
                }
            )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Secteurs d\'activité créés'))

    @transaction.atomic
    def populate_postes(self):
        """Remplit les postes standardisés"""
        self.stdout.write('💼 Remplissage des postes...')
        
        tech_secteur = SecteurActivite.objects.get(code='TECH')
        
        postes_data = [
            # Postes techniques
            {'titre': 'Développeur Full Stack', 'categorie': 'Technique', 'niveau': 'intermediaire', 'secteur': tech_secteur},
            {'titre': 'Développeur Frontend', 'categorie': 'Technique', 'niveau': 'junior', 'secteur': tech_secteur},
            {'titre': 'Développeur Backend', 'categorie': 'Technique', 'niveau': 'junior', 'secteur': tech_secteur},
            {'titre': 'Ingénieur DevOps', 'categorie': 'Technique', 'niveau': 'senior', 'secteur': tech_secteur},
            {'titre': 'Data Scientist', 'categorie': 'Technique', 'niveau': 'senior', 'secteur': tech_secteur},
            {'titre': 'Architecte Logiciel', 'categorie': 'Technique', 'niveau': 'senior', 'secteur': tech_secteur},
            
            # Postes management
            {'titre': 'Chef de Projet', 'categorie': 'Management', 'niveau': 'manager', 'secteur': None},
            {'titre': 'Directeur Technique (CTO)', 'categorie': 'Management', 'niveau': 'c_level', 'secteur': tech_secteur},
            {'titre': 'Team Lead', 'categorie': 'Management', 'niveau': 'lead', 'secteur': None},
            
            # Postes généraux
            {'titre': 'Ingénieur Civil', 'categorie': 'Technique', 'niveau': 'intermediaire', 'secteur': None},
            {'titre': 'Consultant', 'categorie': 'Conseil', 'niveau': 'senior', 'secteur': None},
            {'titre': 'Chargé de Ressources Humaines', 'categorie': 'RH', 'niveau': 'intermediaire', 'secteur': None},
            {'titre': 'Responsable Marketing', 'categorie': 'Marketing', 'niveau': 'manager', 'secteur': None},
            {'titre': 'Comptable', 'categorie': 'Finance', 'niveau': 'intermediaire', 'secteur': None},
        ]
        
        for idx, data in enumerate(postes_data, 1):
            synonymes = []
            if 'Développeur' in data['titre']:
                synonymes = ['Dev', 'Developer', 'Programmeur']
            
            Poste.objects.get_or_create(
                titre=data['titre'],
                defaults={
                    'categorie': data['categorie'],
                    'niveau': data['niveau'],
                    'secteur': data['secteur'],
                    'synonymes': synonymes,
                    'est_actif': True,
                    'ordre_affichage': idx
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(postes_data)} postes créés'))

    @transaction.atomic
    def populate_devises(self):
        """Remplit les devises"""
        self.stdout.write('💰 Remplissage des devises...')
        
        devises_data = [
            {'code': 'XAF', 'nom': 'Franc CFA (CEMAC)', 'symbole': 'FCFA', 'taux': 655.957, 'ordre': 1},
            {'code': 'EUR', 'nom': 'Euro', 'symbole': '€', 'taux': 0.92, 'ordre': 2},
            {'code': 'USD', 'nom': 'Dollar Américain', 'symbole': '$', 'taux': 1.0, 'ordre': 3},
            {'code': 'GBP', 'nom': 'Livre Sterling', 'symbole': '£', 'taux': 0.79, 'ordre': 4},
            {'code': 'CAD', 'nom': 'Dollar Canadien', 'symbole': 'CA$', 'taux': 1.36, 'ordre': 5},
        ]
        
        for data in devises_data:
            Devise.objects.get_or_create(
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'symbole': data['symbole'],
                    'taux_change_usd': data['taux'],
                    'est_active': True,
                    'ordre_affichage': data['ordre']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(devises_data)} devises créées'))

    @transaction.atomic
    def populate_titres_honorifiques(self):
        """Remplit les titres honorifiques"""
        self.stdout.write('🎓 Remplissage des titres honorifiques...')
        
        titres_data = [
            # Civilités
            {'titre': 'M.', 'nom_complet': 'Monsieur', 'type': 'civilite', 'ordre': 1},
            {'titre': 'Mme', 'nom_complet': 'Madame', 'type': 'civilite', 'ordre': 2},
            {'titre': 'Mlle', 'nom_complet': 'Mademoiselle', 'type': 'civilite', 'ordre': 3},
            
            # Titres académiques
            {'titre': 'Dr.', 'nom_complet': 'Docteur', 'type': 'academique', 'ordre': 4},
            {'titre': 'Prof.', 'nom_complet': 'Professeur', 'type': 'academique', 'ordre': 5},
            {'titre': 'Pr.', 'nom_complet': 'Professeur', 'type': 'academique', 'ordre': 6},
            
            # Titres professionnels
            {'titre': 'Ing.', 'nom_complet': 'Ingénieur', 'type': 'professionnel', 'ordre': 7},
            {'titre': 'Me', 'nom_complet': 'Maître (Avocat)', 'type': 'professionnel', 'ordre': 8},
        ]
        
        for data in titres_data:
            TitreHonorifique.objects.get_or_create(
                titre=data['titre'],
                defaults={
                    'nom_complet': data['nom_complet'],
                    'type_titre': data['type'],
                    'est_actif': True,
                    'ordre_affichage': data['ordre']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(titres_data)} titres créés'))

    @transaction.atomic
    def populate_reseaux_sociaux(self):
        """Remplit les réseaux sociaux"""
        self.stdout.write('🌐 Remplissage des réseaux sociaux...')
        
        reseaux_data = [
            {
                'nom': 'LinkedIn',
                'code': 'linkedin',
                'url_base': 'https://linkedin.com/in/',
                'type': 'professionnel',
                'pattern': r'^https?://(?:www\.)?linkedin\.com/in/[\w-]+/?$',
                'placeholder': 'votre-nom',
                'ordre': 1
            },
            {
                'nom': 'GitHub',
                'code': 'github',
                'url_base': 'https://github.com/',
                'type': 'technique',
                'pattern': r'^https?://(?:www\.)?github\.com/[\w-]+/?$',
                'placeholder': 'username',
                'ordre': 2
            },
            {
                'nom': 'Twitter/X',
                'code': 'twitter',
                'url_base': 'https://twitter.com/',
                'type': 'social',
                'pattern': r'^https?://(?:www\.)?(?:twitter|x)\.com/[\w-]+/?$',
                'placeholder': '@username',
                'ordre': 3
            },
            {
                'nom': 'Facebook',
                'code': 'facebook',
                'url_base': 'https://facebook.com/',
                'type': 'social',
                'pattern': r'^https?://(?:www\.)?facebook\.com/[\w.-]+/?$',
                'placeholder': 'profile-name',
                'ordre': 4
            },
            {
                'nom': 'Instagram',
                'code': 'instagram',
                'url_base': 'https://instagram.com/',
                'type': 'social',
                'pattern': r'^https?://(?:www\.)?instagram\.com/[\w.]+/?$',
                'placeholder': '@username',
                'ordre': 5
            },
            {
                'nom': 'Google Scholar',
                'code': 'google_scholar',
                'url_base': 'https://scholar.google.com/citations?user=',
                'type': 'academique',
                'pattern': None,
                'placeholder': 'user-id',
                'ordre': 6
            },
            {
                'nom': 'ResearchGate',
                'code': 'researchgate',
                'url_base': 'https://researchgate.net/profile/',
                'type': 'academique',
                'pattern': None,
                'placeholder': 'Profile-Name',
                'ordre': 7
            },
            {
                'nom': 'Site Web Personnel',
                'code': 'website',
                'url_base': 'https://',
                'type': 'portfolio',
                'pattern': r'^https?://[\w.-]+\.[a-z]{2,}',
                'placeholder': 'monsite.com',
                'ordre': 8
            },
        ]
        
        for data in reseaux_data:
            ReseauSocial.objects.get_or_create(
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'url_base': data['url_base'],
                    'type_reseau': data['type'],
                    'pattern_validation': data['pattern'],
                    'placeholder_exemple': data['placeholder'],
                    'est_actif': True,
                    'ordre_affichage': data['ordre']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(reseaux_data)} réseaux sociaux créés'))