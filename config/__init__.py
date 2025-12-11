"""
==============================================================================
MODULE CONFIG - INITIALISATION
==============================================================================
Ce fichier __init__.py permet d'importer facilement les configurations.

Usage:
    from config import settings
    from config import CATEGORIES_APPELS, COULEURS_CAMEROUN
    
Au lieu de:
    from config.settings import APP_CONFIG, CATEGORIES_APPELS, etc.

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

# Import du module settings complet
from config import settings

# Exports directs des configurations les plus utilisées
from config.settings import (
    # Configuration application
    APP_CONFIG,
    
    # Chemins
    BASE_DIR,
    DATA_DIR,
    LOGS_DIR,
    ASSETS_DIR,
    OUTPUTS_DIR,
    BACKUPS_DIR,
    
    # Catégories et labels
    CATEGORIES_APPELS,
    LABELS_CATEGORIES,
    REGROUPEMENTS,
    LABELS_REGROUPEMENTS,
    
    # Couleurs
    COULEURS_CAMEROUN,
    COULEURS_GRAPHIQUES,
    
    # Configurations
    PLOTLY_CONFIG,
    PLOTLY_TEMPLATE,
    GRAPH_CONFIG,
    CACHE_CONFIG,
    LOGGING_CONFIG,
    MESSAGES,
    
    # Fonctions utilitaires
    get_config,
    get_color,
    get_label_categorie
)

# Version du module
__version__ = '2.0'
__author__ = 'Fred - AIMS Cameroon'

# Liste des exports publics
__all__ = [
    'settings',
    'APP_CONFIG',
    'BASE_DIR',
    'DATA_DIR',
    'LOGS_DIR',
    'ASSETS_DIR',
    'OUTPUTS_DIR',
    'BACKUPS_DIR',
    'CATEGORIES_APPELS',
    'LABELS_CATEGORIES',
    'REGROUPEMENTS',
    'LABELS_REGROUPEMENTS',
    'COULEURS_CAMEROUN',
    'COULEURS_GRAPHIQUES',
    'PLOTLY_CONFIG',
    'PLOTLY_TEMPLATE',
    'GRAPH_CONFIG',
    'CACHE_CONFIG',
    'LOGGING_CONFIG',
    'MESSAGES',
    'get_config',
    'get_color',
    'get_label_categorie'
]