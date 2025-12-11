"""
==============================================================================
MODULE DES COMPOSANTS MÉTRIQUES ET KPIs
==============================================================================
Ce module fournit des composants pour afficher des métriques, KPIs et
statistiques de manière élégante et cohérente.

Composants disponibles :
- metric_card_html() : Carte métrique stylisée avec HTML/CSS
- metric_row() : Affiche plusieurs métriques en ligne
- kpi_card() : Carte KPI sophistiquée pour dashboards
- comparison_metric() : Métrique de comparaison avec variation

Tous les composants utilisent :
- Les couleurs officielles du Cameroun
- Le CSS centralisé
- Un design moderne et professionnel

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
from utils.helpers import formater_nombre

# ==============================================================================
# FONCTION 1 : CARTE MÉTRIQUE HTML STYLISÉE
# ==============================================================================

def metric_card_html(
    label,
    value,
    delta=None,
    delta_color="auto",
    icon="📊",
    color="primary",
    show_trend_arrow=True
):
    """
    Affiche une carte métrique stylisée en HTML avec gradient.
    
    Cette fonction remplace les cartes métriques HTML répétées dans
    toutes les pages. Elle utilise la classe CSS .metric-card.
    
    Args:
        label (str): Label de la métrique (ex: "Total Appels")
        value (str ou int): Valeur à afficher (ex: 15234 ou "15 234")
        delta (float ou str, optional): Variation (ex: +15.3 ou "-5%")
        delta_color (str): Couleur du delta ('auto', 'green', 'red', 'gray')
        icon (str): Emoji ou icône
        color (str): Couleur de la carte ('primary', 'success', 'info', 'warning', 'danger')
        show_trend_arrow (bool): Afficher flèche de tendance si delta
    
    Returns:
        None (affiche directement avec st.markdown)
    
    Example:
        >>> metric_card_html(
        ...     "Total Appels",
        ...     "15 234",
        ...     delta="+12.5%",
        ...     icon="📞"
        ... )
    
    Note:
        Cette fonction est plus flexible que st.metric() natif et
        permet un contrôle total du style via CSS.
    """
    # Formater la valeur si c'est un nombre
    if isinstance(value, (int, float)):
        value_formatted = formater_nombre(value)
    else:
        value_formatted = str(value)
    
    # Déterminer la classe CSS de la carte
    css_class = f"metric-card {color}"
    
    # Construire le HTML de base
    html = f'''
    <div class="{css_class}">
        <div class="icon">{icon}</div>
        <h3>{label}</h3>
        <div class="value">{value_formatted}</div>
    '''
    
    # Ajouter le delta si présent
    if delta is not None:
        # Convertir en string
        delta_str = str(delta)
        
        # Déterminer la couleur du delta
        if delta_color == "auto":
            # Auto : vert si positif, rouge si négatif
            try:
                delta_num = float(delta_str.replace('%', '').replace('+', '').replace(' ', ''))
                if delta_num > 0:
                    delta_color_final = "#28a745"
                    arrow = "▲" if show_trend_arrow else ""
                elif delta_num < 0:
                    delta_color_final = "#dc3545"
                    arrow = "▼" if show_trend_arrow else ""
                else:
                    delta_color_final = "#6c757d"
                    arrow = "➡" if show_trend_arrow else ""
            except:
                delta_color_final = "#6c757d"
                arrow = ""
        elif delta_color == "green":
            delta_color_final = "#28a745"
            arrow = "▲" if show_trend_arrow else ""
        elif delta_color == "red":
            delta_color_final = "#dc3545"
            arrow = "▼" if show_trend_arrow else ""
        else:
            delta_color_final = "#6c757d"
            arrow = ""
        
        html += f'''
        <div class="delta" style="color: {delta_color_final};">
            {arrow} {delta_str}
        </div>
        '''
    
    html += '</div>'
    
    # Afficher avec Streamlit
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 2 : LIGNE DE MÉTRIQUES
# ==============================================================================

def metric_row(metrics_list, columns=None):
    """
    Affiche plusieurs métriques en ligne avec distribution automatique.
    
    Cette fonction simplifie l'affichage de plusieurs métriques côte à côte
    en gérant automatiquement les colonnes Streamlit.
    
    Args:
        metrics_list (list): Liste de dictionnaires de métriques
            Format: [
                {
                    'label': 'Total Appels',
                    'value': 15234,
                    'delta': '+12.5%',
                    'icon': '📞',
                    'color': 'primary'
                },
                ...
            ]
        columns (int, optional): Nombre de colonnes. Si None, auto = len(metrics_list)
    
    Example:
        >>> metrics = [
        ...     {'label': 'Total', 'value': 15234, 'icon': '📞'},
        ...     {'label': 'Moyenne', 'value': 523, 'icon': '📊'},
        ...     {'label': 'Maximum', 'value': 892, 'icon': '📈'}
        ... ]
        >>> metric_row(metrics)
    
    Note:
        Remplace le pattern répété de col1, col2, col3 = st.columns(3)
    """
    if not metrics_list:
        st.warning("⚠️ Aucune métrique à afficher")
        return
    
    # Déterminer le nombre de colonnes
    if columns is None:
        columns = len(metrics_list)
    
    # Créer les colonnes
    cols = st.columns(columns)
    
    # Afficher chaque métrique
    for i, metric_data in enumerate(metrics_list):
        col_index = i % columns
        
        with cols[col_index]:
            # Utiliser metric_card_html ou st.metric selon la présence de 'color'
            if 'color' in metric_data or 'html' in metric_data:
                # Version HTML stylisée
                metric_card_html(
                    label=metric_data.get('label', 'Métrique'),
                    value=metric_data.get('value', 0),
                    delta=metric_data.get('delta'),
                    delta_color=metric_data.get('delta_color', 'auto'),
                    icon=metric_data.get('icon', '📊'),
                    color=metric_data.get('color', 'primary'),
                    show_trend_arrow=metric_data.get('show_trend_arrow', True)
                )
            else:
                # Version native Streamlit (plus simple)
                st.metric(
                    label=metric_data.get('label', 'Métrique'),
                    value=metric_data.get('value', 0),
                    delta=metric_data.get('delta'),
                    delta_color=metric_data.get('delta_color', 'normal')
                )

# ==============================================================================
# FONCTION 3 : CARTE KPI SOPHISTIQUÉE
# ==============================================================================

def kpi_card(
    title,
    value,
    subtitle=None,
    trend=None,
    sparkline_data=None,
    icon="📊",
    color=None,
    target=None,
    height=200
):
    """
    Affiche une carte KPI sophistiquée pour dashboards professionnels.
    
    Args:
        title (str): Titre du KPI
        value (str ou int): Valeur principale
        subtitle (str, optional): Sous-titre ou description
        trend (dict, optional): {'value': '+15%', 'label': 'vs mois dernier'}
        sparkline_data (list, optional): Données pour mini graphique [10, 12, 15, 13, 18]
        icon (str): Emoji ou icône
        color (str, optional): Couleur (hex). Si None, utilise vert Cameroun
        target (dict, optional): {'value': 20000, 'label': 'Objectif'}
        height (int): Hauteur de la carte en pixels
    
    Example:
        >>> kpi_card(
        ...     title="Appels du Mois",
        ...     value="15,234",
        ...     subtitle="Novembre 2025",
        ...     trend={'value': '+12.5%', 'label': 'vs Octobre'},
        ...     sparkline_data=[450, 520, 480, 510, 523],
        ...     icon="📞",
        ...     target={'value': 20000, 'label': 'Objectif mensuel'}
        ... )
    """
    if color is None:
        color = settings.COULEURS_CAMEROUN['vert']
    
    # Formater la valeur
    if isinstance(value, (int, float)):
        value_formatted = formater_nombre(value)
    else:
        value_formatted = str(value)
    
    # Construire le HTML
    html = f'''
    <div style="
        background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        height: {height}px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.3s ease;
    " onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
        
        <!-- Header -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="font-size: 0.9em; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">
                    {title}
                </div>
                {f'<div style="font-size: 0.8em; opacity: 0.8; margin-top: 5px;">{subtitle}</div>' if subtitle else ''}
            </div>
            <div style="font-size: 2em;">{icon}</div>
        </div>
        
        <!-- Valeur principale -->
        <div style="font-size: 2.5em; font-weight: bold; margin: 15px 0;">
            {value_formatted}
        </div>
        
        <!-- Footer avec trend et target -->
        <div style="display: flex; justify-content: space-between; align-items: center;">
    '''
    
    # Trend
    if trend:
        html += f'''
            <div style="font-size: 0.9em;">
                <span style="font-weight: bold;">{trend.get('value', '')}</span>
                <span style="opacity: 0.8; margin-left: 5px;">{trend.get('label', '')}</span>
            </div>
        '''
    
    # Target
    if target:
        progress = 0
        try:
            value_num = float(str(value).replace(',', '').replace(' ', ''))
            target_num = float(target.get('value', 0))
            if target_num > 0:
                progress = min(100, (value_num / target_num) * 100)
        except:
            pass
        
        html += f'''
            <div style="font-size: 0.8em; opacity: 0.9;">
                {target.get('label', 'Objectif')}: {int(progress)}%
            </div>
        '''
    
    html += '''
        </div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 4 : MÉTRIQUE DE COMPARAISON
# ==============================================================================

def comparison_metric(
    label,
    value1,
    value2,
    label1="Actuel",
    label2="Précédent",
    icon="📊",
    show_percentage=True
):
    """
    Affiche une métrique de comparaison entre deux valeurs.
    
    Args:
        label (str): Label de la métrique
        value1 (int ou float): Valeur actuelle
        value2 (int ou float): Valeur de comparaison
        label1 (str): Label de la valeur 1
        label2 (str): Label de la valeur 2
        icon (str): Emoji ou icône
        show_percentage (bool): Afficher le pourcentage de variation
    
    Example:
        >>> comparison_metric(
        ...     "Appels Hebdomadaires",
        ...     value1=1250,
        ...     value2=1080,
        ...     label1="S10_2025",
        ...     label2="S9_2025"
        ... )
    """
    # Calculer la variation
    try:
        variation_abs = value1 - value2
        variation_pct = (variation_abs / value2 * 100) if value2 != 0 else 0
        
        # Déterminer la couleur
        if variation_abs > 0:
            color = "#28a745"
            arrow = "▲"
        elif variation_abs < 0:
            color = "#dc3545"
            arrow = "▼"
        else:
            color = "#6c757d"
            arrow = "➡"
    except:
        variation_abs = 0
        variation_pct = 0
        color = "#6c757d"
        arrow = ""
    
    # Formater les valeurs
    value1_str = formater_nombre(value1)
    value2_str = formater_nombre(value2)
    
    # Construire le HTML
    html = f'''
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 5px solid {settings.COULEURS_CAMEROUN['vert']};
    ">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 1.5em; margin-right: 10px;">{icon}</span>
            <span style="font-size: 1.1em; font-weight: 600; color: {settings.COULEURS_CAMEROUN['vert']};">
                {label}
            </span>
        </div>
        
        <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
            <!-- Valeur 1 -->
            <div style="text-align: center;">
                <div style="font-size: 0.85em; color: #6c757d; margin-bottom: 5px;">
                    {label1}
                </div>
                <div style="font-size: 2em; font-weight: bold; color: {settings.COULEURS_CAMEROUN['vert']};">
                    {value1_str}
                </div>
            </div>
            
            <!-- Séparateur -->
            <div style="width: 2px; background-color: #e9ecef; margin: 0 20px;"></div>
            
            <!-- Valeur 2 -->
            <div style="text-align: center;">
                <div style="font-size: 0.85em; color: #6c757d; margin-bottom: 5px;">
                    {label2}
                </div>
                <div style="font-size: 2em; font-weight: bold; color: #6c757d;">
                    {value2_str}
                </div>
            </div>
        </div>
        
        <!-- Variation -->
        <div style="
            text-align: center;
            padding: 10px;
            background-color: {color}15;
            border-radius: 5px;
            color: {color};
            font-weight: 600;
        ">
            {arrow} {variation_abs:+,} {f'({variation_pct:+.1f}%)' if show_percentage else ''}
        </div>
    </div>
    '''.replace(',', ' ')
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION BONUS 1 : GAUGE (JAUGE)
# ==============================================================================

def gauge_metric(
    label,
    value,
    min_value=0,
    max_value=100,
    target=None,
    unit="",
    color=None
):
    """
    Affiche une métrique sous forme de jauge (gauge).
    
    Args:
        label (str): Label de la métrique
        value (float): Valeur actuelle
        min_value (float): Valeur minimale
        max_value (float): Valeur maximale
        target (float, optional): Valeur cible à marquer
        unit (str): Unité de mesure
        color (str, optional): Couleur de la jauge
    
    Example:
        >>> gauge_metric(
        ...     "Taux d'atteinte objectif",
        ...     value=75,
        ...     target=80,
        ...     unit="%"
        ... )
    """
    if color is None:
        color = settings.COULEURS_CAMEROUN['vert']
    
    # Calculer le pourcentage
    try:
        percentage = ((value - min_value) / (max_value - min_value)) * 100
        percentage = max(0, min(100, percentage))
    except:
        percentage = 0
    
    html = f'''
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    ">
        <div style="font-weight: 600; color: {color}; margin-bottom: 15px; font-size: 1.1em;">
            {label}
        </div>
        
        <!-- Gauge circulaire (simplifié) -->
        <div style="position: relative; width: 150px; height: 150px; margin: 0 auto;">
            <svg width="150" height="150" viewBox="0 0 150 150">
                <!-- Background circle -->
                <circle cx="75" cy="75" r="60" fill="none" stroke="#e9ecef" stroke-width="15"/>
                <!-- Progress circle -->
                <circle cx="75" cy="75" r="60" fill="none" stroke="{color}" stroke-width="15"
                        stroke-dasharray="{percentage * 3.77} 377"
                        stroke-linecap="round"
                        transform="rotate(-90 75 75)"/>
            </svg>
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 2em;
                font-weight: bold;
                color: {color};
            ">
                {value}{unit}
            </div>
        </div>
        
        <div style="margin-top: 15px; font-size: 0.9em; color: #6c757d;">
            Min: {min_value}{unit} | Max: {max_value}{unit}
            {f' | Cible: {target}{unit}' if target else ''}
        </div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION BONUS 2 : STAT CARD COMPACTE
# ==============================================================================

def stat_card_compact(stats_dict, title=None):
    """
    Affiche plusieurs statistiques dans une carte compacte.
    
    Args:
        stats_dict (dict): Dictionnaire {label: valeur}
        title (str, optional): Titre de la carte
    
    Example:
        >>> stats = {
        ...     'Total': '15,234',
        ...     'Moyenne': '523',
        ...     'Maximum': '892',
        ...     'Minimum': '287'
        ... }
        >>> stat_card_compact(stats, title="Statistiques Hebdomadaires")
    """
    html = f'''
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-top: 4px solid {settings.COULEURS_CAMEROUN['vert']};
    ">
    '''
    
    if title:
        html += f'''
        <div style="
            font-size: 1.1em;
            font-weight: 600;
            color: {settings.COULEURS_CAMEROUN['vert']};
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        ">
            {title}
        </div>
        '''
    
    # Grille de statistiques
    html += '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">'
    
    for label, value in stats_dict.items():
        html += f'''
        <div style="text-align: center;">
            <div style="font-size: 0.85em; color: #6c757d; margin-bottom: 5px;">
                {label}
            </div>
            <div style="font-size: 1.5em; font-weight: bold; color: {settings.COULEURS_CAMEROUN['vert']};">
                {value}
            </div>
        </div>
        '''
    
    html += '</div></div>'
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION BONUS 3 : TREND INDICATOR
# ==============================================================================

def trend_indicator(value, threshold_up=5, threshold_down=-5):
    """
    Retourne un indicateur de tendance HTML.
    
    Args:
        value (float): Valeur de variation (%)
        threshold_up (float): Seuil pour tendance haussière forte
        threshold_down (float): Seuil pour tendance baissière forte
    
    Returns:
        str: HTML de l'indicateur
    
    Example:
        >>> trend = trend_indicator(12.5)
        >>> st.markdown(f"Tendance : {trend}", unsafe_allow_html=True)
    """
    if value >= threshold_up:
        return '<span style="color: #28a745; font-weight: bold;">📈 Forte hausse</span>'
    elif value > 0:
        return '<span style="color: #28a745;">↗️ Hausse</span>'
    elif value <= threshold_down:
        return '<span style="color: #dc3545; font-weight: bold;">📉 Forte baisse</span>'
    elif value < 0:
        return '<span style="color: #dc3545;">↘️ Baisse</span>'
    else:
        return '<span style="color: #6c757d;">➡️ Stable</span>'

# ==============================================================================
# FIN DU MODULE
# ==============================================================================