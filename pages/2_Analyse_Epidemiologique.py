"""
==============================================================================
PAGE 2 - ANALYSE ÉPIDÉMIOLOGIQUE
==============================================================================
Page dédiée à l'analyse épidémiologique détaillée :
- Mode 1 : Analyse d'une semaine spécifique
- Mode 2 : Comparaison de plusieurs semaines
- Évolution journalière
- Répartition par catégories
- Graphiques comparatifs
- Export des données

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.0 FINALE - Footer CCOUSP/MINSANTE + Graphiques corrigés
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

# Imports de la nouvelle architecture
from config import settings
from utils.data_loader import charger_toutes_les_donnees
from utils.data_processor import calculer_totaux_semaine, comparer_periodes
from utils.helpers import extraire_numero_semaine, formater_nombre
from utils.logger import setup_logger, log_export
from components.layout import apply_custom_css, page_header, section_header
from components.sidebar import render_sidebar
from components.tables import export_buttons

# Import depuis utils.charts
from utils.charts import (
    creer_graphique_ligne,
    creer_graphique_barres,
    creer_graphique_camembert
)

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

st.set_page_config(
    page_title="Analyse Épidémiologique - Dashboard Urgence",
    page_icon="🔬",
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

logger = setup_logger('analyse_epidemiologique')
logger.info("=== Page Analyse Épidémiologique chargée ===")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="ANALYSE ÉPIDÉMIOLOGIQUE",
    subtitle="Analyse détaillée par semaine",
    icon="🔬"
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
# SÉLECTION DU MODE D'ANALYSE
# ==============================================================================

section_header("Mode d'Analyse", icon="🎯")

mode = st.radio(
    "Choisissez le mode d'analyse :",
    ["📊 Analyse d'une Semaine", "🔄 Comparaison de Plusieurs Semaines"],
    horizontal=True
)

# ==============================================================================
# MODE 1 : ANALYSE D'UNE SEMAINE SPÉCIFIQUE
# ==============================================================================

if mode == "📊 Analyse d'une Semaine":
    
    section_header("Sélection de la Semaine", icon="📅")
    
    # Liste des semaines disponibles (triée)
    semaines_disponibles = sorted(
        df_appels['Semaine épidémiologique'].unique(),
        key=extraire_numero_semaine,
        reverse=True
    )
    
    semaine_selectionnee = st.selectbox(
        "Sélectionnez une semaine épidémiologique :",
        semaines_disponibles,
        index=0
    )
    
    # Filtrer les données
    df_semaine = df_appels[df_appels['Semaine épidémiologique'] == semaine_selectionnee]
    
    if len(df_semaine) == 0:
        st.error(f"❌ Aucune donnée pour {semaine_selectionnee}")
        st.stop()
    
    # Calculer les totaux
    totaux = calculer_totaux_semaine(df_appels, semaine_selectionnee)
    
    # === KPIs DE LA SEMAINE ===
    section_header("Indicateurs Clés", icon="📊")
    
    st.info(
        f"📅 Période : Du {totaux['date_debut'].strftime('%d/%m/%Y')} au {totaux['date_fin'].strftime('%d/%m/%Y')}"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📞 Total Appels",
            value=formater_nombre(totaux['total'])
        )
    
    with col2:
        st.metric(
            label="📅 Jours",
            value=totaux['nb_jours']
        )
    
    with col3:
        st.metric(
            label="📊 Moyenne/Jour",
            value=formater_nombre(int(totaux['moyenne_jour']))
        )
    
    # === ÉVOLUTION JOURNALIÈRE ===
    section_header("Évolution Journalière", icon="📈")
    
    df_jour = df_semaine.copy()
    df_jour['Jour'] = df_jour['DATE'].dt.strftime('%d/%m')
    
    fig_evolution = creer_graphique_ligne(
        data=df_jour,
        x_col='Jour',
        y_col='TOTAL_APPELS_JOUR',
        titre=f"Évolution journalière - {semaine_selectionnee}",
        show_markers=True
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # === RÉPARTITION PAR CATÉGORIES ===
    section_header("Répartition par Catégories", icon="📊")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Top 10 catégories
        categories = totaux['categories']
        top_10 = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10])
        
        fig_categories = creer_graphique_barres(
            data=top_10,
            titre="Top 10 des Catégories",
            orientation='h',
            show_values=True,
            height=500
        )
        
        st.plotly_chart(fig_categories, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    with col2:
        # Statistiques
        st.markdown("#### 📊 Statistiques")
        
        cat_actives = len([v for v in categories.values() if v > 0])
        plus_haute = max(categories.values()) if categories else 0
        plus_basse = min([v for v in categories.values() if v > 0], default=0)
        
        st.metric("Catégories actives", cat_actives)
        st.metric("Plus haute", formater_nombre(plus_haute))
        st.metric("Plus basse", formater_nombre(plus_basse))
        
        st.markdown("---")
        
        # Répartition par regroupements
        regroupements = totaux['regroupements']
        
        fig_regroupements = creer_graphique_camembert(
            data=regroupements,
            titre="Par Regroupement",
            type_graphique='donut',
            show_percentages=True
        )
        
        st.plotly_chart(fig_regroupements, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # === EXPORT ===
    with st.expander("💾 Exporter les Données"):
        export_buttons(
            df_semaine,
            filename_prefix=f"analyse_{semaine_selectionnee}",
            formats=['csv', 'excel']
        )

# ==============================================================================
# MODE 2 : COMPARAISON DE PLUSIEURS SEMAINES
# ==============================================================================

else:  # Comparaison
    
    section_header("Sélection des Semaines", icon="🔄")
    
    # Liste des semaines disponibles (triée)
    semaines_disponibles = sorted(
        df_appels['Semaine épidémiologique'].unique(),
        key=extraire_numero_semaine,
        reverse=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        nb_semaines = st.slider(
            "Nombre de semaines à comparer :",
            min_value=2,
            max_value=min(10, len(semaines_disponibles)),
            value=3
        )
    
    with col2:
        semaines_selectionnees = st.multiselect(
            "Sélectionnez les semaines :",
            semaines_disponibles,
            default=semaines_disponibles[:nb_semaines]
        )
    
    if len(semaines_selectionnees) < 2:
        st.warning("⚠️ Veuillez sélectionner au moins 2 semaines pour la comparaison")
        st.stop()
    
    # Trier les semaines sélectionnées
    semaines_selectionnees = sorted(semaines_selectionnees, key=extraire_numero_semaine)
    
    # === COMPARAISON DES TOTAUX ===
    section_header("Comparaison des Totaux", icon="📊")
    
    # Calculer les totaux pour chaque semaine
    totaux_comparaison = {}
    for semaine in semaines_selectionnees:
        totaux = calculer_totaux_semaine(df_appels, semaine)
        totaux_comparaison[semaine] = totaux['total']
    
    # Graphique de comparaison
    fig_comparaison = creer_graphique_barres(
        data=totaux_comparaison,
        titre="Comparaison du nombre total d'appels",
        orientation='v',
        show_values=True,
        height=400
    )
    
    st.plotly_chart(fig_comparaison, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # === MÉTRIQUES DE COMPARAISON ===
    cols = st.columns(len(semaines_selectionnees))
    
    for i, (col, (semaine, total)) in enumerate(zip(cols, totaux_comparaison.items())):
        with col:
            st.metric(
                label=semaine,
                value=formater_nombre(total)
            )
    
    # === COMPARAISON PAR CATÉGORIES ===
    section_header("Comparaison par Catégories", icon="🔍")
    
    # Sélection des catégories à comparer
    categories_a_comparer = st.multiselect(
        "Sélectionnez les catégories à comparer :",
        [settings.LABELS_CATEGORIES[cat] for cat in settings.CATEGORIES_APPELS],
        default=[settings.LABELS_CATEGORIES[cat] for cat in settings.CATEGORIES_APPELS[:3]]
    )
    
    if categories_a_comparer:
        # Créer le dictionnaire inverse
        reverse_labels = {v: k for k, v in settings.LABELS_CATEGORIES.items()}
        
        # Préparer les données pour comparaison
        comparison_data = []
        
        for categorie_label in categories_a_comparer:
            categorie_code = reverse_labels[categorie_label]
            
            row_data = {'Catégorie': categorie_label}
            
            for semaine in semaines_selectionnees:
                df_sem = df_appels[df_appels['Semaine épidémiologique'] == semaine]
                if categorie_code in df_sem.columns:
                    total = int(df_sem[categorie_code].sum())
                    row_data[semaine] = total
                else:
                    row_data[semaine] = 0
            
            comparison_data.append(row_data)
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # Tableau de comparaison
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        # === GRAPHIQUE BARRES GROUPÉES (VERSION CORRIGÉE) ===
        st.markdown("#### Visualisation Graphique")
        
        # Créer le graphique manuellement avec go.Figure()
        fig_multi = go.Figure()
        
        # Couleurs pour les semaines
        couleurs = [
            settings.COULEURS_CAMEROUN['vert'],
            settings.COULEURS_CAMEROUN['jaune'],
            '#17a2b8',
            settings.COULEURS_CAMEROUN['rouge'],
            '#6c757d'
        ]
        
        # Ajouter une trace pour chaque semaine
        for i, semaine in enumerate(semaines_selectionnees):
            if semaine in df_comparison.columns:
                fig_multi.add_trace(go.Bar(
                    name=semaine,
                    x=df_comparison['Catégorie'],
                    y=df_comparison[semaine],
                    marker_color=couleurs[i % len(couleurs)]
                ))
        
        # Configuration du layout
        fig_multi.update_layout(
            title="Comparaison des catégories sélectionnées",
            xaxis_title="Catégories",
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
    
    # === EXPORT ===
    with st.expander("💾 Exporter les Données Comparatives"):
        # Créer un DataFrame complet de comparaison
        df_export = comparer_periodes(df_appels, semaines_selectionnees)
        
        if len(df_export) > 0:
            export_buttons(
                df_export,
                filename_prefix="comparaison_semaines",
                formats=['csv', 'excel']
            )
            
            logger.info(f"Export comparaison : {len(semaines_selectionnees)} semaines")
        else:
            st.warning("Aucune donnée à exporter")

# ==============================================================================
# INFORMATIONS COMPLÉMENTAIRES
# ==============================================================================

with st.expander("ℹ️ Guide d'Utilisation"):
    st.markdown("""
    ### 📖 Mode d'Emploi
    
    **Mode Analyse d'une Semaine :**
    - Sélectionnez une semaine épidémiologique
    - Consultez les KPIs, l'évolution journalière et la répartition
    - Exportez les données au format CSV ou Excel
    
    **Mode Comparaison :**
    - Sélectionnez 2 à 10 semaines à comparer
    - Choisissez les catégories d'appels à analyser
    - Consultez les graphiques comparatifs
    - Exportez le tableau de comparaison
    
    ### 💡 Conseils
    - Utilisez le mode comparaison pour identifier les tendances
    - Exportez les données pour des analyses plus poussées
    - Les graphiques sont interactifs (zoom, sélection, etc.)
    """)

# ==============================================================================
# FIN DE LA PAGE
# ==============================================================================