"""
==============================================================================
MODULE UTILS - INITIALISATION
==============================================================================
Ce fichier __init__.py permet d'importer facilement les utilitaires.

Usage:
    from utils import charger_toutes_les_donnees, calculer_totaux_semaine
    from utils import formater_nombre, extraire_numero_semaine
    
Au lieu de:
    from utils.data_loader import charger_toutes_les_donnees
    from utils.data_processor import calculer_totaux_semaine
    from utils.helpers import formater_nombre, extraire_numero_semaine

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

# ============================================================================
# DATA LOADER - Chargement des données
# ============================================================================
from utils.data_loader import (
    charger_donnees_appels,
    charger_calendrier_epidemiologique,
    charger_toutes_les_donnees,
    verifier_coherence_donnees,
    detecter_fichiers_data,
    mettre_a_jour_chemins_config
)

# ============================================================================
# DATA PROCESSOR - Traitement et agrégation
# ============================================================================
from utils.data_processor import (
    calculer_totaux_hebdomadaires,
    calculer_totaux_semaine,
    calculer_variations,
    calculer_regroupements,
    obtenir_statistiques_globales,
    regrouper_par_mois,
    comparer_periodes
)

# ============================================================================
# HELPERS - Fonctions utilitaires
# ============================================================================
from utils.helpers import (
    extraire_numero_semaine,
    obtenir_derniere_semaine,
    obtenir_semaine_precedente,
    obtenir_info_semaine_calendrier,
    obtenir_evolution_temporelle,
    convert_df_to_csv,
    convert_df_to_excel,
    formater_nombre,
    obtenir_mois_francais,
    formater_date_francais,
    formater_periode_semaine,
    generer_nom_fichier,
    valider_format_semaine,
    calculer_duree_jours
)

# ============================================================================
# LOGGER - Système de logs
# ============================================================================
from utils.logger import (
    setup_logger,
    log_chargement_donnees,
    log_erreur,
    log_generation_rapport,
    log_upload_fichier,
    log_export,
    log_aggregation,
    log_session,
    log_performance,
    log_validation,
    nettoyer_vieux_logs,
    obtenir_stats_logs
)

# ============================================================================
# CHARTS - Création de graphiques
# ============================================================================
from utils.charts import (
    creer_graphique_barres,
    creer_graphique_camembert,
    creer_graphique_ligne,
    creer_graphique_barres_groupees,
    creer_heatmap,
    creer_graphique_evolution,
    creer_graphique_variation,
    creer_graphique_comparaison,
    creer_graphique_distribution
)

# Version du module
__version__ = '2.0'
__author__ = 'Fred - AIMS Cameroon'

# Liste des exports publics
__all__ = [
    # Data Loader
    'charger_donnees_appels',
    'charger_calendrier_epidemiologique',
    'charger_toutes_les_donnees',
    'verifier_coherence_donnees',
    'detecter_fichiers_data',
    'mettre_a_jour_chemins_config',
    
    # Data Processor
    'calculer_totaux_hebdomadaires',
    'calculer_totaux_semaine',
    'calculer_variations',
    'calculer_regroupements',
    'obtenir_statistiques_globales',
    'regrouper_par_mois',
    'comparer_periodes',
    
    # Helpers
    'extraire_numero_semaine',
    'obtenir_derniere_semaine',
    'obtenir_semaine_precedente',
    'obtenir_info_semaine_calendrier',
    'obtenir_evolution_temporelle',
    'convert_df_to_csv',
    'convert_df_to_excel',
    'formater_nombre',
    'obtenir_mois_francais',
    'formater_date_francais',
    'formater_periode_semaine',
    'generer_nom_fichier',
    'valider_format_semaine',
    'calculer_duree_jours',
    
    # Logger
    'setup_logger',
    'log_chargement_donnees',
    'log_erreur',
    'log_generation_rapport',
    'log_upload_fichier',
    'log_export',
    'log_aggregation',
    'log_session',
    'log_performance',
    'log_validation',
    'nettoyer_vieux_logs',
    'obtenir_stats_logs',
    
    # Charts
    'creer_graphique_barres',
    'creer_graphique_camembert',
    'creer_graphique_ligne',
    'creer_graphique_barres_groupees',
    'creer_heatmap',
    'creer_graphique_evolution',
    'creer_graphique_variation',
    'creer_graphique_comparaison',
    'creer_graphique_distribution'
]