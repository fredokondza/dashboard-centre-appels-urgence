"""
==============================================================================
MODULE DES COMPOSANTS DE MISE EN PAGE
==============================================================================
Ce module fournit des composants de mise en page réutilisables pour
l'ensemble de l'application Streamlit.

Composants disponibles :
- apply_custom_css() : Charge le CSS centralisé
- page_header() : Header de page avec bannière Cameroun
- section_header() : Header de section avec bordure jaune
- page_footer() : Footer standard MINSANTE
- info_box() : Boîtes d'information stylisées
- modele_selection_card() : Cartes pour sélection de modèles

Tous les composants utilisent :
- Les couleurs officielles du Cameroun
- Le CSS centralisé (config/styles.css)
- Un design cohérent et professionnel

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

import streamlit as st
from pathlib import Path
import sys

# Import de la configuration
sys.path.append(str(Path(__file__).parent.parent))

from config import settings

# ==============================================================================
# FONCTION 1 : CHARGER LE CSS CENTRALISÉ
# ==============================================================================

def apply_custom_css():
    """
    Charge le fichier CSS centralisé dans la page Streamlit.
    
    Cette fonction doit être appelée au début de chaque page pour :
    - Charger config/styles.css
    - Appliquer les styles cohérents
    - Éliminer le CSS embarqué répété
    
    Returns:
        bool: True si le CSS a été chargé avec succès
    
    Example:
        >>> # Au début de chaque page
        >>> from components.layout import apply_custom_css
        >>> apply_custom_css()
    
    Note:
        Cette fonction remplace les ~150 lignes de CSS répétées
        dans chaque fichier Python.
    """
    try:
        # Chemin vers le fichier CSS
        css_file = settings.BASE_DIR / 'config' / 'styles.css'
        
        if css_file.exists():
            # Lire le contenu du CSS
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Injecter dans Streamlit
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
            
            return True
        else:
            st.warning(f"⚠️ Fichier CSS introuvable : {css_file}")
            return False
            
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du CSS : {str(e)}")
        return False

# ==============================================================================
# FONCTION 2 : HEADER DE PAGE PRINCIPAL
# ==============================================================================

def page_header(title, subtitle=None, icon=None, show_flag=True):
    """
    Affiche le header principal d'une page avec bannière gradient.
    
    Args:
        title (str): Titre principal de la page
        subtitle (str, optional): Sous-titre descriptif
        icon (str, optional): Emoji ou icône à afficher avant le titre
        show_flag (bool): Afficher le drapeau du Cameroun
    
    Example:
        >>> page_header(
        ...     "Dashboard Centre d'Appels",
        ...     subtitle="Vue d'ensemble des données",
        ...     icon="🏥"
        ... )
    
    Note:
        Utilise la classe CSS .main-title du fichier styles.css
    """
    # Construire le titre complet
    titre_complet = ""
    
    if show_flag:
        titre_complet += settings.DRAPEAU_CAMEROUN + " "
    
    if icon:
        titre_complet += icon + " "
    
    titre_complet += title.upper()
    
    # Construire le HTML
    html = f'<div class="main-title"><h1>{titre_complet}</h1>'
    
    if subtitle:
        html += f'<p style="font-size: 1.1em; margin-top: 10px;">{subtitle}</p>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 3 : HEADER DE SECTION
# ==============================================================================

def section_header(title, subtitle=None, icon=None, level=2):
    """
    Affiche un header de section avec bordure jaune.
    
    Args:
        title (str): Titre de la section
        subtitle (str, optional): Sous-titre ou description
        icon (str, optional): Emoji ou icône
        level (int): Niveau de titre (2 ou 3)
    
    Example:
        >>> section_header("Configuration du Rapport", icon="⚙️")
        >>> section_header("Statistiques", subtitle="Période 2025", level=3)
    
    Note:
        Utilise la classe CSS .section-header du fichier styles.css
    """
    # Construire le titre
    titre_complet = ""
    if icon:
        titre_complet += icon + " "
    titre_complet += title
    
    # Balise de titre selon le niveau
    if level == 2:
        titre_html = f'<h2>{titre_complet}</h2>'
    else:
        titre_html = f'<h3>{titre_complet}</h3>'
    
    # Construire le HTML
    html = f'<div class="section-header">{titre_html}'
    
    if subtitle:
        html += f'<p>{subtitle}</p>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 4 : FOOTER DE PAGE
# ==============================================================================

def page_footer(show_credits=True, show_version=True, custom_text=None):
    """
    Affiche le footer standard MINSANTE en bas de page.
    
    Args:
        show_credits (bool): Afficher les crédits de développement
        show_version (bool): Afficher la version de l'application
        custom_text (str, optional): Texte personnalisé supplémentaire
    
    Example:
        >>> # À la fin de chaque page
        >>> page_footer()
        >>> # Ou avec personnalisation
        >>> page_footer(custom_text="Version Bêta - Tests en cours")
    
    Note:
        Utilise la classe CSS .footer du fichier styles.css
    """
    html = '<div class="footer">'
    
    # Ligne 1 : Titre
    html += f'<p><strong>{settings.TEMPLATES["footer"]}</strong></p>'
    
    # Ligne 2 : Copyright
    html += f'<p>{settings.TEMPLATES["copyright"]}'
    
    if show_credits:
        html += f' | {settings.TEMPLATES["credits"]}'
    
    html += '</p>'
    
    # Ligne 3 : Version et texte personnalisé
    if show_version or custom_text:
        html += '<p style="font-size: 0.9em; margin-top: 10px;">'
        
        if show_version:
            html += f'Version {settings.APP_CONFIG["version"]}'
        
        if custom_text:
            if show_version:
                html += ' | '
            html += custom_text
        
        html += '</p>'
    
    html += '</div>'
    
    # Ajouter une ligne de séparation avant le footer
    st.markdown("---")
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 5 : BOÎTE D'INFORMATION
# ==============================================================================

def info_box(message, box_type="info", icon=None, title=None):
    """
    Affiche une boîte d'information stylisée.
    
    Args:
        message (str): Message à afficher (peut contenir du HTML)
        box_type (str): Type de boîte ('info', 'success', 'warning', 'danger')
        icon (str, optional): Emoji ou icône à afficher
        title (str, optional): Titre de la boîte
    
    Example:
        >>> info_box(
        ...     "Les données datent de plus de 7 jours",
        ...     box_type="warning",
        ...     icon="⚠️",
        ...     title="Attention"
        ... )
    
    Note:
        Utilise les classes CSS .info-box du fichier styles.css
    """
    # Déterminer l'icône par défaut selon le type
    if icon is None:
        icons_default = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'danger': '❌'
        }
        icon = icons_default.get(box_type, 'ℹ️')
    
    # Classe CSS selon le type
    css_class = f'info-box {box_type}'
    
    # Construire le HTML
    html = f'<div class="{css_class}">'
    
    if title:
        html += f'<p style="font-weight: bold; margin-bottom: 10px;">{icon} {title}</p>'
    
    html += f'<p>{icon if not title else ""} {message}</p>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 6 : CARTE DE SÉLECTION DE MODÈLE (POUR PAGE GÉNÉRATION RAPPORTS)
# ==============================================================================

def modele_selection_card(
    title,
    description,
    features_list,
    selected=False,
    emoji="📄"
):
    """
    Affiche une carte pour sélectionner un modèle de rapport.
    
    Args:
        title (str): Titre du modèle
        description (str): Description courte
        features_list (list): Liste des fonctionnalités (str)
        selected (bool): Si True, applique le style "sélectionné"
        emoji (str): Emoji du modèle
    
    Returns:
        str: HTML de la carte
    
    Example:
        >>> html = modele_selection_card(
        ...     "Modèle Original",
        ...     "7 slides - Format standard",
        ...     ["Page de titre", "Faits saillants", "Comparaison"],
        ...     selected=True,
        ...     emoji="📄"
        ... )
        >>> st.markdown(html, unsafe_allow_html=True)
    
    Note:
        Utilise les classes CSS .modele-card du fichier styles.css
    """
    # Classe CSS selon sélection
    css_class = 'modele-card modele-selected' if selected else 'modele-card'
    
    # Construire le HTML
    html = f'<div class="{css_class}">'
    html += f'<h3 style="color: #007A33;">{emoji} {title}</h3>'
    html += f'<p><strong>{description}</strong></p>'
    
    # Liste des fonctionnalités
    if features_list:
        html += '<ul>'
        for feature in features_list:
            html += f'<li>{feature}</li>'
        html += '</ul>'
    
    html += '</div>'
    
    return html

# ==============================================================================
# FONCTION BONUS 1 : CARTE MÉTRIQUE SIMPLE HTML
# ==============================================================================

def metric_card_simple(label, value, icon="📊", color="primary"):
    """
    Affiche une carte métrique simple en HTML.
    
    Args:
        label (str): Label de la métrique
        value (str ou int): Valeur à afficher
        icon (str): Emoji ou icône
        color (str): Couleur ('primary', 'success', 'info', 'warning', 'danger')
    
    Example:
        >>> metric_card_simple("Total Appels", "15,234", icon="📞")
    
    Note:
        Pour une version plus avancée avec delta, voir components/metrics.py
    """
    html = f'''
    <div class="metric-card {color}">
        <div class="icon">{icon}</div>
        <h3>{label}</h3>
        <div class="value">{value}</div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION BONUS 2 : BANDEAU D'ALERTE
# ==============================================================================

def alert_banner(message, alert_type="info", dismissible=False):
    """
    Affiche un bandeau d'alerte en haut de section.
    
    Args:
        message (str): Message d'alerte
        alert_type (str): Type ('info', 'success', 'warning', 'danger')
        dismissible (bool): Si True, peut être fermé (non implémenté en HTML pur)
    
    Example:
        >>> alert_banner(
        ...     "Nouvelle version disponible !",
        ...     alert_type="success"
        ... )
    """
    # Utiliser les composants natifs de Streamlit pour les alertes
    if alert_type == "info":
        st.info(message)
    elif alert_type == "success":
        st.success(message)
    elif alert_type == "warning":
        st.warning(message)
    elif alert_type == "danger":
        st.error(message)

# ==============================================================================
# FONCTION BONUS 3 : DIVIDER PERSONNALISÉ
# ==============================================================================

def custom_divider(text=None, color=None):
    """
    Affiche un séparateur personnalisé avec texte optionnel.
    
    Args:
        text (str, optional): Texte à afficher au centre
        color (str, optional): Couleur du séparateur
    
    Example:
        >>> custom_divider()  # Simple ligne
        >>> custom_divider("Section suivante", color="#007A33")
    """
    if color is None:
        color = settings.COULEURS_CAMEROUN['jaune']
    
    if text:
        html = f'''
        <div style="display: flex; align-items: center; margin: 30px 0;">
            <div style="flex: 1; height: 2px; background-color: {color};"></div>
            <div style="padding: 0 20px; font-weight: bold; color: {color};">{text}</div>
            <div style="flex: 1; height: 2px; background-color: {color};"></div>
        </div>
        '''
    else:
        html = f'<div style="height: 2px; background-color: {color}; margin: 20px 0;"></div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION BONUS 4 : BREADCRUMB (FIL D'ARIANE)
# ==============================================================================

def breadcrumb(items):
    """
    Affiche un fil d'Ariane pour la navigation.
    
    Args:
        items (list): Liste des éléments du fil d'Ariane
            Format: [{"label": "Accueil", "url": "#"}, ...]
    
    Example:
        >>> breadcrumb([
        ...     {"label": "Accueil", "url": "#"},
        ...     {"label": "Analyses", "url": "#"},
        ...     {"label": "Comparaisons", "url": None}  # Dernier élément sans lien
        ... ])
    """
    html = '<nav style="margin: 10px 0; font-size: 0.9em;">'
    
    for i, item in enumerate(items):
        if i > 0:
            html += ' <span style="color: #6c757d;">›</span> '
        
        if item.get("url") and i < len(items) - 1:
            html += f'<a href="{item["url"]}" style="color: #007A33; text-decoration: none;">{item["label"]}</a>'
        else:
            # Dernier élément ou sans URL
            html += f'<span style="color: #6c757d;">{item["label"]}</span>'
    
    html += '</nav>'
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION BONUS 5 : BADGE
# ==============================================================================

def badge(text, badge_type="primary"):
    """
    Affiche un badge (étiquette) inline.
    
    Args:
        text (str): Texte du badge
        badge_type (str): Type de badge ('primary', 'success', 'warning', 'danger', 'info')
    
    Returns:
        str: HTML du badge
    
    Example:
        >>> html = badge("Nouveau", badge_type="success")
        >>> st.markdown(f"Fonctionnalité {html}", unsafe_allow_html=True)
    """
    # Couleurs selon le type
    colors = {
        'primary': '#007A33',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8'
    }
    
    bg_color = colors.get(badge_type, colors['primary'])
    text_color = 'white' if badge_type != 'warning' else '#343a40'
    
    html = f'''
    <span style="
        background-color: {bg_color};
        color: {text_color};
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 600;
        display: inline-block;
        margin: 0 5px;
    ">{text}</span>
    '''
    
    return html

# ==============================================================================
# FONCTION BONUS 6 : LOADING SPINNER PERSONNALISÉ
# ==============================================================================

def custom_spinner(text="Chargement en cours..."):
    """
    Affiche un spinner de chargement personnalisé.
    
    Args:
        text (str): Texte à afficher à côté du spinner
    
    Example:
        >>> # Utiliser avec context manager
        >>> with custom_spinner("Traitement des données..."):
        >>>     # Code long
        >>>     time.sleep(5)
    
    Note:
        En réalité, utiliser st.spinner() de Streamlit est plus simple.
        Cette fonction est un exemple de personnalisation possible.
    """
    # Utiliser directement le spinner de Streamlit
    return st.spinner(text)

# ==============================================================================
# FONCTION BONUS 7 : PROGRESS BAR PERSONNALISÉE
# ==============================================================================

def custom_progress_bar(progress, text=None, color=None):
    """
    Affiche une barre de progression personnalisée.
    
    Args:
        progress (float): Progression entre 0 et 1
        text (str, optional): Texte à afficher
        color (str, optional): Couleur de la barre
    
    Example:
        >>> custom_progress_bar(0.75, text="Téléchargement : 75%")
    """
    if color is None:
        color = settings.COULEURS_CAMEROUN['vert']
    
    progress_pct = int(progress * 100)
    
    html = f'''
    <div style="margin: 20px 0;">
        {f'<p style="margin-bottom: 5px; font-weight: 500;">{text}</p>' if text else ''}
        <div style="
            width: 100%;
            height: 25px;
            background-color: #e9ecef;
            border-radius: 5px;
            overflow: hidden;
        ">
            <div style="
                width: {progress_pct}%;
                height: 100%;
                background-color: {color};
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 0.85em;
                transition: width 0.3s ease;
            ">
                {progress_pct}%
            </div>
        </div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FIN DU MODULE
# ==============================================================================