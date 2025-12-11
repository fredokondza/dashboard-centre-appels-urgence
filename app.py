"""
==============================================================================
DASHBOARD CENTRE D'APPELS D'URGENCE SANITAIRE - PAGE D'ACCUEIL
==============================================================================
Application Streamlit pour le suivi et l'analyse des appels du Centre 
d'Appels d'Urgence Sanitaire 1510 - MINSANTE Cameroun.

Cette page affiche :
- Vue d'ensemble des statistiques clés
- Évolution des appels sur les 10 dernières semaines
- Top 8 des catégories d'appels
- Répartition par regroupements thématiques

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.1 FINALE - Évolution corrigée + Footer CCOUSP/MINSANTE
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# Imports des modules
from config import settings
from utils.data_loader import charger_toutes_les_donnees
from utils.data_processor import obtenir_statistiques_globales
from utils.helpers import formater_nombre, obtenir_evolution_temporelle
from utils.logger import setup_logger, log_chargement_donnees, log_erreur
from components.layout import apply_custom_css, page_header
from components.sidebar import render_sidebar
from components.metrics import metric_row
from utils.charts import (
    creer_graphique_evolution,
    creer_graphique_barres,
    creer_graphique_camembert
)

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

st.set_page_config(
    page_title=settings.APP_CONFIG['page_title'],
    page_icon=settings.APP_CONFIG['page_icon'],
    layout=settings.APP_CONFIG['layout'],
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

logger = setup_logger('app')
logger.info("=== Page d'accueil chargée ===")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="DASHBOARD CENTRE D'APPELS D'URGENCE SANITAIRE",
    subtitle="Vue d'ensemble et statistiques clés",
    icon="🏥"
)

# ==============================================================================
# CHARGEMENT DONNÉES
# ==============================================================================

@st.cache_data(ttl=settings.CACHE_CONFIG['ttl'])
def load_data():
    try:
        donnees = charger_toutes_les_donnees()
        log_chargement_donnees('Toutes les données', nb_lignes=len(donnees['appels']), success=True)
        return donnees
    except Exception as e:
        log_erreur('load_data', 'Échec du chargement', exception=e)
        raise

try:
    donnees = load_data()
    df_appels = donnees['appels']
    df_hebdo = donnees['hebdomadaire']
    stats = donnees['statistiques']
except Exception as e:
    st.error(settings.MESSAGES['error']['data_inconsistency'])
    st.stop()

# ==============================================================================
# BANNIÈRE INFO
# ==============================================================================

st.info(f"""
    📅 **Période analysée :** {stats['date_min'].strftime('%d/%m/%Y')} - {stats['date_max'].strftime('%d/%m/%Y')}  
    📊 **{stats['nb_jours']} jours** de données sur **{stats['nb_semaines']} semaines** épidémiologiques
""")

# ==============================================================================
# MÉTRIQUES CLÉS
# ==============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📞 Total", formater_nombre(stats['total_appels']))
with col2:
    st.metric("📅 Jours", stats['nb_jours'])
with col3:
    st.metric("📊 Moy/Jour", formater_nombre(int(stats['moyenne_jour'])))
with col4:
    st.metric("🗓️ Semaines", stats['nb_semaines'])

# ==============================================================================
# ÉVOLUTION TEMPORELLE - CORRECTION ICI ✅
# ==============================================================================

st.markdown("##### 📈 Évolution des Appels (10 dernières semaines)")

# Obtenir les données triées depuis la fonction helper
evolution = obtenir_evolution_temporelle(df_hebdo, nb_semaines=10)

if evolution['semaines']:
    # Créer un DataFrame depuis le dictionnaire retourné
    df_evolution = pd.DataFrame({
        'Semaine épidémiologique': evolution['semaines'],
        'TOTAL_APPELS_SEMAINE': evolution['valeurs']
    })
    
    # Utiliser le DataFrame trié pour le graphique ✅
    fig_evolution = creer_graphique_evolution(
        data=df_evolution,
        x_col='Semaine épidémiologique',
        y_col='TOTAL_APPELS_SEMAINE',
        titre="",
        ajouter_moyenne=True,
        ajouter_tendance=False
    )
    
    fig_evolution.update_layout(height=230, margin=dict(l=40, r=40, t=10, b=40))
    
    st.plotly_chart(fig_evolution, use_container_width=True, config=settings.PLOTLY_CONFIG)

# ==============================================================================
# TOP CATÉGORIES + RÉPARTITION
# ==============================================================================

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("##### 🏆 Top 8 des Catégories")
    
    categories_data = {}
    for categorie in settings.CATEGORIES_APPELS:
        if categorie in df_appels.columns:
            total = int(df_appels[categorie].sum())
            if total > 0:
                label = settings.LABELS_CATEGORIES[categorie]
                categories_data[label] = total
    
    top_categories = dict(sorted(categories_data.items(), key=lambda x: x[1], reverse=True)[:8])
    
    if top_categories:
        fig_top = creer_graphique_barres(
            data=top_categories,
            titre="",
            orientation='h',
            show_values=True,
            height=260
        )
        fig_top.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_top, use_container_width=True, config=settings.PLOTLY_CONFIG)

with col2:
    st.markdown("##### 🔵 Répartition par Thématique")
    
    stats_globales = obtenir_statistiques_globales(df_appels, df_hebdo)
    repartition = stats_globales.get('repartition_regroupements', {})
    
    regroupements_data = {
        groupe: data['total'] 
        for groupe, data in repartition.items() 
        if data['total'] > 0
    }
    
    if regroupements_data:
        fig_regroupements = creer_graphique_camembert(
            data=regroupements_data,
            titre="",
            type_graphique='donut',
            show_percentages=True
        )
        fig_regroupements.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=9)
            )
        )
        st.plotly_chart(fig_regroupements, use_container_width=True, config=settings.PLOTLY_CONFIG)

# ==============================================================================
# ACCÈS RAPIDE
# ==============================================================================

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("pages/1_Vue_Ensemble.py", label="📊 Vue Ensemble", icon="📊")
with col2:
    st.page_link("pages/2_Analyse_Epidemiologique.py", label="📈 Analyse Épidémio", icon="📈")
with col3:
    st.page_link("pages/3_Comparaisons.py", label="🔄 Comparaisons", icon="🔄")
with col4:
    st.page_link("pages/5_Generation_Rapports.py", label="📊 Rapports", icon="📊")

# ==============================================================================
# FIN
# ==============================================================================