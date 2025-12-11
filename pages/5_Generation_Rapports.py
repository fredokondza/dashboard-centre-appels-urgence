"""
==============================================================================
PAGE 5 - GÉNÉRATION DE RAPPORTS POWERPOINT
==============================================================================
Page dédiée à la génération automatique de rapports PowerPoint :
- 3 modèles disponibles (Original, A, B)
- Sélection de la semaine épidémiologique
- Génération automatique avec données actualisées
- Téléchargement du rapport généré
- Historique des rapports

Modèles disponibles :
- Modèle Original : 7 slides (Standard MINSANTE)
- Modèle A : 16 slides (Analyse détaillée)
- Modèle B : 12 slides (Format condensé)

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.1 FINALE - Session State + Footer CCOUSP/MINSANTE
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from pathlib import Path
import traceback

# Imports de la nouvelle architecture
from config import settings
from utils.data_loader import charger_toutes_les_donnees
from utils.helpers import extraire_numero_semaine, generer_nom_fichier
from utils.logger import setup_logger, log_generation_rapport
from components.layout import apply_custom_css, page_header, section_header
from components.sidebar import render_sidebar

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

st.set_page_config(
    page_title="Génération de Rapports - Dashboard Urgence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# INITIALISATION SESSION STATE
# ==============================================================================

if 'modele_selectionne' not in st.session_state:
    st.session_state.modele_selectionne = None

if 'rapport_genere' not in st.session_state:
    st.session_state.rapport_genere = None

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

logger = setup_logger('generation_rapports')
logger.info("=== Page Génération de Rapports chargée ===")

# ==============================================================================
# IMPORTS DES GÉNÉRATEURS POWERPOINT
# ==============================================================================

# Générateur ORIGINAL
try:
    from utils.pptx_generator_minsante import generer_rapport_minsante
    ORIGINAL_AVAILABLE = True
except Exception as e:
    ORIGINAL_AVAILABLE = False
    logger.error(f"Générateur ORIGINAL non disponible : {e}")

# Générateur AVANCÉ
try:
    from utils.pptx_generator_advanced import generer_rapport_avance
    ADVANCED_AVAILABLE = True
except Exception as e:
    ADVANCED_AVAILABLE = False
    logger.error(f"Générateur AVANCÉ non disponible : {e}")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="GÉNÉRATION DE RAPPORTS POWERPOINT",
    subtitle="Rapports automatisés au format MINSANTE",
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
    df_calendrier = donnees['calendrier']
    df_hebdo = donnees['hebdomadaire']
    
except Exception as e:
    st.error(settings.MESSAGES['error']['data_inconsistency'])
    logger.error(f"Erreur chargement : {str(e)}")
    st.stop()

# ==============================================================================
# SECTION 1 : SÉLECTION DU MODÈLE
# ==============================================================================

section_header("Sélection du Modèle de Rapport", icon="📋")

st.info(
    "Choisissez le modèle de rapport selon vos besoins : analyse standard, détaillée ou condensée"
)

# Afficher les modèles disponibles
col1, col2, col3 = st.columns(3)

with col1:
    # Modèle Original
    st.markdown("### 📄 Modèle Original")
    st.markdown("**7 slides - Format standard MINSANTE**")
    st.markdown("""
    - Page de titre
    - Faits saillants
    - Comparaison semaine précédente
    - Top 10 catégories
    - Répartition thématique
    - Évolution temporelle
    - Contact
    """)
    
    if ORIGINAL_AVAILABLE:
        if st.button("✅ Sélectionner", key="btn_original", use_container_width=True):
            st.session_state.modele_selectionne = "ORIGINAL"
            st.session_state.rapport_genere = None
            st.rerun()
    else:
        st.error("❌ Non disponible")

with col2:
    # Modèle A (Avancé)
    st.markdown("### 📊 Modèle A - Détaillé")
    st.markdown("**16 slides - Analyse approfondie**")
    st.markdown("""
    - Analyse détaillée par catégorie
    - Graphiques comparatifs avancés
    - Statistiques détaillées
    - Analyse des variations
    - Tendances et projections
    - Annexes complètes
    """)
    
    if ADVANCED_AVAILABLE:
        if st.button("✅ Sélectionner", key="btn_a", use_container_width=True):
            st.session_state.modele_selectionne = "A"
            st.session_state.rapport_genere = None
            st.rerun()
    else:
        st.error("❌ Non disponible")

with col3:
    # Modèle B (Condensé)
    st.markdown("### 📑 Modèle B - Condensé")
    st.markdown("**12 slides - Format compact**")
    st.markdown("""
    - Synthèse des KPIs
    - Top catégories uniquement
    - Comparaison simplifiée
    - Graphiques essentiels
    - Format de présentation rapide
    """)
    
    if ADVANCED_AVAILABLE:
        if st.button("✅ Sélectionner", key="btn_b", use_container_width=True):
            st.session_state.modele_selectionne = "B"
            st.session_state.rapport_genere = None
            st.rerun()
    else:
        st.error("❌ Non disponible")

# Afficher le modèle sélectionné
if st.session_state.modele_selectionne:
    modele_label = {
        "ORIGINAL": "Modèle Original",
        "A": "Modèle A - Détaillé",
        "B": "Modèle B - Condensé"
    }
    st.success(f"✅ {modele_label[st.session_state.modele_selectionne]} sélectionné")
    
    # Bouton pour changer de modèle
    if st.button("🔄 Changer de modèle", key="btn_reset"):
        st.session_state.modele_selectionne = None
        st.session_state.rapport_genere = None
        st.rerun()

# ==============================================================================
# SECTION 2 : CONFIGURATION DU RAPPORT
# ==============================================================================

if st.session_state.modele_selectionne:
    
    section_header("Configuration du Rapport", icon="⚙️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sélection de la semaine
        semaines_disponibles = sorted(
            df_appels['Semaine épidémiologique'].unique(),
            key=extraire_numero_semaine,
            reverse=True
        )
        
        semaine_selectionnee = st.selectbox(
            "📊 Sélectionnez la semaine épidémiologique :",
            semaines_disponibles,
            index=0,
            help="La semaine sur laquelle portera le rapport"
        )
    
    with col2:
        # Options du rapport
        st.markdown("**Options :**")
        
        # Options selon le modèle
        if st.session_state.modele_selectionne == "ORIGINAL":
            inclure_comparaison = st.checkbox("Inclure comparaison semaine précédente", value=True)
            inclure_evolution = st.checkbox("Inclure graphique d'évolution", value=True)
        elif st.session_state.modele_selectionne == "A":
            inclure_annexes = st.checkbox("Inclure annexes complètes", value=True)
            inclure_projections = st.checkbox("Inclure projections", value=False)
        else:  # Modèle B
            format_compact = st.checkbox("Format ultra-compact", value=False)
    
    # Aperçu de la configuration
    st.markdown("---")
    st.markdown("### 📋 Récapitulatif de la Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Modèle", st.session_state.modele_selectionne)
    with col2:
        st.metric("Semaine", semaine_selectionnee)
    with col3:
        nb_slides = 7 if st.session_state.modele_selectionne == "ORIGINAL" else (16 if st.session_state.modele_selectionne == "A" else 12)
        st.metric("Slides", nb_slides)
    
    # ==============================================================================
    # SECTION 3 : GÉNÉRATION DU RAPPORT
    # ==============================================================================
    
    section_header("Génération du Rapport", icon="🚀")
    
    # Informations avant génération
    st.info("""
    **Avant de générer :**
    
    ✅ Vérifiez la semaine sélectionnée  
    ✅ Vérifiez les options configurées  
    ✅ La génération peut prendre 20-40 secondes  
    
    Le fichier sera disponible au téléchargement après génération.
    """)
    
    # Bouton de génération
    if st.button("🎯 GÉNÉRER LE RAPPORT", type="primary", use_container_width=True, key="btn_generer"):
        
        with st.spinner(f"⏳ Génération du rapport Modèle {st.session_state.modele_selectionne} en cours..."):
            
            try:
                start_time = datetime.now()
                
                # Générer le nom de fichier
                filename = generer_nom_fichier(
                    f"rapport_{st.session_state.modele_selectionne}_{semaine_selectionnee}",
                    extension='pptx',
                    include_timestamp=True
                )
                
                output_path = settings.OUTPUTS_DIR / filename
                
                # S'assurer que le dossier outputs existe
                settings.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
                
                # Appeler le générateur approprié
                if st.session_state.modele_selectionne == "ORIGINAL":
                    if ORIGINAL_AVAILABLE:
                        output_file = generer_rapport_minsante(
                            df_appels=df_appels,
                            df_calendrier=df_calendrier,
                            semaine=semaine_selectionnee,
                            output_path=str(output_path)
                        )
                    else:
                        raise Exception("Générateur Original non disponible")
                
                elif st.session_state.modele_selectionne in ["A", "B"]:
                    if ADVANCED_AVAILABLE:
                        output_file = generer_rapport_avance(
                            df_appels=df_appels,
                            df_calendrier=df_calendrier,
                            semaine=semaine_selectionnee,
                            modele=st.session_state.modele_selectionne,
                            output_path=str(output_path)
                        )
                    else:
                        raise Exception("Générateur Avancé non disponible")
                
                # Calculer la durée
                duree = (datetime.now() - start_time).total_seconds()
                
                # Vérifier que le fichier existe
                if Path(output_file).exists():
                    # Stocker les infos du rapport dans session_state
                    st.session_state.rapport_genere = {
                        'fichier': output_file,
                        'nom': filename,
                        'duree': duree,
                        'taille': Path(output_file).stat().st_size / 1024 / 1024
                    }
                    
                    st.success(f"✅ Rapport généré avec succès en {duree:.1f}s !")
                    st.balloons()
                    
                    # Logs
                    log_generation_rapport(
                        modele=st.session_state.modele_selectionne,
                        nb_slides=nb_slides,
                        success=True,
                        duree=duree
                    )
                    
                else:
                    raise Exception("Le fichier n'a pas été créé")
            
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération : {str(e)}")
                
                # Afficher le traceback pour le debugging
                with st.expander("🔍 Détails de l'erreur"):
                    st.code(traceback.format_exc())
                
                log_generation_rapport(
                    modele=st.session_state.modele_selectionne,
                    success=False,
                    message=str(e)
                )
                logger.error(f"Erreur génération rapport : {str(e)}")
    
    # Afficher le bouton de téléchargement si un rapport a été généré
    if st.session_state.rapport_genere:
        st.markdown("---")
        st.markdown("### 📥 Téléchargement")
        
        info = st.session_state.rapport_genere
        
        with open(info['fichier'], 'rb') as f:
            st.download_button(
                label="📥 TÉLÉCHARGER LE RAPPORT",
                data=f,
                file_name=info['nom'],
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
                type="primary"
            )
        
        st.info(f"📊 Fichier : `{info['nom']}` ({info['taille']:.2f} MB) - Généré en {info['duree']:.1f}s")

else:
    # Aucun modèle sélectionné
    if not ORIGINAL_AVAILABLE and not ADVANCED_AVAILABLE:
        st.error("❌ Aucun générateur de rapport disponible. Vérifiez les fichiers dans utils/")
    else:
        st.info("👆 Sélectionnez un modèle de rapport ci-dessus pour commencer")

# ==============================================================================
# SECTION 4 : HISTORIQUE DES RAPPORTS
# ==============================================================================

with st.expander("📂 Historique des Rapports Générés"):
    
    st.markdown("### 📁 Rapports Disponibles")
    
    # Lister les fichiers PPTX dans outputs/
    if settings.OUTPUTS_DIR.exists():
        fichiers_pptx = sorted(
            settings.OUTPUTS_DIR.glob("rapport_*.pptx"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if fichiers_pptx:
            st.info(f"📊 {len(fichiers_pptx)} rapport(s) disponible(s)")
            
            for fichier in fichiers_pptx[:10]:  # Limiter à 10 derniers
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                
                stats = fichier.stat()
                taille = stats.st_size / 1024 / 1024
                date_modif = datetime.fromtimestamp(stats.st_mtime)
                
                with col1:
                    st.write(f"📄 {fichier.name}")
                
                with col2:
                    st.write(f"📏 {taille:.2f} MB")
                
                with col3:
                    st.write(f"🕐 {date_modif.strftime('%d/%m/%Y %H:%M')}")
                
                with col4:
                    with open(fichier, 'rb') as f:
                        st.download_button(
                            "📥",
                            data=f,
                            file_name=fichier.name,
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            key=f"download_{fichier.name}"
                        )
                
                st.markdown("---")
        else:
            st.info("Aucun rapport généré pour le moment")
    else:
        st.warning("Dossier outputs/ introuvable")

# ==============================================================================
# GUIDE D'UTILISATION
# ==============================================================================

with st.expander("ℹ️ Guide d'Utilisation"):
    st.markdown("""
    ### 📖 Comment générer un rapport ?
    
    **Étape 1 : Sélection du Modèle**
    - Cliquez sur "Sélectionner" sous le modèle souhaité
    - Chaque modèle a un format et un nombre de slides différent
    
    **Étape 2 : Configuration**
    - Choisissez la semaine épidémiologique
    - Configurez les options selon le modèle
    
    **Étape 3 : Génération**
    - Cliquez sur "GÉNÉRER LE RAPPORT"
    - Attendez 20-40 secondes
    - Téléchargez le fichier PowerPoint
    
    ### 📊 Descriptions des Modèles
    
    **Modèle Original (7 slides)**
    - Format standard MINSANTE
    - Adapté aux présentations officielles
    - Durée : ~25 secondes
    
    **Modèle A (16 slides)**
    - Analyse détaillée et complète
    - Pour les rapports approfondis
    - Durée : ~40 secondes
    
    **Modèle B (12 slides)**
    - Format condensé et synthétique
    - Pour les présentations rapides
    - Durée : ~30 secondes
    
    ### 💡 Conseils
    - Générez les rapports avant les réunions
    - Conservez les versions historiques
    - Vérifiez les données avant génération
    """)

# ==============================================================================
# FIN DE LA PAGE
# ==============================================================================