"""
==============================================================================
PAGE 3 - COMPARAISONS TEMPORELLES
==============================================================================
Page dédiée aux comparaisons temporelles avancées :
- Comparaison hebdomadaire entre périodes
- Comparaison mensuelle avec agrégation
- Analyse des tendances avec régression linéaire
- Visualisations comparatives multicritères

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.2 FINALE - Correction suffixe _sum + Footer CCOUSP/MINSANTE
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Imports de la nouvelle architecture
from config import settings
from utils.data_loader import charger_toutes_les_donnees
from utils.data_processor import regrouper_par_mois
from utils.helpers import extraire_numero_semaine, formater_nombre
from utils.logger import setup_logger
from components.layout import apply_custom_css, page_header, section_header
from components.sidebar import render_sidebar
from components.metrics import metric_row
from components.tables import export_buttons

# Import depuis utils.charts
from utils.charts import (
    creer_graphique_evolution,
    creer_graphique_barres,
    creer_graphique_variation
)

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

st.set_page_config(
    page_title="Comparaisons - Dashboard Urgence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS + JAVASCRIPT
# ==============================================================================

apply_custom_css()

components.html("""
<script>
function forceHamburgerAlwaysVisible() {
    const selectors = [
        '[data-testid="collapsedControl"]',
        'button[kind="icon"]',
        '[class*="collapsedControl"]'
    ];
    
    let btn = null;
    for (const selector of selectors) {
        btn = parent.document.querySelector(selector);
        if (btn) break;
    }
    
    if (btn) {
        btn.style.cssText = `
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: fixed !important;
            top: 4.2rem !important;
            left: 0.8rem !important;
            z-index: 9999999999 !important;
            width: 52px !important;
            height: 52px !important;
            background: linear-gradient(135deg, #007A33 0%, #00a844 100%) !important;
            border-radius: 10px !important;
            border: 3px solid white !important;
            box-shadow: 0 4px 16px rgba(0, 122, 51, 0.5) !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            pointer-events: auto !important;
        `;
        
        btn.setAttribute('aria-hidden', 'false');
        
        if (btn.parentElement) {
            btn.parentElement.style.cssText = `
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
            `;
        }
    }
}

setInterval(forceHamburgerAlwaysVisible, 100);

const observer = new MutationObserver(forceHamburgerAlwaysVisible);
observer.observe(parent.document.body, { 
    childList: true, 
    subtree: true,
    attributes: true,
    attributeFilter: ['style', 'class', 'aria-hidden']
});

forceHamburgerAlwaysVisible();

parent.document.addEventListener('click', function(e) {
    setTimeout(forceHamburgerAlwaysVisible, 50);
    setTimeout(forceHamburgerAlwaysVisible, 200);
    setTimeout(forceHamburgerAlwaysVisible, 500);
});
</script>
""", height=0)

logger = setup_logger('comparaisons')
logger.info("=== Page Comparaisons chargée ===")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="COMPARAISONS TEMPORELLES",
    subtitle="Analyses comparatives et tendances",
    icon="📊"
)

# ==============================================================================
# CHARGEMENT DES DONNÉES
# ==============================================================================

@st.cache_data(ttl=settings.CACHE_CONFIG['ttl'])
def load_data():
    """Charge toutes les données avec cache."""
    return charger_toutes_les_donnees()

try:
    donnees = load_data()
    df_appels = donnees['appels']
    df_hebdo = donnees['hebdomadaire']
    
except Exception as e:
    st.error(settings.MESSAGES['error']['data_inconsistency'])
    logger.error(f"Erreur chargement : {str(e)}")
    st.stop()

# ==============================================================================
# SÉLECTION DU TYPE DE COMPARAISON
# ==============================================================================

section_header("Type de Comparaison", icon="🎯")

type_comparaison = st.radio(
    "Choisissez le type de comparaison :",
    ["Comparaison Hebdomadaire", "Comparaison Mensuelle", "Analyse des Tendances"],
    horizontal=True
)

# ==============================================================================
# COMPARAISON HEBDOMADAIRE
# ==============================================================================

if type_comparaison == "Comparaison Hebdomadaire":
    
    section_header("Comparaison Hebdomadaire", icon="📅")
    
    # Trier les semaines
    semaines_disponibles = sorted(
        df_appels['Semaine épidémiologique'].unique(),
        key=extraire_numero_semaine
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        periode_debut = st.selectbox(
            "Semaine de début :",
            semaines_disponibles,
            index=0
        )
    
    with col2:
        # Filtrer pour ne montrer que les semaines après la semaine de début
        index_debut = semaines_disponibles.index(periode_debut)
        semaines_fin = semaines_disponibles[index_debut:]
        
        periode_fin = st.selectbox(
            "Semaine de fin :",
            semaines_fin,
            index=len(semaines_fin) - 1
        )
    
    # Filtrer les semaines dans la plage
    idx_fin = semaines_disponibles.index(periode_fin)
    semaines_periode = semaines_disponibles[index_debut:idx_fin+1]
    
    # Filtrer et trier le DataFrame
    df_periode = df_hebdo[df_hebdo['Semaine épidémiologique'].isin(semaines_periode)].copy()
    df_periode['_sort'] = df_periode['Semaine épidémiologique'].apply(extraire_numero_semaine)
    df_periode = df_periode.sort_values('_sort').drop('_sort', axis=1).reset_index(drop=True)
    
    if len(df_periode) > 0:
        
        # === STATISTIQUES DE LA PÉRIODE ===
        section_header("Statistiques de la Période", icon="📊")
        
        total_periode = df_periode['TOTAL_APPELS_SEMAINE'].sum()
        nb_semaines = len(df_periode)
        moyenne_periode = df_periode['TOTAL_APPELS_SEMAINE'].mean()
        ecart_type = df_periode['TOTAL_APPELS_SEMAINE'].std()
        
        metrics = [
            {'label': 'Total Appels', 'value': int(total_periode), 'icon': '📞'},
            {'label': 'Semaines', 'value': nb_semaines, 'icon': '📅'},
            {'label': 'Moyenne/Semaine', 'value': int(moyenne_periode), 'icon': '📊'},
            {'label': 'Écart-Type', 'value': int(ecart_type), 'icon': '📈'}
        ]
        
        metric_row(metrics, columns=4)
        
        # === GRAPHIQUE D'ÉVOLUTION ===
        section_header("Évolution sur la Période", icon="📈")
        
        fig_evolution = creer_graphique_evolution(
            data=df_periode,
            x_col='Semaine épidémiologique',
            y_col='TOTAL_APPELS_SEMAINE',
            titre=f"Évolution du {periode_debut} au {periode_fin}",
            ajouter_moyenne=True,
            ajouter_tendance=False
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True, config=settings.PLOTLY_CONFIG)
        
        # === COMPARAISON PREMIÈRE vs DERNIÈRE ===
        section_header("Comparaison Première vs Dernière Semaine", icon="🔄")
        
        premiere = df_periode.iloc[0]
        derniere = df_periode.iloc[-1]
        
        variation_abs = derniere['TOTAL_APPELS_SEMAINE'] - premiere['TOTAL_APPELS_SEMAINE']
        variation_rel = (variation_abs / premiere['TOTAL_APPELS_SEMAINE'] * 100) if premiere['TOTAL_APPELS_SEMAINE'] != 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                premiere['Semaine épidémiologique'],
                formater_nombre(int(premiere['TOTAL_APPELS_SEMAINE']))
            )
        
        with col2:
            st.metric(
                derniere['Semaine épidémiologique'],
                formater_nombre(int(derniere['TOTAL_APPELS_SEMAINE']))
            )
        
        with col3:
            st.metric(
                "Variation",
                f"{int(variation_abs):+}",
                delta=f"{variation_rel:+.1f}%"
            )
        
        # === TOP CATÉGORIES (VERSION FINALE CORRIGÉE) ===
        section_header("Top 10 des Catégories sur la Période", icon="🏆")
        
        categories_periode = {}
        
        # Parcourir les catégories
        for categorie in settings.CATEGORIES_APPELS:
            # Les colonnes dans df_periode ont le format: CATEGORIE_JOUR_sum
            col_name = f"{categorie}_sum"
            
            # Vérifier si la colonne existe
            if col_name in df_periode.columns:
                total = int(df_periode[col_name].sum())
                
                # Ne garder que les catégories avec total > 0
                if total > 0:
                    # Récupérer le label depuis settings
                    label = settings.LABELS_CATEGORIES.get(categorie, categorie)
                    categories_periode[label] = total
        
        # Vérifier qu'on a des données
        if categories_periode:
            # Trier et garder le top 10
            top_10 = dict(sorted(categories_periode.items(), key=lambda x: x[1], reverse=True)[:10])
            
            fig_top = creer_graphique_barres(
                data=top_10,
                titre=f"Top 10 du {periode_debut} au {periode_fin}",
                orientation='h',
                show_values=True,
                height=500
            )
            
            st.plotly_chart(fig_top, use_container_width=True, config=settings.PLOTLY_CONFIG)
        else:
            st.warning("⚠️ Aucune catégorie avec des données trouvée pour cette période")
        
        # Export
        with st.expander("💾 Exporter les Données"):
            export_buttons(df_periode, filename_prefix="comparaison_hebdo")
    
    else:
        st.warning(settings.MESSAGES['warning']['no_data'])

# ==============================================================================
# COMPARAISON MENSUELLE
# ==============================================================================

elif type_comparaison == "Comparaison Mensuelle":
    
    section_header("Comparaison Mensuelle", icon="📅")
    
    st.info(
        "💡 Les données sont regroupées par mois (approximation basée sur les semaines épidémiologiques)"
    )
    
    # Regrouper par mois
    df_mois = regrouper_par_mois(df_hebdo)
    
    # === VUE D'ENSEMBLE ===
    section_header("Vue d'Ensemble Mensuelle", icon="📊")
    
    total_general = df_mois['TOTAL_APPELS_SEMAINE'].sum()
    nb_mois = len(df_mois)
    moyenne_mois = df_mois['TOTAL_APPELS_SEMAINE'].mean()
    
    metrics = [
        {'label': 'Total Général', 'value': int(total_general), 'icon': '📞'},
        {'label': 'Nombre de Mois', 'value': nb_mois, 'icon': '📅'},
        {'label': 'Moyenne/Mois', 'value': int(moyenne_mois), 'icon': '📊'}
    ]
    
    metric_row(metrics, columns=3)
    
    # === GRAPHIQUE MENSUEL ===
    section_header("Comparaison des Mois", icon="📈")
    
    fig_mois = creer_graphique_barres(
        data=dict(zip(df_mois['Mois'], df_mois['TOTAL_APPELS_SEMAINE'])),
        titre="Nombre d'appels par mois",
        orientation='v',
        show_values=True,
        height=500
    )
    
    st.plotly_chart(fig_mois, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # === MOIS EXTRÊMES ===
    col1, col2 = st.columns(2)
    
    with col1:
        mois_max = df_mois.loc[df_mois['TOTAL_APPELS_SEMAINE'].idxmax()]
        st.success(f"🏆 **Mois le plus chargé :** {mois_max['Mois']} avec {formater_nombre(int(mois_max['TOTAL_APPELS_SEMAINE']))} appels")
    
    with col2:
        mois_min = df_mois.loc[df_mois['TOTAL_APPELS_SEMAINE'].idxmin()]
        st.info(f"📉 **Mois le moins chargé :** {mois_min['Mois']} avec {formater_nombre(int(mois_min['TOTAL_APPELS_SEMAINE']))} appels")
    
    # === COMPARAISON PAR CATÉGORIE (VERSION CORRIGÉE) ===
    section_header("Comparaison par Catégorie", icon="🔍")
    
    categories_a_comparer = st.multiselect(
        "Sélectionnez les catégories à comparer :",
        [settings.LABELS_CATEGORIES[cat] for cat in settings.CATEGORIES_APPELS],
        default=[settings.LABELS_CATEGORIES[cat] for cat in settings.CATEGORIES_APPELS[:3]]
    )
    
    if categories_a_comparer:
        reverse_labels = {v: k for k, v in settings.LABELS_CATEGORIES.items()}
        
        # Créer le graphique manuellement avec go.Figure()
        fig_multi = go.Figure()
        
        # Couleurs
        couleurs = [
            settings.COULEURS_CAMEROUN['vert'],
            settings.COULEURS_CAMEROUN['jaune'],
            '#17a2b8',
            settings.COULEURS_CAMEROUN['rouge'],
            '#6c757d'
        ]
        
        # Ajouter une trace pour chaque catégorie
        for i, cat_label in enumerate(categories_a_comparer):
            cat_code = reverse_labels[cat_label]
            col_name = cat_code.replace('_JOUR', '_SEMAINE')
            
            if col_name in df_mois.columns:
                fig_multi.add_trace(go.Bar(
                    name=cat_label,
                    x=df_mois['Mois'],
                    y=df_mois[col_name],
                    marker_color=couleurs[i % len(couleurs)]
                ))
        
        # Configuration du layout
        fig_multi.update_layout(
            title="Comparaison des catégories par mois",
            xaxis_title="Mois",
            yaxis_title="Nombre d'appels",
            barmode='group',
            height=500,
            template=settings.PLOTLY_TEMPLATE,
            font=dict(family=settings.GRAPH_CONFIG['font_family']),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                tickangle=-45
            )
        )
        
        st.plotly_chart(fig_multi, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # Export
    with st.expander("📋 Tableau et Export"):
        st.dataframe(df_mois, use_container_width=True, height=400)
        export_buttons(df_mois, filename_prefix="comparaison_mensuelle")

# ==============================================================================
# ANALYSE DES TENDANCES
# ==============================================================================

else:  # Analyse des Tendances
    
    section_header("Analyse des Tendances", icon="📈")
    
    # Trier par semaine
    df_hebdo_sorted = df_hebdo.copy()
    df_hebdo_sorted['_sort'] = df_hebdo_sorted['Semaine épidémiologique'].apply(extraire_numero_semaine)
    df_hebdo_sorted = df_hebdo_sorted.sort_values('_sort').reset_index(drop=True)
    
    # === VUE GLOBALE ===
    section_header("Vue Globale", icon="🌐")
    
    # Calculer la tendance (régression linéaire)
    df_hebdo_sorted['num_semaine'] = range(1, len(df_hebdo_sorted) + 1)
    coefficients = np.polyfit(df_hebdo_sorted['num_semaine'], df_hebdo_sorted['TOTAL_APPELS_SEMAINE'], 1)
    tendance = coefficients[0]
    
    premiere_val = df_hebdo_sorted.iloc[0]['TOTAL_APPELS_SEMAINE']
    derniere_val = df_hebdo_sorted.iloc[-1]['TOTAL_APPELS_SEMAINE']
    variation_totale = ((derniere_val - premiere_val) / premiere_val * 100) if premiere_val != 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Première Semaine", formater_nombre(int(premiere_val)))
    
    with col2:
        st.metric(
            "Dernière Semaine",
            formater_nombre(int(derniere_val)),
            delta=f"{variation_totale:+.1f}%"
        )
    
    with col3:
        tendance_label = "Croissante" if tendance > 0 else "Décroissante" if tendance < 0 else "Stable"
        st.metric("Tendance", tendance_label, delta=f"{tendance:+.1f} appels/semaine")
    
    # === GRAPHIQUE AVEC TENDANCE ===
    section_header("Évolution avec Ligne de Tendance", icon="📊")
    
    fig_tendance = creer_graphique_evolution(
        data=df_hebdo_sorted,
        x_col='Semaine épidémiologique',
        y_col='TOTAL_APPELS_SEMAINE',
        titre="Évolution des appels avec ligne de tendance",
        ajouter_moyenne=False,
        ajouter_tendance=True
    )
    
    st.plotly_chart(fig_tendance, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # === ANALYSE DE VOLATILITÉ ===
    section_header("Analyse de Volatilité", icon="📊")
    
    # Calculer les variations
    df_hebdo_sorted['variation'] = df_hebdo_sorted['TOTAL_APPELS_SEMAINE'].diff()
    df_hebdo_sorted['variation_pct'] = df_hebdo_sorted['TOTAL_APPELS_SEMAINE'].pct_change() * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        var_max = df_hebdo_sorted['variation'].max()
        st.metric("Plus Grande Hausse", f"{int(var_max):+}")
    
    with col2:
        var_min = df_hebdo_sorted['variation'].min()
        st.metric("Plus Grande Baisse", f"{int(var_min):+}")
    
    with col3:
        var_moy = df_hebdo_sorted['variation'].mean()
        st.metric("Variation Moyenne", f"{int(var_moy):+}")
    
    with col4:
        volatilite = df_hebdo_sorted['variation'].std()
        st.metric("Volatilité (σ)", formater_nombre(int(volatilite)))
    
    # Graphique des variations
    df_var = df_hebdo_sorted[1:].copy()  # Exclure la première ligne
    
    fig_var = creer_graphique_variation(
        data=df_var,
        x_col='Semaine épidémiologique',
        y_col='variation',
        titre="Variations hebdomadaires",
        height=400
    )
    
    st.plotly_chart(fig_var, use_container_width=True, config=settings.PLOTLY_CONFIG)

# ==============================================================================
# FIN DE LA PAGE
# ==============================================================================