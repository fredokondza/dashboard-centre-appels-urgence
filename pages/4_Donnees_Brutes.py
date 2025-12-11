"""
==============================================================================
PAGE 4 - DONNÉES BRUTES
==============================================================================
Page dédiée à la consultation et l'export des données brutes :
- Consultation des données journalières
- Consultation des données hebdomadaires
- Consultation du calendrier épidémiologique
- Filtrage et recherche avancée
- Export des données (CSV, Excel)
- Upload et mise à jour des fichiers
- Historique des sauvegardes

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.2 FINALE - Calendrier corrigé + Upload fonctionnel + Footer CCOUSP/MINSANTE
==============================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import shutil
from pathlib import Path
from datetime import datetime

# Imports de la nouvelle architecture
from config import settings
from utils.data_loader import charger_toutes_les_donnees, detecter_fichiers_data
from utils.helpers import formater_nombre
from utils.logger import setup_logger, log_upload_fichier, log_export
from components.layout import apply_custom_css, page_header, section_header
from components.sidebar import render_sidebar
from components.metrics import metric_row
from components.tables import display_dataframe_formatted, export_buttons

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

st.set_page_config(
    page_title="Données Brutes - Dashboard Urgence",
    page_icon="📋",
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

logger = setup_logger('donnees_brutes')
logger.info("=== Page Données Brutes chargée ===")

# ==============================================================================
# SIDEBAR
# ==============================================================================

render_sidebar()

# ==============================================================================
# HEADER
# ==============================================================================

page_header(
    title="DONNÉES BRUTES",
    subtitle="Consultation, Export et Gestion des Données",
    icon="📋"
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
# ONGLETS PRINCIPAUX
# ==============================================================================

section_header("Gestion des Données", icon="📊")

tab_consultation, tab_gestion = st.tabs(["👁️ Consultation & Export", "📤 Upload & Mise à Jour"])

# ==============================================================================
# TAB 1 : CONSULTATION ET EXPORT
# ==============================================================================

with tab_consultation:
    
    type_donnees = st.radio(
        "Sélectionnez le type de données à consulter :",
        ["Données Journalières", "Données Hebdomadaires", "Calendrier Épidémiologique"],
        horizontal=True
    )
    
    # ========== DONNÉES JOURNALIÈRES ==========
    if type_donnees == "Données Journalières":
        
        section_header("Données Journalières", icon="📅")
        
        # Informations générales
        metrics = [
            {'label': 'Lignes', 'value': len(df_appels), 'icon': '📊'},
            {'label': 'Date Début', 'value': df_appels['DATE'].min().strftime('%d/%m/%Y'), 'icon': '📅'},
            {'label': 'Date Fin', 'value': df_appels['DATE'].max().strftime('%d/%m/%Y'), 'icon': '📅'},
            {'label': 'Semaines', 'value': df_appels['Semaine épidémiologique'].nunique(), 'icon': '🗓️'}
        ]
        
        metric_row(metrics, columns=4)
        
        # === FILTRES ===
        st.markdown("### 🔍 Filtres")
        
        col1, col2 = st.columns(2)
        
        with col1:
            semaines_disponibles = ['Toutes'] + sorted(df_appels['Semaine épidémiologique'].unique().tolist())
            semaine_filtre = st.selectbox("Filtrer par semaine :", semaines_disponibles)
        
        with col2:
            use_date_filter = st.checkbox("Filtrer par plage de dates")
        
        df_filtered = df_appels.copy()
        
        if semaine_filtre != 'Toutes':
            df_filtered = df_filtered[df_filtered['Semaine épidémiologique'] == semaine_filtre]
        
        if use_date_filter:
            col1, col2 = st.columns(2)
            with col1:
                date_debut = st.date_input(
                    "Date de début :",
                    value=df_appels['DATE'].min().date(),
                    min_value=df_appels['DATE'].min().date(),
                    max_value=df_appels['DATE'].max().date()
                )
            with col2:
                date_fin = st.date_input(
                    "Date de fin :",
                    value=df_appels['DATE'].max().date(),
                    min_value=df_appels['DATE'].min().date(),
                    max_value=df_appels['DATE'].max().date()
                )
            
            df_filtered = df_filtered[
                (df_filtered['DATE'].dt.date >= date_debut) & 
                (df_filtered['DATE'].dt.date <= date_fin)
            ]
        
        st.info(f"📊 **{len(df_filtered)}** lignes correspondent aux critères")
        
        # === AFFICHAGE ===
        st.markdown("### 📋 Tableau des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            colonnes_a_afficher = st.multiselect(
                "Colonnes à afficher :",
                df_filtered.columns.tolist(),
                default=['DATE', 'Semaine épidémiologique', 'TOTAL_APPELS_JOUR', 
                        'CSU_JOUR', 'PHARMACIE_JOUR', 'URGENCE_MEDICALE_JOUR'][:min(6, len(df_filtered.columns))]
            )
        
        with col2:
            nb_lignes = st.slider("Lignes à afficher :", 10, len(df_filtered), min(50, len(df_filtered)))
        
        if colonnes_a_afficher:
            display_dataframe_formatted(
                df_filtered[colonnes_a_afficher].head(nb_lignes),
                height=600
            )
        else:
            st.warning("⚠️ Sélectionnez au moins une colonne")
        
        # === STATISTIQUES ===
        with st.expander("📊 Statistiques Descriptives"):
            colonnes_numeriques = df_filtered.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if colonnes_numeriques:
                stats = df_filtered[colonnes_numeriques].describe()
                st.dataframe(stats, use_container_width=True)
            else:
                st.info("Aucune colonne numérique")
        
        # === EXPORT ===
        st.markdown("### 💾 Export des Données")
        export_buttons(df_filtered, filename_prefix="donnees_journalieres")
    
    # ========== DONNÉES HEBDOMADAIRES ==========
    elif type_donnees == "Données Hebdomadaires":
        
        section_header("Données Hebdomadaires (Agrégées)", icon="📊")
        
        # Informations
        total_appels = df_hebdo['TOTAL_APPELS_SEMAINE'].sum()
        moyenne = df_hebdo['TOTAL_APPELS_SEMAINE'].mean()
        maximum = df_hebdo['TOTAL_APPELS_SEMAINE'].max()
        
        metrics = [
            {'label': 'Semaines', 'value': len(df_hebdo), 'icon': '📊'},
            {'label': 'Total Appels', 'value': int(total_appels), 'icon': '📞'},
            {'label': 'Moyenne/Semaine', 'value': int(moyenne), 'icon': '📊'},
            {'label': 'Maximum', 'value': int(maximum), 'icon': '📈'}
        ]
        
        metric_row(metrics, columns=4)
        
        # === FILTRES ===
        st.markdown("### 🔍 Filtres")
        
        col1, col2 = st.columns(2)
        
        with col1:
            semaines_disponibles = sorted(df_hebdo['Semaine épidémiologique'].unique().tolist())
            semaines_selectionnees = st.multiselect(
                "Semaines à afficher (vide = toutes) :",
                semaines_disponibles,
                default=[]
            )
        
        with col2:
            use_seuil = st.checkbox("Filtrer par seuil d'appels")
            if use_seuil:
                seuil_min = st.number_input(
                    "Minimum d'appels :",
                    min_value=0,
                    max_value=int(df_hebdo['TOTAL_APPELS_SEMAINE'].max()),
                    value=0
                )
        
        df_hebdo_filtered = df_hebdo.copy()
        
        if semaines_selectionnees:
            df_hebdo_filtered = df_hebdo_filtered[
                df_hebdo_filtered['Semaine épidémiologique'].isin(semaines_selectionnees)
            ]
        
        if use_seuil:
            df_hebdo_filtered = df_hebdo_filtered[
                df_hebdo_filtered['TOTAL_APPELS_SEMAINE'] >= seuil_min
            ]
        
        st.info(f"📊 **{len(df_hebdo_filtered)}** semaines correspondent aux critères")
        
        # === AFFICHAGE ===
        st.markdown("### 📋 Tableau des Données Hebdomadaires")
        
        display_dataframe_formatted(df_hebdo_filtered, height=600)
        
        # === STATISTIQUES ===
        with st.expander("📊 Statistiques Descriptives"):
            colonnes_numeriques = df_hebdo_filtered.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if colonnes_numeriques:
                stats = df_hebdo_filtered[colonnes_numeriques].describe()
                st.dataframe(stats, use_container_width=True)
        
        # === EXPORT ===
        st.markdown("### 💾 Export des Données")
        export_buttons(df_hebdo_filtered, filename_prefix="donnees_hebdomadaires")
    
    # ========== CALENDRIER ÉPIDÉMIOLOGIQUE (VERSION CORRIGÉE) ==========
    else:
        
        section_header("Calendrier Épidémiologique 2025", icon="📅")
        
        st.info(
            "📌 Ce calendrier définit les semaines épidémiologiques utilisées pour l'analyse"
        )
        
        # Informations
        metrics = [
            {'label': 'Lignes', 'value': len(df_calendrier), 'icon': '📊'},
            {'label': 'Année', 'value': '2025', 'icon': '📅'},
            {'label': 'Première Date', 'value': df_calendrier['DATE'].min().strftime('%d/%m/%Y'), 'icon': '📅'},
            {'label': 'Dernière Date', 'value': df_calendrier['DATE'].max().strftime('%d/%m/%Y'), 'icon': '📅'}
        ]
        
        metric_row(metrics, columns=4)
        
        # === AFFICHAGE ===
        st.markdown("### 📋 Tableau du Calendrier")
        
        # Préparer le DataFrame pour affichage
        df_cal_display = df_calendrier.copy()
        
        # Formater la colonne DATE
        df_cal_display['DATE'] = df_cal_display['DATE'].dt.strftime('%d/%m/%Y')
        
        # Renommer les colonnes
        df_cal_display = df_cal_display.rename(columns={
            'Week_No': 'N° Semaine',
            'Semaine épidémiologique': 'Label Semaine',
            'Month': 'Mois',
            'DATE': 'Date'
        })
        
        display_dataframe_formatted(df_cal_display, height=600)
        
        # === RECHERCHE ===
        with st.expander("🔍 Rechercher une semaine spécifique"):
            semaines_uniques = sorted(df_calendrier['Semaine épidémiologique'].unique())
            
            semaine_recherche = st.selectbox(
                "Sélectionnez une semaine :",
                semaines_uniques
            )
            
            if semaine_recherche:
                # Filtrer les dates de cette semaine
                df_sem = df_calendrier[df_calendrier['Semaine épidémiologique'] == semaine_recherche]
                
                if len(df_sem) > 0:
                    date_debut = df_sem['DATE'].min()
                    date_fin = df_sem['DATE'].max()
                    nb_jours = len(df_sem)
                    
                    st.markdown(f"""
                    **Informations sur {semaine_recherche} :**
                    - **Numéro :** {df_sem.iloc[0]['Week_No']}
                    - **Mois :** {df_sem.iloc[0]['Month']}
                    - **Du :** {date_debut.strftime('%d/%m/%Y')}
                    - **Au :** {date_fin.strftime('%d/%m/%Y')}
                    - **Nombre de jours :** {nb_jours}
                    """)
        
        # === EXPORT ===
        st.markdown("### 💾 Export du Calendrier")
        export_buttons(df_cal_display, filename_prefix="calendrier_epidemiologique_2025")

# ==============================================================================
# TAB 2 : UPLOAD ET MISE À JOUR
# ==============================================================================

with tab_gestion:
    
    section_header("Upload et Mise à Jour des Fichiers Excel", icon="📤")
    
    st.info("""
    **📋 Instructions pour la mise à jour des données :**

    1. **Format requis** : Fichiers Excel (.xlsx uniquement)
    2. **Structure** : Les colonnes doivent correspondre exactement au format actuel
    3. **Sauvegarde** : Une copie de sauvegarde est automatiquement créée avant toute mise à jour
    4. **Validation** : Les données sont vérifiées avant d'être enregistrées

    **⚠️ ATTENTION :** 
    - Ne modifiez pas les noms des colonnes
    - Assurez-vous que les dates sont au format correct
    - Les semaines épidémiologiques doivent être au format S5_2025
    """)
    
    # ==============================================================================
    # FICHIERS ACTUELS
    # ==============================================================================
    
    st.markdown("### 📂 Fichiers Actuels")
    
    fichiers_detectes = detecter_fichiers_data()
    
    col1, col2 = st.columns(2)
    
    # Fichier Appels
    with col1:
        st.markdown("#### 📄 Fichier Appels")
        
        fichier_appels = fichiers_detectes['appels']
        
        if fichier_appels and os.path.exists(fichier_appels):
            stats = os.stat(fichier_appels)
            taille = stats.st_size / 1024
            modif = datetime.fromtimestamp(stats.st_mtime)
            
            st.success(f"✅ Fichier détecté")
            st.info(f"📂 `{os.path.basename(fichier_appels)}`")
            st.write(f"📏 Taille : {taille:.1f} Ko")
            st.write(f"🕐 Modifié : {modif.strftime('%d/%m/%Y %H:%M')}")
            
            with open(fichier_appels, "rb") as f:
                st.download_button(
                    "📥 Télécharger",
                    f,
                    file_name=os.path.basename(fichier_appels),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        else:
            st.error("❌ Fichier non détecté")
    
    # Fichier Calendrier
    with col2:
        st.markdown("#### 📄 Calendrier Épidémiologique")
        
        fichier_calendrier = fichiers_detectes['calendrier']
        
        if fichier_calendrier and os.path.exists(fichier_calendrier):
            stats = os.stat(fichier_calendrier)
            taille = stats.st_size / 1024
            modif = datetime.fromtimestamp(stats.st_mtime)
            
            st.success(f"✅ Fichier détecté")
            st.info(f"📂 `{os.path.basename(fichier_calendrier)}`")
            st.write(f"📏 Taille : {taille:.1f} Ko")
            st.write(f"🕐 Modifié : {modif.strftime('%d/%m/%Y %H:%M')}")
            
            with open(fichier_calendrier, "rb") as f:
                st.download_button(
                    "📥 Télécharger",
                    f,
                    file_name=os.path.basename(fichier_calendrier),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        else:
            st.error("❌ Fichier non détecté")
    
    # ==============================================================================
    # UPLOAD DE NOUVEAUX FICHIERS
    # ==============================================================================
    
    st.markdown("---")
    st.markdown("### 📤 Upload de Nouveaux Fichiers")
    
    upload_tab1, upload_tab2 = st.tabs(["📊 Appels Journaliers", "📅 Calendrier"])
    
    # ===== UPLOAD APPELS JOURNALIERS =====
    with upload_tab1:
        st.markdown("#### 📊 Mettre à jour le fichier des appels")
        
        fichiers_detectes_upload = detecter_fichiers_data()
        fichier_actuel_appels = fichiers_detectes_upload['appels']
        
        if fichier_actuel_appels:
            st.info(f"📂 **Fichier actuel :** `{os.path.basename(fichier_actuel_appels)}`")
        
        uploaded_appels = st.file_uploader(
            "Sélectionnez le nouveau fichier Excel",
            type=['xlsx'],
            key='up_appels',
            help="Format requis : .xlsx avec les colonnes DATE, URGENCE_MEDICALE_JOUR, CSU_JOUR, etc."
        )
        
        if uploaded_appels:
            try:
                df_new = pd.read_excel(uploaded_appels)
                st.success(f"✅ Fichier chargé : {uploaded_appels.name}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Lignes", len(df_new))
                with col2:
                    st.metric("Colonnes", len(df_new.columns))
                
                # Validation
                colonnes_req = ['DATE'] + settings.CATEGORIES_APPELS
                colonnes_manq = [c for c in colonnes_req if c not in df_new.columns]
                
                if colonnes_manq:
                    st.error(f"❌ Colonnes manquantes : {', '.join(colonnes_manq)}")
                else:
                    st.success("✅ Structure du fichier validée !")
                    
                    with st.expander("👁️ Prévisualiser (10 premières lignes)"):
                        st.dataframe(df_new.head(10), use_container_width=True)
                    
                    st.markdown("---")
                    
                    if st.button("✅ CONFIRMER LA MISE À JOUR", type="primary", use_container_width=True, key="conf_app"):
                        # Créer le dossier de backup
                        backup_dir = settings.DATA_DIR / "backups"
                        backup_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Sauvegarder l'ancien fichier
                        if fichier_actuel_appels and os.path.exists(fichier_actuel_appels):
                            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                            nom_backup = f"{Path(fichier_actuel_appels).stem}_backup_{ts}.xlsx"
                            backup_path = backup_dir / nom_backup
                            shutil.copy2(fichier_actuel_appels, backup_path)
                            st.info(f"💾 Sauvegarde créée : `{nom_backup}`")
                            
                            # Supprimer l'ancien fichier
                            os.remove(fichier_actuel_appels)
                        
                        # Sauvegarder le nouveau fichier
                        nouveau_chemin = fichier_actuel_appels if fichier_actuel_appels else str(settings.DATA_DIR / uploaded_appels.name)
                        
                        with open(nouveau_chemin, "wb") as f:
                            f.write(uploaded_appels.getbuffer())
                        
                        st.success(f"🎉 Fichier mis à jour : `{os.path.basename(nouveau_chemin)}`")
                        st.balloons()
                        
                        log_upload_fichier(uploaded_appels.name, len(uploaded_appels.getvalue()), success=True)
                        
                        # Effacer le cache
                        st.cache_data.clear()
                        
                        st.info("💡 Rafraîchissez la page (F5) pour voir les changements.")
            
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
                log_upload_fichier(uploaded_appels.name, success=False, message=str(e))
    
    # ===== UPLOAD CALENDRIER =====
    with upload_tab2:
        st.markdown("#### 📅 Mettre à jour le calendrier épidémiologique")
        
        fichiers_detectes_upload = detecter_fichiers_data()
        fichier_actuel_cal = fichiers_detectes_upload['calendrier']
        
        if fichier_actuel_cal:
            st.info(f"📂 **Fichier actuel :** `{os.path.basename(fichier_actuel_cal)}`")
        
        uploaded_cal = st.file_uploader(
            "Sélectionnez le nouveau fichier Excel",
            type=['xlsx'],
            key='up_cal',
            help="Format requis : .xlsx avec les colonnes DATE et Semaine épidémiologique"
        )
        
        if uploaded_cal:
            try:
                df_new_cal = pd.read_excel(uploaded_cal)
                st.success(f"✅ Fichier chargé : {uploaded_cal.name}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Lignes", len(df_new_cal))
                with col2:
                    st.metric("Colonnes", len(df_new_cal.columns))
                
                # Validation
                colonnes_req_cal = ['DATE', 'Semaine épidémiologique']
                colonnes_manq_cal = [c for c in colonnes_req_cal if c not in df_new_cal.columns]
                
                if colonnes_manq_cal:
                    st.error(f"❌ Colonnes manquantes : {', '.join(colonnes_manq_cal)}")
                else:
                    st.success("✅ Structure du fichier validée !")
                    
                    with st.expander("👁️ Prévisualiser (10 premières lignes)"):
                        st.dataframe(df_new_cal.head(10), use_container_width=True)
                    
                    st.markdown("---")
                    
                    if st.button("✅ CONFIRMER LA MISE À JOUR", type="primary", use_container_width=True, key="conf_cal"):
                        # Créer le dossier de backup
                        backup_dir = settings.DATA_DIR / "backups"
                        backup_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Sauvegarder l'ancien fichier
                        if fichier_actuel_cal and os.path.exists(fichier_actuel_cal):
                            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                            nom_backup = f"{Path(fichier_actuel_cal).stem}_backup_{ts}.xlsx"
                            backup_path = backup_dir / nom_backup
                            shutil.copy2(fichier_actuel_cal, backup_path)
                            st.info(f"💾 Sauvegarde créée : `{nom_backup}`")
                            
                            # Supprimer l'ancien fichier
                            os.remove(fichier_actuel_cal)
                        
                        # Sauvegarder le nouveau fichier
                        nouveau_chemin = fichier_actuel_cal if fichier_actuel_cal else str(settings.DATA_DIR / uploaded_cal.name)
                        
                        with open(nouveau_chemin, "wb") as f:
                            f.write(uploaded_cal.getbuffer())
                        
                        st.success(f"🎉 Fichier mis à jour : `{os.path.basename(nouveau_chemin)}`")
                        st.balloons()
                        
                        log_upload_fichier(uploaded_cal.name, len(uploaded_cal.getvalue()), success=True)
                        
                        # Effacer le cache
                        st.cache_data.clear()
                        
                        st.info("💡 Rafraîchissez la page (F5) pour voir les changements.")
            
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
                log_upload_fichier(uploaded_cal.name, success=False, message=str(e))
    
    # ==============================================================================
    # HISTORIQUE DES SAUVEGARDES
    # ==============================================================================
    
    st.markdown("---")
    st.markdown("### 📚 Historique des Sauvegardes")
    
    backup_dir = settings.DATA_DIR / "backups"
    
    if backup_dir.exists():
        backups = sorted(backup_dir.glob("*_backup_*.xlsx"), key=os.path.getmtime, reverse=True)
        
        if backups:
            st.success(f"✅ {len(backups)} sauvegarde(s) disponible(s)")
            
            for backup in backups[:10]:  # Afficher les 10 dernières
                stats = os.stat(backup)
                taille = stats.st_size / 1024
                modif = datetime.fromtimestamp(stats.st_mtime)
                
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"📄 {backup.name}")
                with col2:
                    st.write(f"📏 {taille:.1f} Ko")
                with col3:
                    st.write(f"🕐 {modif.strftime('%d/%m/%Y %H:%M')}")
                with col4:
                    with open(backup, "rb") as f:
                        st.download_button(
                            label="📥",
                            data=f,
                            file_name=backup.name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_backup_{backup.name}"
                        )
        else:
            st.info("ℹ️ Aucune sauvegarde disponible")
    else:
        st.info("ℹ️ Le dossier de sauvegarde n'existe pas encore")

# ==============================================================================
# FIN DE LA PAGE
# ==============================================================================