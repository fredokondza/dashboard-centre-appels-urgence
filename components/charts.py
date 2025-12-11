"""
==============================================================================
MODULE DES COMPOSANTS GRAPHIQUES
==============================================================================
Ce module fournit des wrappers de haut niveau pour les graphiques
utilisés fréquemment dans les pages du dashboard.

Ces fonctions encapsulent utils.charts avec des configurations
pré-définies pour un usage rapide dans les pages.

Différence avec utils/charts.py :
- utils/charts.py : Fonctions de base configurables
- components/charts.py : Wrappers spécifiques au dashboard avec configs par défaut

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Import de la configuration
sys.path.append(str(Path(__file__).parent.parent))

from config import settings
from utils import charts as base_charts
from utils.helpers import extraire_numero_semaine

# ==============================================================================
# FONCTION 1 : GRAPHIQUE ÉVOLUTION SEMAINES (PRESET DASHBOARD)
# ==============================================================================

def graphique_evolution_semaines(df_hebdo, nb_semaines=10, titre=None):
    """
    Affiche un graphique d'évolution des dernières semaines (preset dashboard).
    
    Cette fonction est un wrapper qui :
    - Trie automatiquement les semaines
    - Sélectionne les N dernières semaines
    - Applique les paramètres standards du dashboard
    - Ajoute moyenne et tendance par défaut
    
    Args:
        df_hebdo (pd.DataFrame): DataFrame hebdomadaire
        nb_semaines (int): Nombre de semaines à afficher
        titre (str, optional): Titre personnalisé
    
    Returns:
        plotly.graph_objects.Figure: Graphique prêt à afficher
    
    Example:
        >>> fig = graphique_evolution_semaines(df_hebdo, nb_semaines=10)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    # Trier et filtrer
    df_sorted = df_hebdo.copy()
    df_sorted['_sort'] = df_sorted['Semaine épidémiologique'].apply(extraire_numero_semaine)
    df_sorted = df_sorted.sort_values('_sort').tail(nb_semaines).drop('_sort', axis=1).reset_index(drop=True)
    
    # Titre par défaut
    if titre is None:
        titre = f"Évolution des {nb_semaines} dernières semaines"
    
    # Créer le graphique
    fig = base_charts.creer_graphique_evolution(
        data=df_sorted,
        x_col='Semaine épidémiologique',
        y_col='TOTAL_APPELS_SEMAINE',
        titre=titre,
        ajouter_moyenne=True,
        ajouter_tendance=True,
        height=500
    )
    
    return fig

# ==============================================================================
# FONCTION 2 : GRAPHIQUE TOP CATÉGORIES (PRESET DASHBOARD)
# ==============================================================================

def graphique_top_categories(df_appels, semaine=None, top_n=10, orientation='h'):
    """
    Affiche un graphique des top N catégories (preset dashboard).
    
    Args:
        df_appels (pd.DataFrame): DataFrame des appels
        semaine (str, optional): Semaine spécifique. Si None, toutes les données
        top_n (int): Nombre de catégories à afficher
        orientation (str): 'h' (horizontal) ou 'v' (vertical)
    
    Returns:
        plotly.graph_objects.Figure: Graphique prêt à afficher
    
    Example:
        >>> fig = graphique_top_categories(df_appels, semaine='S10_2025', top_n=10)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    # Filtrer par semaine si spécifié
    if semaine:
        df_filtered = df_appels[df_appels['Semaine épidémiologique'] == semaine]
    else:
        df_filtered = df_appels
    
    # Calculer les totaux par catégorie
    categories_data = {}
    for categorie in settings.CATEGORIES_APPELS:
        if categorie in df_filtered.columns:
            total = int(df_filtered[categorie].sum())
            if total > 0:
                label = settings.LABELS_CATEGORIES[categorie]
                categories_data[label] = total
    
    # Trier et garder le top N
    top_categories = dict(sorted(categories_data.items(), key=lambda x: x[1], reverse=True)[:top_n])
    
    # Titre
    titre = f"Top {top_n} des Catégories"
    if semaine:
        titre += f" - {semaine}"
    
    # Créer le graphique
    fig = base_charts.creer_graphique_barres(
        data=top_categories,
        titre=titre,
        orientation=orientation,
        show_values=True,
        height=500
    )
    
    return fig

# ==============================================================================
# FONCTION 3 : GRAPHIQUE RÉPARTITION REGROUPEMENTS (PRESET DASHBOARD)
# ==============================================================================

def graphique_repartition_regroupements(regroupements_data, titre=None, type_graphique='donut'):
    """
    Affiche un graphique de répartition par regroupements thématiques.
    
    Args:
        regroupements_data (dict): Dictionnaire {regroupement: valeur}
        titre (str, optional): Titre personnalisé
        type_graphique (str): 'pie' ou 'donut'
    
    Returns:
        plotly.graph_objects.Figure: Graphique prêt à afficher
    
    Example:
        >>> regroupements = {'Renseignements': 3000, 'Assistances': 2000}
        >>> fig = graphique_repartition_regroupements(regroupements)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    if titre is None:
        titre = "Répartition par Thématique"
    
    fig = base_charts.creer_graphique_camembert(
        data=regroupements_data,
        titre=titre,
        type_graphique=type_graphique,
        show_percentages=True
    )
    
    return fig

# ==============================================================================
# FONCTION 4 : GRAPHIQUE COMPARAISON SEMAINES (PRESET DASHBOARD)
# ==============================================================================

def graphique_comparaison_semaines(df_appels, semaines_list, categories=None):
    """
    Affiche un graphique de comparaison entre plusieurs semaines.
    
    Args:
        df_appels (pd.DataFrame): DataFrame des appels
        semaines_list (list): Liste des semaines à comparer
        categories (list, optional): Liste des catégories à comparer
            Si None, compare uniquement les totaux
    
    Returns:
        plotly.graph_objects.Figure: Graphique prêt à afficher
    
    Example:
        >>> fig = graphique_comparaison_semaines(df_appels, ['S9_2025', 'S10_2025'])
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    if categories is None:
        # Comparaison des totaux uniquement
        totaux = {}
        for semaine in semaines_list:
            df_sem = df_appels[df_appels['Semaine épidémiologique'] == semaine]
            totaux[semaine] = int(df_sem['TOTAL_APPELS_JOUR'].sum())
        
        fig = base_charts.creer_graphique_barres(
            data=totaux,
            titre="Comparaison du nombre total d'appels",
            orientation='v',
            show_values=True,
            height=400
        )
    else:
        # Comparaison par catégories
        comparison_data = []
        reverse_labels = {v: k for k, v in settings.LABELS_CATEGORIES.items()}
        
        for categorie_label in categories:
            if categorie_label in reverse_labels:
                categorie_code = reverse_labels[categorie_label]
                row_data = {'Catégorie': categorie_label}
                
                for semaine in semaines_list:
                    df_sem = df_appels[df_appels['Semaine épidémiologique'] == semaine]
                    if categorie_code in df_sem.columns:
                        total = int(df_sem[categorie_code].sum())
                        row_data[semaine] = total
                    else:
                        row_data[semaine] = 0
                
                comparison_data.append(row_data)
        
        df_comparison = pd.DataFrame(comparison_data)
        
        fig = base_charts.creer_graphique_barres_groupees(
            data=df_comparison,
            x_col='Catégorie',
            categories_cols=semaines_list,
            titre="Comparaison des catégories",
            height=500
        )
    
    return fig

# ==============================================================================
# FONCTION 5 : GRAPHIQUE ÉVOLUTION JOURNALIÈRE (PRESET DASHBOARD)
# ==============================================================================

def graphique_evolution_journaliere(df_appels, semaine):
    """
    Affiche l'évolution journalière pour une semaine spécifique.
    
    Args:
        df_appels (pd.DataFrame): DataFrame des appels
        semaine (str): Semaine épidémiologique
    
    Returns:
        plotly.graph_objects.Figure: Graphique prêt à afficher
    
    Example:
        >>> fig = graphique_evolution_journaliere(df_appels, 'S10_2025')
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    # Filtrer
    df_semaine = df_appels[df_appels['Semaine épidémiologique'] == semaine].copy()
    
    # Préparer les données
    df_semaine['Jour'] = df_semaine['DATE'].dt.strftime('%d/%m')
    
    # Créer le graphique
    fig = base_charts.creer_graphique_ligne(
        data=df_semaine,
        x_col='Jour',
        y_col='TOTAL_APPELS_JOUR',
        titre=f"Évolution journalière - {semaine}",
        show_markers=True,
        fill_area=True,
        moyenne_line=True,
        height=400
    )
    
    return fig

# ==============================================================================
# FONCTION 6 : GRAPHIQUE MENSUEL (PRESET DASHBOARD)
# ==============================================================================

def graphique_comparaison_mensuelle(df_mois):
    """
    Affiche un graphique de comparaison mensuelle.
    
    Args:
        df_mois (pd.DataFrame): DataFrame mensuel (de regrouper_par_mois)
    
    Returns:
        plotly.graph_objects.Figure: Graphique prêt à afficher
    
    Example:
        >>> from utils import regrouper_par_mois
        >>> df_mois = regrouper_par_mois(df_hebdo)
        >>> fig = graphique_comparaison_mensuelle(df_mois)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    data_mois = dict(zip(df_mois['Mois'], df_mois['TOTAL_APPELS_SEMAINE']))
    
    fig = base_charts.creer_graphique_barres(
        data=data_mois,
        titre="Nombre d'appels par mois",
        orientation='v',
        show_values=True,
        height=500
    )
    
    return fig

# ==============================================================================
# FONCTION 7 : AFFICHAGE GRAPHIQUE AVEC PLOTLY CONFIG (HELPER)
# ==============================================================================

def afficher_graphique(fig, key=None):
    """
    Affiche un graphique Plotly avec la configuration standard du dashboard.
    
    Cette fonction encapsule st.plotly_chart avec les paramètres standards.
    
    Args:
        fig (plotly.graph_objects.Figure): Graphique à afficher
        key (str, optional): Clé unique pour Streamlit
    
    Example:
        >>> fig = graphique_evolution_semaines(df_hebdo)
        >>> afficher_graphique(fig)
    """
    st.plotly_chart(
        fig,
        use_container_width=True,
        config=settings.PLOTLY_CONFIG,
        key=key
    )

# ==============================================================================
# FONCTION BONUS : GRAPHIQUE AVEC EXPORT INTÉGRÉ
# ==============================================================================

def graphique_avec_export(fig, filename_prefix="graphique", show_export=True):
    """
    Affiche un graphique avec option d'export PNG.
    
    Args:
        fig (plotly.graph_objects.Figure): Graphique à afficher
        filename_prefix (str): Préfixe du nom de fichier
        show_export (bool): Afficher le bouton d'export
    
    Example:
        >>> fig = graphique_top_categories(df_appels)
        >>> graphique_avec_export(fig, "top_categories")
    """
    # Afficher le graphique
    afficher_graphique(fig)
    
    # Bouton d'export
    if show_export:
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # Export PNG (via Plotly)
            st.info("💡 Utilisez l'icône 📷 dans le graphique pour exporter en PNG")

# ==============================================================================
# FIN DU MODULE
# ==============================================================================