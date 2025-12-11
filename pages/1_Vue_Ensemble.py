"""
==============================================================================
PAGE 1 - VUE D'ENSEMBLE
==============================================================================
Page dédiée à l'analyse de la dernière semaine épidémiologique :
- KPIs de la semaine
- Répartition par catégories (17 catégories)
- Répartition par regroupements (5 thématiques)
- Comparaison avec la semaine précédente
- Évolution temporelle triée

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.0 FINALE - Footer CCOUSP/MINSANTE intégré
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Imports de la nouvelle architecture
from config import settings
from utils.data_loader import charger_toutes_les_donnees
from utils.data_processor import calculer_totaux_semaine, calculer_variations
from utils.helpers import obtenir_derniere_semaine, obtenir_semaine_precedente, formater_nombre, extraire_numero_semaine
from utils.logger import setup_logger
from components.layout import apply_custom_css, page_header, section_header, page_footer
from components.sidebar import render_sidebar
from components.tables import export_buttons

# Import depuis utils.charts
from utils.charts import (
    creer_graphique_barres,
    creer_graphique_camembert,
    creer_graphique_evolution
)

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

st.set_page_config(
    page_title="Vue d'Ensemble - Dashboard Urgence",
    page_icon="👁️",
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

logger = setup_logger('vue_ensemble')
logger.info("=== Page Vue d'Ensemble chargée ===")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="VUE D'ENSEMBLE",
    subtitle="Analyse de la dernière semaine épidémiologique",
    icon="👁️"
)

# ==============================================================================
# CHARGEMENT DES DONNÉES
# ==============================================================================

@st.cache_data(ttl=settings.CACHE_CONFIG['ttl'])
def load_data():
    """Charge toutes les données avec cache."""
    return charger_toutes_les_donnees()

try:
    with st.spinner(settings.CACHE_CONFIG['spinner_text']):
        donnees = load_data()
    
    df_appels = donnees['appels']
    df_hebdo = donnees['hebdomadaire']
    
except Exception as e:
    st.error(settings.MESSAGES['error']['data_inconsistency'])
    st.error(f"Détails : {str(e)}")
    logger.error(f"Erreur chargement : {str(e)}")
    st.stop()

# ==============================================================================
# DÉTERMINER LES SEMAINES À ANALYSER
# ==============================================================================

semaine_actuelle = obtenir_derniere_semaine(df_hebdo)
semaine_precedente = obtenir_semaine_precedente(df_hebdo, semaine_actuelle)

if not semaine_actuelle:
    st.error("❌ Impossible de déterminer la dernière semaine")
    st.stop()

# Calculer les totaux
totaux_actuel = calculer_totaux_semaine(df_appels, semaine_actuelle)

# ==============================================================================
# SECTION 1 : KPIs DE LA SEMAINE
# ==============================================================================

section_header("Indicateurs Clés", icon="📊")

st.info(f"📅 **Semaine analysée :** {semaine_actuelle}")

# Calculer les variations si semaine précédente disponible
delta_total = None
if semaine_precedente:
    variations = calculer_variations(df_appels, semaine_actuelle, semaine_precedente)
    delta_total = f"{variations['variation_relative']:+.1f}%"

# Afficher les métriques
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📞 Total Appels",
        value=formater_nombre(totaux_actuel['total']),
        delta=delta_total
    )

with col2:
    st.metric(
        label="📅 Jours",
        value=totaux_actuel['nb_jours']
    )

with col3:
    st.metric(
        label="📊 Moyenne/Jour",
        value=formater_nombre(int(totaux_actuel['moyenne_jour']))
    )

# ==============================================================================
# SECTION 2 : RÉPARTITION DES APPELS
# ==============================================================================

section_header("Répartition des Appels", icon="📊")

# Onglets pour basculer entre catégories et regroupements
tab1, tab2 = st.tabs(["📋 Par Catégories (17)", "🔵 Par Regroupements (5)"])

# === ONGLET 1 : PAR CATÉGORIES ===
with tab1:
    st.markdown("#### Répartition par Catégorie d'Appels")
    
    categories = totaux_actuel['categories']
    
    if categories:
        # Trier par valeur décroissante
        categories_sorted = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
        
        # Graphique en barres horizontales
        fig_categories = creer_graphique_barres(
            data=categories_sorted,
            titre=f"Répartition des appels - {semaine_actuelle}",
            orientation='h',
            show_values=True,
            height=600
        )
        
        st.plotly_chart(fig_categories, use_container_width=True, config=settings.PLOTLY_CONFIG)
        
        # Top 3
        top3 = list(categories_sorted.items())[:3]
        col1, col2, col3 = st.columns(3)
        
        for i, (col, (categorie, valeur)) in enumerate(zip([col1, col2, col3], top3)):
            with col:
                medaille = "🥇" if i == 0 else ("🥈" if i == 1 else "🥉")
                st.metric(
                    label=f"{medaille} Top {i+1}",
                    value=categorie,
                    delta=f"{formater_nombre(valeur)} appels"
                )
    else:
        st.warning(settings.MESSAGES['warning']['no_data'])

# === ONGLET 2 : PAR REGROUPEMENTS ===
with tab2:
    st.markdown("#### Répartition par Regroupement Thématique")
    
    regroupements = totaux_actuel['regroupements']
    
    if regroupements:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Graphique camembert
            fig_regroupements = creer_graphique_camembert(
                data=regroupements,
                titre="Distribution des appels",
                type_graphique='donut',
                show_percentages=True
            )
            st.plotly_chart(fig_regroupements, use_container_width=True, config=settings.PLOTLY_CONFIG)
        
        with col2:
            # Tableau récapitulatif
            st.markdown("##### Détails par Regroupement")
            
            recap_data = []
            total_general = sum(regroupements.values())
            
            for groupe, valeur in sorted(regroupements.items(), key=lambda x: x[1], reverse=True):
                pourcentage = (valeur / total_general * 100) if total_general > 0 else 0
                recap_data.append({
                    'Regroupement': groupe,
                    'Appels': formater_nombre(valeur),
                    '%': f"{pourcentage:.1f}%"
                })
            
            df_recap = pd.DataFrame(recap_data)
            st.dataframe(df_recap, use_container_width=True, hide_index=True, height=250)
    else:
        st.warning(settings.MESSAGES['warning']['no_data'])

# ==============================================================================
# SECTION 3 : COMPARAISON AVEC LA SEMAINE PRÉCÉDENTE
# ==============================================================================

if semaine_precedente:
    section_header("Comparaison avec la Semaine Précédente", icon="🔄")
    
    totaux_precedent = calculer_totaux_semaine(df_appels, semaine_precedente)
    
    # Métriques de comparaison
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📞 Total Appels")
        
        var_total = totaux_actuel['total'] - totaux_precedent['total']
        var_pct = (var_total / totaux_precedent['total'] * 100) if totaux_precedent['total'] > 0 else 0
        
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            st.metric(
                label=semaine_actuelle,
                value=formater_nombre(totaux_actuel['total']),
                delta=f"{var_total:+,} ({var_pct:+.1f}%)".replace(',', ' ')
            )
        
        with subcol2:
            st.metric(
                label=semaine_precedente,
                value=formater_nombre(totaux_precedent['total'])
            )
    
    with col2:
        st.markdown("### 📊 Moyenne Journalière")
        
        var_moy = totaux_actuel['moyenne_jour'] - totaux_precedent['moyenne_jour']
        var_moy_pct = (var_moy / totaux_precedent['moyenne_jour'] * 100) if totaux_precedent['moyenne_jour'] > 0 else 0
        
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            st.metric(
                label=semaine_actuelle,
                value=f"{totaux_actuel['moyenne_jour']:.0f}",
                delta=f"{var_moy:+.1f} ({var_moy_pct:+.1f}%)"
            )
        
        with subcol2:
            st.metric(
                label=semaine_precedente,
                value=f"{totaux_precedent['moyenne_jour']:.0f}"
            )
    
    with col3:
        st.markdown("### 📈 Jours de données")
        
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            st.metric(
                label=semaine_actuelle,
                value=totaux_actuel['nb_jours']
            )
        
        with subcol2:
            st.metric(
                label=semaine_precedente,
                value=totaux_precedent['nb_jours']
            )
    
    # Variations par regroupement
    st.markdown("---")
    st.markdown("#### Variations par Regroupement")
    
    variations_detail = variations.get('regroupements', {})
    
    if variations_detail:
        var_data = []
        for groupe, data in variations_detail.items():
            var_data.append({
                'Regroupement': groupe,
                semaine_precedente: formater_nombre(data['precedent']),
                semaine_actuelle: formater_nombre(data['actuel']),
                'Variation': f"{data['variation_absolue']:+,}".replace(',', ' '),
                'Variation %': f"{data['variation_relative']:+.1f}%"
            })
        
        df_variations = pd.DataFrame(var_data)
        st.dataframe(df_variations, use_container_width=True, hide_index=True)

# ==============================================================================
# SECTION 4 : ÉVOLUTION TEMPORELLE (10 SEMAINES)
# ==============================================================================

section_header("Évolution Temporelle", icon="📈")

# Filtrer les 10 dernières semaines
df_hebdo_sorted = df_hebdo.copy()
df_hebdo_sorted['_sort'] = df_hebdo_sorted['Semaine épidémiologique'].apply(extraire_numero_semaine)
df_hebdo_sorted = df_hebdo_sorted.sort_values('_sort').tail(10).reset_index(drop=True)

if len(df_hebdo_sorted) > 0:
    fig_evolution = creer_graphique_evolution(
        data=df_hebdo_sorted,
        x_col='Semaine épidémiologique',
        y_col='TOTAL_APPELS_SEMAINE',
        titre="Évolution des 10 dernières semaines",
        ajouter_moyenne=True,
        ajouter_tendance=True
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True, config=settings.PLOTLY_CONFIG)
    
    # Statistiques de tendance
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_val = df_hebdo_sorted['TOTAL_APPELS_SEMAINE'].min()
        st.metric("📉 Minimum", formater_nombre(int(min_val)))
    
    with col2:
        max_val = df_hebdo_sorted['TOTAL_APPELS_SEMAINE'].max()
        st.metric("📈 Maximum", formater_nombre(int(max_val)))
    
    with col3:
        moyenne = df_hebdo_sorted['TOTAL_APPELS_SEMAINE'].mean()
        st.metric("📊 Moyenne", formater_nombre(int(moyenne)))
else:
    st.warning(settings.MESSAGES['warning']['no_data'])

# ==============================================================================
# EXPORT DES DONNÉES
# ==============================================================================

with st.expander("💾 Exporter les Données de la Semaine"):
    df_semaine = df_appels[df_appels['Semaine épidémiologique'] == semaine_actuelle]
    
    if len(df_semaine) > 0:
        st.info(f"📊 {len(df_semaine)} jours de données pour {semaine_actuelle}")
        
        export_buttons(
            df_semaine,
            filename_prefix=f"vue_ensemble_{semaine_actuelle}",
            formats=['csv', 'excel']
        )
    else:
        st.warning("Aucune donnée à exporter")

# ==============================================================================
# FOOTER
# ==============================================================================

#page_footer()

# ==============================================================================
# FIN DE LA PAGE
# ==============================================================================