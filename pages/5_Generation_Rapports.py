"""
==============================================================================
PAGE 5 - GÉNÉRATION DE RAPPORTS POWERPOINT - VERSION AMÉLIORÉE
==============================================================================
Page dédiée à la génération automatique de rapports PowerPoint :
- Modèle UNIQUE optimisé (MINSANTE)
- Sélection par semaine OU par période personnalisée (jour début + jour fin)
- Génération automatique avec données actualisées
- Téléchargement du rapport généré
- Historique des rapports

Nouveautés v4.0:
✨ Filtre de dates personnalisé (jour début - jour fin)
✨ Modèle unique optimisé avec graphiques améliorés
✨ Interface simplifiée et intuitive

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 4.0 - Filtre Dates Personnalisées + Modèle Unique Optimisé
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime, timedelta
from pathlib import Path
import traceback
import pandas as pd

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

if 'mode_selection' not in st.session_state:
    st.session_state.mode_selection = "semaine"  # "semaine" ou "periode"

if 'rapport_genere' not in st.session_state:
    st.session_state.rapport_genere = None

if 'date_debut' not in st.session_state:
    st.session_state.date_debut = None

if 'date_fin' not in st.session_state:
    st.session_state.date_fin = None

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
logger.info("=== Page Génération de Rapports v4.0 chargée ===")

# ==============================================================================
# IMPORTS DES GÉNÉRATEURS POWERPOINT
# ==============================================================================

# Générateur OPTIMISÉ (Modèle Unique)
try:
    from utils.pptx_generator_minsante import generer_rapport_minsante
    GENERATOR_AVAILABLE = True
except Exception as e:
    GENERATOR_AVAILABLE = False
    logger.error(f"Générateur non disponible : {e}")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="GÉNÉRATION DE RAPPORTS POWERPOINT",
    subtitle="Rapport MINSANTE avec graphiques optimisés - 7 slides professionnelles",
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
    
    # Récupérer les dates min/max disponibles
    date_min = df_appels['DATE'].min()
    date_max = df_appels['DATE'].max()
    
except Exception as e:
    st.error(settings.MESSAGES['error']['data_inconsistency'])
    logger.error(f"Erreur chargement : {str(e)}")
    st.stop()

# ==============================================================================
# VÉRIFICATION DISPONIBILITÉ GÉNÉRATEUR
# ==============================================================================

if not GENERATOR_AVAILABLE:
    st.error("❌ **Générateur de rapport non disponible**")
    st.error("Vérifiez que le fichier `utils/pptx_generator_minsante.py` existe et est correct.")
    st.stop()

# ==============================================================================
# SECTION 1 : MODE DE SÉLECTION
# ==============================================================================

section_header("Mode de Sélection de Période", icon="📅")

st.info("""
**Deux options disponibles :**

📊 **Par semaine épidémiologique** : Sélectionnez une semaine complète (S1, S2, etc.)  
📅 **Par période personnalisée** : Choisissez n'importe quel jour de début et jour de fin
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Sélection par SEMAINE", 
                 use_container_width=True, 
                 type="primary" if st.session_state.mode_selection == "semaine" else "secondary"):
        st.session_state.mode_selection = "semaine"
        st.session_state.rapport_genere = None
        st.rerun()

with col2:
    if st.button("📅 Sélection par PÉRIODE (Jour début - Jour fin)", 
                 use_container_width=True,
                 type="primary" if st.session_state.mode_selection == "periode" else "secondary"):
        st.session_state.mode_selection = "periode"
        st.session_state.rapport_genere = None
        st.rerun()

# Afficher le mode sélectionné
mode_label = {
    "semaine": "📊 Sélection par Semaine Épidémiologique",
    "periode": "📅 Sélection par Période Personnalisée"
}
st.success(f"✅ Mode actif : **{mode_label[st.session_state.mode_selection]}**")

st.markdown("---")

# ==============================================================================
# SECTION 2 : CONFIGURATION SELON LE MODE
# ==============================================================================

section_header("Configuration du Rapport", icon="⚙️")

if st.session_state.mode_selection == "semaine":
    # ========================================================================
    # MODE SEMAINE ÉPIDÉMIOLOGIQUE
    # ========================================================================
    
    st.markdown("### 📊 Sélection par Semaine Épidémiologique")
    
    col1, col2 = st.columns([2, 1])
    
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
        
        # Afficher les dates de la semaine
        df_semaine_info = df_appels[df_appels['Semaine épidémiologique'] == semaine_selectionnee]
        date_debut_semaine = df_semaine_info['DATE'].min()
        date_fin_semaine = df_semaine_info['DATE'].max()
        
        st.info(f"📅 Période : **{date_debut_semaine.strftime('%d/%m/%Y')}** au **{date_fin_semaine.strftime('%d/%m/%Y')}**")
    
    with col2:
        # Statistiques de la semaine
        st.markdown("**📊 Aperçu de la semaine :**")
        total_appels = df_semaine_info['TOTAL_APPELS_JOUR'].sum()
        nb_jours = len(df_semaine_info)
        
        st.metric("Total Appels", f"{total_appels:,}".replace(",", " "))
        st.metric("Jours de données", nb_jours)
    
    # Variables pour la génération
    data_debut = date_debut_semaine
    data_fin = date_fin_semaine
    mode_generation = "semaine"
    periode_label = semaine_selectionnee

else:
    # ========================================================================
    # MODE PÉRIODE PERSONNALISÉE
    # ========================================================================
    
    st.markdown("### 📅 Sélection par Période Personnalisée")
    
    st.info(f"""
    📊 **Données disponibles :**  
    Du **{date_min.strftime('%d/%m/%Y')}** au **{date_max.strftime('%d/%m/%Y')}**
    
    Sélectionnez n'importe quelle période dans cette plage.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date de début
        date_debut_input = st.date_input(
            "📅 Date de DÉBUT",
            value=date_max - timedelta(days=6),  # Par défaut : dernière semaine
            min_value=date_min,
            max_value=date_max,
            help="Premier jour de la période",
            format="DD/MM/YYYY"
        )
        
        st.session_state.date_debut = pd.to_datetime(date_debut_input)
    
    with col2:
        # Date de fin
        date_fin_input = st.date_input(
            "📅 Date de FIN",
            value=date_max,
            min_value=date_min,
            max_value=date_max,
            help="Dernier jour de la période",
            format="DD/MM/YYYY"
        )
        
        st.session_state.date_fin = pd.to_datetime(date_fin_input)
    
    # Validation de la période
    if st.session_state.date_debut > st.session_state.date_fin:
        st.error("❌ **Erreur** : La date de début doit être antérieure ou égale à la date de fin")
        st.stop()
    
    # Calculer la durée
    duree_periode = (st.session_state.date_fin - st.session_state.date_debut).days + 1
    
    # Filtrer les données de la période
    df_periode = df_appels[
        (df_appels['DATE'] >= st.session_state.date_debut) & 
        (df_appels['DATE'] <= st.session_state.date_fin)
    ]
    
    # Vérifier qu'il y a des données
    if len(df_periode) == 0:
        st.warning("⚠️ **Aucune donnée disponible pour cette période**")
        st.stop()
    
    # Afficher les statistiques de la période
    st.markdown("---")
    st.markdown("### 📊 Aperçu de la Période Sélectionnée")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Durée", f"{duree_periode} jour(s)")
    
    with col2:
        total_appels_periode = df_periode['TOTAL_APPELS_JOUR'].sum()
        st.metric("Total Appels", f"{total_appels_periode:,}".replace(",", " "))
    
    with col3:
        moyenne_periode = int(df_periode['TOTAL_APPELS_JOUR'].mean())
        st.metric("Moyenne/Jour", f"{moyenne_periode:,}".replace(",", " "))
    
    with col4:
        nb_jours_data = len(df_periode)
        st.metric("Jours de données", nb_jours_data)
    
    # Variables pour la génération
    data_debut = st.session_state.date_debut
    data_fin = st.session_state.date_fin
    mode_generation = "periode"
    periode_label = f"{data_debut.strftime('%d/%m/%Y')} au {data_fin.strftime('%d/%m/%Y')}"

# ==============================================================================
# RÉCAPITULATIF DE LA CONFIGURATION
# ==============================================================================

st.markdown("---")
st.markdown("### 📋 Récapitulatif de la Configuration")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Modèle", "MINSANTE Optimisé")

with col2:
    st.metric("Période", periode_label)

with col3:
    st.metric("Slides", "7")

with col4:
    nb_jours_rapport = (data_fin - data_debut).days + 1
    st.metric("Jours", nb_jours_rapport)

# ==============================================================================
# SECTION 3 : GÉNÉRATION DU RAPPORT
# ==============================================================================

st.markdown("---")
section_header("Génération du Rapport", icon="🚀")

# Informations avant génération
st.info("""
**Avant de générer :**

✅ Vérifiez la période sélectionnée  
✅ La génération peut prendre 20-40 secondes  
✅ Le fichier sera téléchargeable immédiatement après génération

**Contenu du rapport :**
- 📊 Slide 1 : Page de titre avec drapeau du Cameroun
- 📈 Slide 2 : Faits saillants avec 3 graphiques camembert optimisés
- 📋 Slide 3 : Tableau de comparaison
- 📊 Slide 4 : Graphique d'évolution avec étiquettes
- 💬 Slide 5 : Questions d'intérêt
- ✅ Slide 6 : Activités menées et planifiées
- 🙏 Slide 7 : Remerciements
""")

# Bouton de génération
if st.button("🎯 GÉNÉRER LE RAPPORT POWERPOINT", type="primary", use_container_width=True, key="btn_generer"):
    
    with st.spinner(f"⏳ Génération du rapport pour la période {periode_label} en cours..."):
        
        try:
            start_time = datetime.now()
            
            # Générer le nom de fichier
            if mode_generation == "semaine":
                prefix = f"rapport_MINSANTE_{periode_label}"
            else:
                prefix = f"rapport_MINSANTE_{data_debut.strftime('%Y%m%d')}_{data_fin.strftime('%Y%m%d')}"
            
            filename = generer_nom_fichier(
                prefix,
                extension='pptx',
                include_timestamp=True
            )
            
            output_path = settings.OUTPUTS_DIR / filename
            
            # S'assurer que le dossier outputs existe
            settings.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
            
            # Filtrer les données pour la période sélectionnée
            if mode_generation == "semaine":
                df_filtered = df_appels[df_appels['Semaine épidémiologique'] == periode_label]
                semaine_param = periode_label
            else:
                df_filtered = df_appels[
                    (df_appels['DATE'] >= data_debut) & 
                    (df_appels['DATE'] <= data_fin)
                ]
                # Pour mode période, on utilise la semaine de la date de fin
                semaine_param = df_filtered['Semaine épidémiologique'].iloc[-1] if len(df_filtered) > 0 else "CUSTOM"
            
            # Appeler le générateur
            output_file = generer_rapport_minsante(
                df_appels=df_filtered,
                df_calendrier=df_calendrier,
                semaine=semaine_param,
                output_path=str(output_path)
            )
            
            # Calculer la durée
            duree = (datetime.now() - start_time).total_seconds()
            
            # Vérifier que le fichier existe
            if Path(output_file).exists():
                # Stocker les infos du rapport dans session_state
                st.session_state.rapport_genere = {
                    'fichier': output_file,
                    'nom': filename,
                    'duree': duree,
                    'taille': Path(output_file).stat().st_size / 1024 / 1024,
                    'periode': periode_label,
                    'mode': mode_generation
                }
                
                st.success(f"✅ Rapport généré avec succès en {duree:.1f}s !")
                st.balloons()
                
                # Logs
                log_generation_rapport(
                    modele="MINSANTE_OPTIMISE",
                    nb_slides=7,
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
                modele="MINSANTE_OPTIMISE",
                success=False,
                message=str(e)
            )
            logger.error(f"Erreur génération rapport : {str(e)}")

# ==============================================================================
# SECTION 4 : TÉLÉCHARGEMENT
# ==============================================================================

# Afficher le bouton de téléchargement si un rapport a été généré
if st.session_state.rapport_genere:
    st.markdown("---")
    section_header("Téléchargement du Rapport", icon="📥")
    
    info = st.session_state.rapport_genere
    
    # Informations sur le rapport généré
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 Fichier", info['nom'][:30] + "...")
    
    with col2:
        st.metric("📏 Taille", f"{info['taille']:.2f} MB")
    
    with col3:
        st.metric("⏱️ Temps de génération", f"{info['duree']:.1f}s")
    
    # Bouton de téléchargement
    with open(info['fichier'], 'rb') as f:
        st.download_button(
            label="📥 TÉLÉCHARGER LE RAPPORT POWERPOINT",
            data=f,
            file_name=info['nom'],
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
            type="primary"
        )
    
    st.success(f"✅ Rapport pour la période **{info['periode']}** prêt au téléchargement")

# ==============================================================================
# SECTION 5 : HISTORIQUE DES RAPPORTS
# ==============================================================================

st.markdown("---")

with st.expander("📂 Historique des Rapports Générés", expanded=False):
    
    st.markdown("### 📁 Rapports Disponibles")
    
    # Lister les fichiers PPTX dans outputs/
    if settings.OUTPUTS_DIR.exists():
        fichiers_pptx = sorted(
            settings.OUTPUTS_DIR.glob("rapport_*.pptx"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if fichiers_pptx:
            st.info(f"📊 **{len(fichiers_pptx)} rapport(s) disponible(s)**")
            
            # Tableau des rapports
            for idx, fichier in enumerate(fichiers_pptx[:15], 1):  # Limiter à 15 derniers
                col1, col2, col3, col4, col5 = st.columns([1, 4, 2, 2, 1])
                
                stats = fichier.stat()
                taille = stats.st_size / 1024 / 1024
                date_modif = datetime.fromtimestamp(stats.st_mtime)
                
                with col1:
                    st.write(f"**#{idx}**")
                
                with col2:
                    st.write(f"📄 {fichier.name[:50]}...")
                
                with col3:
                    st.write(f"📏 {taille:.2f} MB")
                
                with col4:
                    st.write(f"🕐 {date_modif.strftime('%d/%m/%Y %H:%M')}")
                
                with col5:
                    with open(fichier, 'rb') as f:
                        st.download_button(
                            "📥",
                            data=f,
                            file_name=fichier.name,
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            key=f"download_{idx}_{fichier.name}",
                            help="Télécharger ce rapport"
                        )
                
                if idx < len(fichiers_pptx):
                    st.markdown("---")
        else:
            st.info("📭 Aucun rapport généré pour le moment")
    else:
        st.warning("⚠️ Dossier outputs/ introuvable")

# ==============================================================================
# SECTION 6 : GUIDE D'UTILISATION
# ==============================================================================

with st.expander("ℹ️ Guide d'Utilisation", expanded=False):
    st.markdown("""
    ### 📖 Comment générer un rapport ?
    
    **Étape 1 : Choisir le Mode de Sélection**
    
    🔹 **Mode Semaine** : Sélectionner une semaine épidémiologique complète
    - Parfait pour les rapports hebdomadaires standards
    - Période pré-définie (du lundi au dimanche)
    
    🔹 **Mode Période Personnalisée** : Choisir n'importe quelle période
    - Jour de début et jour de fin libres
    - Parfait pour des analyses sur mesure
    - Exemples : du 1er au 15, du 10 au 20, etc.
    
    **Étape 2 : Configuration**
    
    - **Mode Semaine** : Sélectionnez la semaine dans la liste déroulante
    - **Mode Période** : Choisissez la date de début et la date de fin
    
    **Étape 3 : Génération**
    
    - Vérifiez le récapitulatif de la configuration
    - Cliquez sur "GÉNÉRER LE RAPPORT POWERPOINT"
    - Attendez 20-40 secondes
    - Téléchargez le fichier PowerPoint
    
    ### 📊 Contenu du Rapport (7 Slides)
    
    **Slide 1 : Page de Titre**
    - Drapeau du Cameroun
    - Titre du rapport
    - Date de la période
    
    **Slide 2 : Faits Saillants**
    - Total des appels
    - 3 graphiques camembert optimisés :
      - Renseignements Santé (palette bleue)
      - Assistances Médicales (palette rouge)
      - Signaux de Surveillance (palette violette)
    - Étiquettes avec pourcentages et valeurs
    
    **Slide 3 : Comparaison**
    - Tableau de comparaison avec la période précédente
    - Évolution par catégorie
    
    **Slide 4 : Évolution**
    - Graphique en colonnes avec tri automatique
    - Étiquettes de données
    - Tendances visuelles
    
    **Slide 5 : Questions d'Intérêt**
    - Top 5 questions posées au 1510
    - Formatage professionnel
    
    **Slide 6 : Activités**
    - Tableau 2x2 : Activités menées / Activités planifiées
    - Vision synthétique des actions
    
    **Slide 7 : Remerciements**
    - Slide de clôture
    - Fond vert Cameroun
    
    ### 🎨 Améliorations Graphiques v4.0
    
    ✨ **Couleurs optimisées pour PowerPoint**
    - Palettes vives et contrastées
    - Différenciation visuelle par thématique
    
    ✨ **Étiquettes améliorées**
    - Pourcentages + Valeurs affichés
    - Police blanche en gras pour contraste
    - Position optimisée (INSIDE_END)
    
    ✨ **Légendes professionnelles**
    - Placement en bas
    - Taille de police adaptée
    - Ne surcharge pas le graphique
    
    ### 💡 Conseils d'Utilisation
    
    ✅ **Pour les rapports hebdomadaires standards**
    - Utilisez le mode "Semaine"
    - Générez le rapport chaque semaine
    
    ✅ **Pour des analyses spécifiques**
    - Utilisez le mode "Période"
    - Choisissez n'importe quelle plage de dates
    - Exemples : début/fin de mois, périodes de pics, etc.
    
    ✅ **Avant une présentation**
    - Générez le rapport à l'avance
    - Vérifiez les données
    - Conservez plusieurs versions dans l'historique
    
    ### 🔧 Dépannage
    
    **Le rapport ne se génère pas ?**
    - Vérifiez que la période contient des données
    - Vérifiez que les fichiers sont bien chargés
    - Consultez les détails de l'erreur
    
    **Le téléchargement ne fonctionne pas ?**
    - Vérifiez votre navigateur
    - Réessayez la génération
    - Consultez l'historique des rapports
    
    **Les graphiques sont vides ?**
    - Vérifiez que la période contient des appels
    - Certaines catégories peuvent être à zéro
    
    ### 📞 Support
    
    Pour toute question ou assistance :
    - Consultez la documentation technique
    - Contactez l'équipe MINSANTE/CCOUSP
    """)

# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Dashboard Centre d'Appels d'Urgence Sanitaire 1510</strong></p>
    <p>Centre de Coordination des Urgences de Santé Publique (CCOUSP) - MINSANTE</p>
    <p>Version 4.0 - Décembre 2025</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# FIN DE LA PAGE
# ==============================================================================