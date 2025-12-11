"""
==============================================================================
CONFIGURATION CENTRALE DU DASHBOARD
==============================================================================
Fichier de configuration centralisé pour le Dashboard Centre d'Appels 
d'Urgence Sanitaire - MINSANTE Cameroun

Ce fichier contient :
- Configuration de l'application
- Chemins des fichiers de données
- Définition des catégories d'appels
- Regroupements thématiques
- Paramètres visuels (couleurs, formats)
- Configuration des logs et du cache
- Messages système

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.1 - Ajout chargement drapeau
==============================================================================
"""

import os
from pathlib import Path
import base64

# ==============================================================================
# CHEMINS DES FICHIERS
# ==============================================================================

# Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Répertoires de données
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"
OUTPUTS_DIR = BASE_DIR / "outputs"
BACKUPS_DIR = DATA_DIR / "backups"

# Création automatique des répertoires si nécessaire
for directory in [DATA_DIR, LOGS_DIR, ASSETS_DIR, OUTPUTS_DIR, BACKUPS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# FONCTION POUR CHARGER LE DRAPEAU
# ==============================================================================

def load_drapeau_cameroun():
    """
    Charge l'image du drapeau du Cameroun en base64.
    Cherche d'abord le fichier SVG, puis PNG, puis retourne l'emoji.
    
    Returns:
        str: HTML img tag avec base64 ou emoji
    """
    # Liste des fichiers à chercher (ordre de priorité)
    drapeau_files = [
        DATA_DIR / "Flag_of_Cameroon.svg",
        DATA_DIR / "drapeau_cameroun.svg",
        DATA_DIR / "Flag_of_Cameroon.png",
        DATA_DIR / "drapeau_cameroun.png"
    ]
    
    for drapeau_path in drapeau_files:
        if drapeau_path.exists():
            try:
                with open(drapeau_path, "rb") as img_file:
                    base64_image = base64.b64encode(img_file.read()).decode()
                    
                    # Déterminer le type MIME
                    if drapeau_path.suffix == '.svg':
                        mime_type = 'image/svg+xml'
                    elif drapeau_path.suffix == '.png':
                        mime_type = 'image/png'
                    else:
                        mime_type = 'image/png'
                    
                    return f'<img src="data:{mime_type};base64,{base64_image}" width="32" height="32" style="vertical-align: middle; margin-right: 8px;" alt="Drapeau Cameroun">'
            except Exception as e:
                print(f"Erreur lors du chargement du drapeau depuis {drapeau_path}: {e}")
                continue
    
    # Fallback sur emoji si aucun fichier trouvé
    return "🇨🇲"

# Charger le drapeau une fois au démarrage
DRAPEAU_CAMEROUN = load_drapeau_cameroun()
DRAPEAU_EMOJI = "🇨🇲"  # Backup emoji

# ==============================================================================
# CONFIGURATION DE L'APPLICATION
# ==============================================================================

APP_CONFIG = {
    'page_title': 'Dashboard Centre d\'Appels d\'Urgence Sanitaire - MINSANTE',
    'page_icon': '🏥',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'version': '2.1',
    'author': 'Fred - AIMS Cameroon',
    'organisation': 'MINSANTE - République du Cameroun',
    'contact': 'centre.appel@minsante.cm',
    'year': 2025
}

# Fichiers de données (détection automatique ou chemins par défaut)
CHEMINS_FICHIERS = {
    'appels': str(DATA_DIR / "Appels_hebdomadaires (1).xlsx"),
    'calendrier': str(DATA_DIR / "CALENDRIER_EPIDEMIOLOGIQUE_2025_cm.xlsx")
}

# Noms des feuilles Excel
SHEET_APPELS = "BASE_DONNEES_APPELS_Net"
SHEET_CALENDRIER = "Table 1"

# ==============================================================================
# CATÉGORIES D'APPELS (17 CATÉGORIES) - NOMS RÉELS DU FICHIER EXCEL
# ==============================================================================

CATEGORIES_APPELS = [
    "CSU_JOUR",
    "PHARMACIE_JOUR",
    "STRUCTURE_REFERENCE_JOUR",
    "PROGRAMME_SANTE_JOUR",
    "RUMEURS_JOUR",
    "PROBLEMATIQUE_SANTE_JOUR",
    "URGENCE_MEDICALE_JOUR",
    "GESTION_MALADIE_JOUR",
    "AUTRES_JOUR",
    "SOCIAL_JOUR",
    "SECURITAIRE_JOUR",
    "PSYCHO_JOUR",
    "SIGNAUX_SFE_JOUR",
    "AUTRES_SANTE_PUBLIQUE_JOUR",
    "CAS_SUSPECTS_JOUR",
    "FARCES_JOUR",
    "HARCELEMENTS_JOUR"
]

# ==============================================================================
# LABELS DES CATÉGORIES (TRADUCTION LISIBLE)
# ==============================================================================

LABELS_CATEGORIES = {
    "CSU_JOUR": "Couverture Santé Universelle",
    "PHARMACIE_JOUR": "Informations Pharmacie",
    "STRUCTURE_REFERENCE_JOUR": "Structures de Référence",
    "PROGRAMME_SANTE_JOUR": "Programmes de Santé",
    "RUMEURS_JOUR": "Rumeurs Sanitaires",
    "PROBLEMATIQUE_SANTE_JOUR": "Problématiques de Santé",
    "URGENCE_MEDICALE_JOUR": "Urgences Médicales",
    "GESTION_MALADIE_JOUR": "Gestion de Maladies",
    "AUTRES_JOUR": "Autres Appels",
    "SOCIAL_JOUR": "Questions Sociales",
    "SECURITAIRE_JOUR": "Questions Sécuritaires",
    "PSYCHO_JOUR": "Soutien Psychologique",
    "SIGNAUX_SFE_JOUR": "Signaux de Surveillance Épidémiologique",
    "AUTRES_SANTE_PUBLIQUE_JOUR": "Autres Santé Publique",
    "CAS_SUSPECTS_JOUR": "Cas Suspects",
    "FARCES_JOUR": "Appels Farces",
    "HARCELEMENTS_JOUR": "Appels de Harcèlement"
}

# ==============================================================================
# REGROUPEMENTS THÉMATIQUES (5 GROUPES)
# ==============================================================================

REGROUPEMENTS = {
    'Renseignements Santé': [
        'CSU_JOUR',
        'PHARMACIE_JOUR',
        'STRUCTURE_REFERENCE_JOUR',
        'PROGRAMME_SANTE_JOUR',
        'RUMEURS_JOUR',
        'PROBLEMATIQUE_SANTE_JOUR'
    ],
    'Assistances Médicales': [
        'URGENCE_MEDICALE_JOUR',
        'GESTION_MALADIE_JOUR',
        'AUTRES_JOUR'
    ],
    'Assistances Psycho-Sociales': [
        'SOCIAL_JOUR',
        'SECURITAIRE_JOUR',
        'PSYCHO_JOUR'
    ],
    'Signaux': [
        'SIGNAUX_SFE_JOUR',
        'AUTRES_SANTE_PUBLIQUE_JOUR',
        'CAS_SUSPECTS_JOUR'
    ],
    'Autres Appels': [
        'FARCES_JOUR',
        'HARCELEMENTS_JOUR'
    ]
}

# Labels des regroupements (pour affichage)
LABELS_REGROUPEMENTS = {
    'Renseignements Santé': 'Renseignements Santé',
    'Assistances Médicales': 'Assistances Médicales',
    'Assistances Psycho-Sociales': 'Assistances Psycho-Sociales',
    'Signaux': 'Signaux d\'Alerte',
    'Autres Appels': 'Autres Appels'
}

# Labels courts pour regroupements (pour graphiques)
LABELS_REGROUPEMENTS_COURTS = {
    'Renseignements Santé': 'Renseignements',
    'Assistances Médicales': 'Assistances Méd.',
    'Assistances Psycho-Sociales': 'Psycho-Social',
    'Signaux': 'Signaux',
    'Autres Appels': 'Autres'
}

# ==============================================================================
# COULEURS ET IDENTITÉ VISUELLE
# ==============================================================================

# Couleurs officielles du Cameroun
COULEURS_CAMEROUN = {
    'vert': '#007A33',      # Vert du drapeau
    'jaune': '#FFD700',     # Jaune du drapeau
    'rouge': '#CE1126',     # Rouge du drapeau
    'blanc': '#FFFFFF',
    'gris': '#6c757d',
    'gris_clair': '#f8f9fa',
    'noir': '#000000'
}

# Palette de couleurs pour les graphiques
COULEURS_GRAPHIQUES = [
    '#007A33',  # Vert
    '#FFD700',  # Jaune
    '#28a745',  # Vert clair
    '#ffc107',  # Jaune foncé
    '#17a2b8',  # Cyan
    '#6c757d',  # Gris
    '#20c997',  # Teal
    '#fd7e14',  # Orange
    '#e83e8c',  # Rose
    '#6f42c1',  # Violet
    '#007bff',  # Bleu
    '#dc3545',  # Rouge
    '#1E90FF',  # Bleu dodger
    '#32CD32',  # Vert lime
    '#FF8C00',  # Orange foncé
    '#9370DB',  # Violet moyen
    '#20B2AA'   # Turquoise clair
]

# Couleurs pour les regroupements
COULEURS_REGROUPEMENTS = {
    'Renseignements Santé': '#007A33',
    'Assistances Médicales': '#FFD700',
    'Assistances Psycho-Sociales': '#17a2b8',
    'Signaux': '#CE1126',
    'Autres Appels': '#6c757d'
}

# ==============================================================================
# FORMATS ET AFFICHAGE
# ==============================================================================

# Format de date
FORMAT_DATE = "%d/%m/%Y"
FORMAT_DATE_LONG = "%d %B %Y"
FORMAT_DATE_HEURE = "%d/%m/%Y %H:%M:%S"

# Format des nombres
FORMAT_NOMBRE_MILLIERS = " "  # Séparateur de milliers (espace)
FORMAT_NOMBRE_DECIMALES = 2

# Mois en français
MOIS_FRANCAIS = {
    1: "Janvier",
    2: "Février", 
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
}

# Jours en français
JOURS_FRANCAIS = {
    0: "Lundi",
    1: "Mardi",
    2: "Mercredi",
    3: "Jeudi",
    4: "Vendredi",
    5: "Samedi",
    6: "Dimanche"
}

# ==============================================================================
# CONFIGURATION PLOTLY
# ==============================================================================

PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': [
        'pan2d',
        'select2d',
        'lasso2d',
        'autoScale2d',
        'toggleSpikelines'
    ],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'graphique_minsante',
        'height': 800,
        'width': 1200,
        'scale': 2
    },
    'locale': 'fr'
}

# Template par défaut pour les graphiques
PLOTLY_TEMPLATE = 'plotly_white'

# Configuration des graphiques
GRAPH_CONFIG = {
    'font_family': 'Arial, sans-serif',
    'font_size': 12,
    'title_font_size': 16,
    'height': 500,
    'margin': {'l': 80, 'r': 80, 't': 80, 'b': 80}
}

# ==============================================================================
# CONFIGURATION DU CACHE
# ==============================================================================

CACHE_CONFIG = {
    'ttl': 3600,  # Time To Live : 1 heure (3600 secondes)
    'max_entries': 100,  # Nombre maximum d'entrées en cache
    'show_spinner': True,
    'spinner_text': '🔄 Chargement des données en cours...'
}

# ==============================================================================
# CONFIGURATION DES LOGS
# ==============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',  # Niveaux : DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,  # Nombre de fichiers de backup
    'log_file': str(LOGS_DIR / 'dashboard.log'),
    'encoding': 'utf-8'
}

# ==============================================================================
# MESSAGES SYSTÈME
# ==============================================================================

MESSAGES = {
    # Messages de succès
    'success': {
        'data_loaded': '✅ Données chargées avec succès',
        'file_uploaded': '✅ Fichier uploadé avec succès',
        'backup_created': '✅ Sauvegarde créée avec succès',
        'report_generated': '✅ Rapport généré avec succès',
        'export_success': '✅ Export réussi'
    },
    
    # Messages d'erreur
    'error': {
        'file_not_found': '❌ Fichier introuvable',
        'invalid_format': '❌ Format de fichier invalide',
        'missing_columns': '❌ Colonnes manquantes dans le fichier',
        'data_inconsistency': '❌ Incohérence détectée dans les données',
        'upload_failed': '❌ Échec de l\'upload',
        'generation_failed': '❌ Échec de la génération',
        'export_failed': '❌ Échec de l\'export'
    },
    
    # Messages d'avertissement
    'warning': {
        'no_data': '⚠️ Aucune donnée disponible',
        'partial_data': '⚠️ Données incomplètes',
        'old_data': '⚠️ Les données datent de plus de 7 jours',
        'large_file': '⚠️ Fichier volumineux, le traitement peut prendre du temps'
    },
    
    # Messages d'information
    'info': {
        'loading': 'ℹ️ Chargement en cours...',
        'processing': 'ℹ️ Traitement en cours...',
        'select_option': 'ℹ️ Veuillez sélectionner une option',
        'no_filter': 'ℹ️ Aucun filtre appliqué'
    }
}

# ==============================================================================
# PARAMÈTRES DES PAGES
# ==============================================================================

PAGES_CONFIG = {
    'accueil': {
        'title': 'Accueil',
        'icon': '🏠',
        'description': 'Vue d\'ensemble du centre d\'appels'
    },
    'vue_ensemble': {
        'title': 'Vue d\'Ensemble',
        'icon': '👁️',
        'description': 'Analyse de la dernière semaine'
    },
    'analyse_epidemiologique': {
        'title': 'Analyse Épidémiologique',
        'icon': '🔬',
        'description': 'Analyse détaillée par semaine'
    },
    'comparaisons': {
        'title': 'Comparaisons Temporelles',
        'icon': '📊',
        'description': 'Comparaisons et tendances'
    },
    'donnees_brutes': {
        'title': 'Données Brutes',
        'icon': '📋',
        'description': 'Consultation et export des données'
    },
    'generation_rapports': {
        'title': 'Génération de Rapports',
        'icon': '📄',
        'description': 'Rapports PowerPoint MINSANTE'
    }
}

# ==============================================================================
# PARAMÈTRES DES RAPPORTS POWERPOINT
# ==============================================================================

PPTX_CONFIG = {
    'models': {
        'ORIGINAL': {
            'name': 'Modèle Original',
            'slides': 7,
            'description': 'Format standard MINSANTE',
            'filename_prefix': 'Situation_Centre_Appel'
        },
        'A': {
            'name': 'Modèle A - Amélioré',
            'slides': 16,
            'description': 'Analyse approfondie avec graphiques avancés',
            'filename_prefix': 'Rapport_Avance_A'
        },
        'B': {
            'name': 'Modèle B - Nouvelle Version',
            'slides': 12,
            'description': 'Design moderne professionnel',
            'filename_prefix': 'Rapport_Avance_B'
        }
    },
    'format': {
        'width': 10,  # pouces
        'height': 7.5,  # pouces (16:9)
    }
}

# ==============================================================================
# PARAMÈTRES D'EXPORT
# ==============================================================================

EXPORT_CONFIG = {
    'csv': {
        'encoding': 'utf-8-sig',
        'sep': ',',
        'index': False
    },
    'excel': {
        'engine': 'openpyxl',
        'index': False,
        'sheet_name': 'Données'
    },
    'max_rows_display': 1000,  # Limite d'affichage pour les gros datasets
}

# ==============================================================================
# PARAMÈTRES DE VALIDATION
# ==============================================================================

VALIDATION_CONFIG = {
    'max_file_size': 50 * 1024 * 1024,  # 50 MB
    'allowed_extensions': ['.xlsx', '.xls', '.csv'],
    'required_columns_appels': ['DATE'] + CATEGORIES_APPELS,
    'required_columns_calendrier': ['DATE', 'Semaine épidémiologique'],
    'min_rows': 1,
    'max_rows': 100000
}

# ==============================================================================
# STATISTIQUES ET SEUILS
# ==============================================================================

STATS_CONFIG = {
    'nb_top_categories': 10,  # Nombre de catégories à afficher dans les tops
    'nb_semaines_evolution': 10,  # Nombre de semaines pour graphique évolution
    'seuil_alerte_hausse': 20,  # % d'augmentation considérée comme alerte
    'seuil_alerte_baisse': -20,  # % de diminution considérée comme alerte
    'percentiles': [25, 50, 75, 90, 95]  # Percentiles pour analyses statistiques
}

# ==============================================================================
# TEXTES ET TEMPLATES
# ==============================================================================

TEMPLATES = {
    'copyright': f"© {APP_CONFIG['year']} MINSANTE - République du Cameroun",
    'credits': f"Développé par {APP_CONFIG['author']}",
    'footer': f"{DRAPEAU_EMOJI} Dashboard Centre d'Appels d'Urgence Sanitaire",
    'email_subject': "Rapport Centre d'Appels - MINSANTE",
    'no_data_message': "Aucune donnée disponible pour cette période"
}

# ==============================================================================
# AIDE ET DOCUMENTATION
# ==============================================================================

HELP_TEXTS = {
    'semaine_epidemiologique': """
    **Semaine Épidémiologique :** 
    Format : S[numéro]_[année] (ex: S10_2025)
    Période du lundi au dimanche selon le calendrier épidémiologique international.
    """,
    
    'categories_appels': """
    **Catégories d'Appels :**
    Le système classe les appels en 17 catégories principales regroupées en 5 thématiques :
    - Renseignements Santé
    - Assistances Médicales  
    - Assistances Psycho-Sociales
    - Signaux d'Alerte
    - Autres Appels
    """,
    
    'export': """
    **Export des Données :**
    - CSV : Format texte compatible Excel
    - Excel : Format natif avec mise en forme
    Les fichiers exportés contiennent toutes les données filtrées.
    """,
    
    'upload': """
    **Upload de Fichiers :**
    - Format accepté : .xlsx uniquement
    - Taille maximale : 50 MB
    - Une sauvegarde automatique est créée avant toute mise à jour
    """
}

# ==============================================================================
# CONFIGURATION AVANCÉE (OPTIONNEL)
# ==============================================================================

ADVANCED_CONFIG = {
    'enable_caching': True,
    'enable_logging': True,
    'enable_error_tracking': True,
    'enable_performance_monitoring': False,
    'debug_mode': False,
    'show_warnings': True,
    'auto_refresh': False,
    'refresh_interval': 300  # secondes
}

# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def get_config(key, default=None):
    """
    Récupère une valeur de configuration.
    
    Args:
        key (str): Clé de configuration (ex: 'APP_CONFIG.version')
        default: Valeur par défaut si la clé n'existe pas
        
    Returns:
        La valeur de configuration ou la valeur par défaut
    """
    try:
        parts = key.split('.')
        value = globals()[parts[0]]
        for part in parts[1:]:
            value = value[part]
        return value
    except (KeyError, TypeError):
        return default

def get_color(color_name):
    """
    Récupère une couleur par son nom.
    
    Args:
        color_name (str): Nom de la couleur
        
    Returns:
        str: Code couleur hexadécimal
    """
    return COULEURS_CAMEROUN.get(color_name, COULEURS_CAMEROUN['vert'])

def get_label_categorie(categorie_code):
    """
    Récupère le label d'une catégorie d'appel.
    
    Args:
        categorie_code (str): Code de la catégorie (ex: 'CSU_JOUR')
        
    Returns:
        str: Label lisible de la catégorie
    """
    return LABELS_CATEGORIES.get(categorie_code, categorie_code)

# ==============================================================================
# FIN DU FICHIER DE CONFIGURATION
# ==============================================================================