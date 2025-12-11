"""
==============================================================================
MODULE COMPONENTS - INITIALISATION
==============================================================================
Ce fichier __init__.py permet d'importer facilement les composants UI.

Usage:
    from components import page_header, metric_row, export_buttons
    
Au lieu de:
    from components.layout import page_header
    from components.metrics import metric_row
    from components.tables import export_buttons

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

# ============================================================================
# LAYOUT - Composants de mise en page
# ============================================================================
from components.layout import (
    apply_custom_css,
    page_header,
    section_header,
    page_footer,
    info_box,
    modele_selection_card,
    metric_card_simple,
    alert_banner,
    custom_divider,
    breadcrumb,
    badge,
    custom_spinner,
    custom_progress_bar
)

# ============================================================================
# METRICS - Composants métriques et KPIs
# ============================================================================
from components.metrics import (
    metric_card_html,
    metric_row,
    kpi_card,
    comparison_metric
)

# ============================================================================
# TABLES - Composants tableaux et exports
# ============================================================================
from components.tables import (
    display_dataframe_formatted,
    export_buttons,
    create_summary_table,
    create_comparison_table,
    create_table_with_sparklines,
    create_pivot_table_interface,
    create_filtered_table
)

# ============================================================================
# CHARTS - Wrappers de graphiques réutilisables
# ============================================================================
from components.charts import (
    graphique_evolution_semaines,
    graphique_top_categories,
    graphique_repartition_regroupements,
    graphique_comparaison_semaines,
    graphique_evolution_journaliere,
    graphique_comparaison_mensuelle,
    afficher_graphique,
    graphique_avec_export
)

# Version du module
__version__ = '2.0'
__author__ = 'Fred - AIMS Cameroon'

# Liste des exports publics
__all__ = [
    # Layout
    'apply_custom_css',
    'page_header',
    'section_header',
    'page_footer',
    'info_box',
    'modele_selection_card',
    'metric_card_simple',
    'alert_banner',
    'custom_divider',
    'breadcrumb',
    'badge',
    'custom_spinner',
    'custom_progress_bar',
    
    # Metrics
    'metric_card_html',
    'metric_row',
    'kpi_card',
    'comparison_metric',
    
    # Tables
    'display_dataframe_formatted',
    'export_buttons',
    'create_summary_table',
    'create_comparison_table',
    'create_table_with_sparklines',
    'create_pivot_table_interface',
    'create_filtered_table',
    
    # Charts
    'graphique_evolution_semaines',
    'graphique_top_categories',
    'graphique_repartition_regroupements',
    'graphique_comparaison_semaines',
    'graphique_evolution_journaliere',
    'graphique_comparaison_mensuelle',
    'afficher_graphique',
    'graphique_avec_export'
]