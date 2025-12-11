"""
==============================================================================
MODULE DE CRÉATION DE GRAPHIQUES PLOTLY
==============================================================================
Ce module fournit des fonctions pour créer des graphiques Plotly standardisés
et cohérents avec la charte graphique MINSANTE.

Toutes les fonctions utilisent :
- Les couleurs officielles du Cameroun (config.settings)
- Le template Plotly standardisé
- Des tooltips améliorés
- Des annotations automatiques
- Un style professionnel

Fonctions disponibles :
- creer_graphique_barres() : Graphique en barres simple
- creer_graphique_camembert() : Graphique circulaire (pie/donut)
- creer_graphique_ligne() : Courbe d'évolution
- creer_graphique_barres_groupees() : Barres groupées (comparaison)
- creer_heatmap() : Carte de chaleur
- creer_graphique_evolution() : Évolution temporelle avancée
- creer_graphique_variation() : Barres de variation (+/-)
- creer_graphique_comparaison() : Comparaison multi-critères
- creer_graphique_distribution() : Distribution par catégories

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0 (Optimisée)
==============================================================================
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Import de la configuration
sys.path.append(str(Path(__file__).parent.parent))

from config import settings

# ==============================================================================
# FONCTION 1 : GRAPHIQUE EN BARRES SIMPLE
# ==============================================================================

def creer_graphique_barres(
    data,
    x_col=None,
    y_col=None,
    titre="Graphique en Barres",
    orientation='v',
    couleur=None,
    show_values=True,
    height=500
):
    """
    Crée un graphique en barres simple (vertical ou horizontal).
    
    Args:
        data (dict ou pd.DataFrame): Données du graphique
            - Si dict: {label: valeur}
            - Si DataFrame: spécifier x_col et y_col
        x_col (str, optional): Nom de la colonne X (si DataFrame)
        y_col (str, optional): Nom de la colonne Y (si DataFrame)
        titre (str): Titre du graphique
        orientation (str): 'v' (vertical) ou 'h' (horizontal)
        couleur (str, optional): Couleur des barres. Si None, utilise vert Cameroun
        show_values (bool): Afficher les valeurs sur les barres
        height (int): Hauteur du graphique en pixels
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    
    Example:
        >>> data = {'CSU': 1200, 'Urgence': 800, 'Info': 600}
        >>> fig = creer_graphique_barres(data, titre="Top 3 Catégories")
        >>> fig.show()
    """
    # Convertir dict en DataFrame si nécessaire
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=['Catégorie', 'Valeur'])
        x_col = 'Catégorie'
        y_col = 'Valeur'
    else:
        df = data.copy()
    
    # Couleur par défaut
    if couleur is None:
        couleur = settings.COULEURS_CAMEROUN['vert']
    
    # Créer le graphique
    if orientation == 'v':
        fig = go.Figure(data=[
            go.Bar(
                x=df[x_col],
                y=df[y_col],
                marker_color=couleur,
                text=df[y_col] if show_values else None,
                textposition='outside',
                texttemplate='%{text:,}'.replace(',', ' '),
                hovertemplate='<b>%{x}</b><br>Valeur: %{y:,}<extra></extra>'.replace(',', ' ')
            )
        ])
    else:  # horizontal
        fig = go.Figure(data=[
            go.Bar(
                x=df[y_col],
                y=df[x_col],
                marker_color=couleur,
                orientation='h',
                text=df[y_col] if show_values else None,
                textposition='outside',
                texttemplate='%{text:,}'.replace(',', ' '),
                hovertemplate='<b>%{y}</b><br>Valeur: %{x:,}<extra></extra>'.replace(',', ' ')
            )
        ])
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=x_col if orientation == 'v' else y_col,
        yaxis_title=y_col if orientation == 'v' else x_col,
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        showlegend=False,
        plot_bgcolor='white',
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size']
    )
    
    return fig

# ==============================================================================
# FONCTION 2 : GRAPHIQUE CAMEMBERT (PIE/DONUT)
# ==============================================================================

def creer_graphique_camembert(
    data,
    labels_col=None,
    values_col=None,
    titre="Répartition",
    type_graphique='pie',
    couleurs=None,
    show_percentages=True,
    hole=0
):
    """
    Crée un graphique circulaire (camembert ou donut).
    
    Args:
        data (dict ou pd.DataFrame): Données du graphique
        labels_col (str, optional): Colonne des labels (si DataFrame)
        values_col (str, optional): Colonne des valeurs (si DataFrame)
        titre (str): Titre du graphique
        type_graphique (str): 'pie' (camembert) ou 'donut' (anneau)
        couleurs (list, optional): Liste de couleurs. Si None, utilise palette Cameroun
        show_percentages (bool): Afficher les pourcentages
        hole (float): Taille du trou central (0 = pie, 0.4 = donut)
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    
    Example:
        >>> data = {'Renseignements': 3000, 'Assistances': 2000, 'Signaux': 500}
        >>> fig = creer_graphique_camembert(data, titre="Répartition par Thématique")
    """
    # Convertir dict en DataFrame si nécessaire
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=['Label', 'Valeur'])
        labels_col = 'Label'
        values_col = 'Valeur'
    else:
        df = data.copy()
    
    # Couleurs par défaut
    if couleurs is None:
        couleurs = settings.COULEURS_GRAPHIQUES
    
    # Type de graphique
    if type_graphique == 'donut' and hole == 0:
        hole = 0.4
    
    # Créer le graphique
    fig = go.Figure(data=[
        go.Pie(
            labels=df[labels_col],
            values=df[values_col],
            marker=dict(colors=couleurs),
            hole=hole,
            textposition='auto',
            texttemplate='%{label}<br>%{value:,}<br>(%{percent})'.replace(',', ' ') if show_percentages else '%{label}<br>%{value:,}'.replace(',', ' '),
            hovertemplate='<b>%{label}</b><br>Valeur: %{value:,}<br>Pourcentage: %{percent}<extra></extra>'.replace(',', ' ')
        )
    ])
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        height=500,
        template=settings.PLOTLY_TEMPLATE,
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size']
    )
    
    return fig

# ==============================================================================
# FONCTION 3 : GRAPHIQUE EN LIGNE (ÉVOLUTION)
# ==============================================================================

def creer_graphique_ligne(
    data,
    x_col,
    y_col,
    titre="Évolution",
    couleur=None,
    show_markers=True,
    fill_area=False,
    moyenne_line=False,
    height=500
):
    """
    Crée un graphique en ligne pour l'évolution temporelle.
    
    Args:
        data (pd.DataFrame): Données du graphique
        x_col (str): Colonne X (généralement dates ou semaines)
        y_col (str): Colonne Y (valeurs)
        titre (str): Titre du graphique
        couleur (str, optional): Couleur de la ligne
        show_markers (bool): Afficher les points
        fill_area (bool): Remplir l'aire sous la courbe
        moyenne_line (bool): Ajouter une ligne de moyenne
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    
    Example:
        >>> fig = creer_graphique_ligne(df, 'Semaine', 'Total', titre="Évolution des appels")
    """
    df = data.copy()
    
    # Couleur par défaut
    if couleur is None:
        couleur = settings.COULEURS_CAMEROUN['vert']
    
    # Créer le graphique
    mode = 'lines+markers' if show_markers else 'lines'
    
    fig = go.Figure()
    
    # Ligne principale
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode=mode,
        name='Valeurs',
        line=dict(color=couleur, width=3),
        marker=dict(size=8, color=couleur),
        fill='tozeroy' if fill_area else None,
        fillcolor=f'rgba(0, 122, 51, 0.2)' if fill_area else None,
        hovertemplate='<b>%{x}</b><br>Valeur: %{y:,}<extra></extra>'.replace(',', ' ')
    ))
    
    # Ligne de moyenne (optionnelle)
    if moyenne_line and len(df) > 0:
        moyenne = df[y_col].mean()
        fig.add_hline(
            y=moyenne,
            line_dash="dash",
            line_color=settings.COULEURS_CAMEROUN['jaune'],
            annotation_text=f"Moyenne: {int(moyenne):,}".replace(',', ' '),
            annotation_position="right"
        )
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        hovermode='x unified',
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size'],
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    
    return fig

# ==============================================================================
# FONCTION 4 : GRAPHIQUE BARRES GROUPÉES (COMPARAISON)
# ==============================================================================

def creer_graphique_barres_groupees(
    data,
    x_col,
    categories_cols,
    titre="Comparaison",
    couleurs=None,
    orientation='v',
    height=500
):
    """
    Crée un graphique avec barres groupées pour comparaison.
    
    Args:
        data (pd.DataFrame): Données du graphique
        x_col (str): Colonne X (catégories principales)
        categories_cols (list): Liste des colonnes à comparer
        titre (str): Titre du graphique
        couleurs (list, optional): Liste de couleurs pour chaque série
        orientation (str): 'v' (vertical) ou 'h' (horizontal)
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    
    Example:
        >>> fig = creer_graphique_barres_groupees(
        ...     df, 'Catégorie', ['S9_2025', 'S10_2025'],
        ...     titre="Comparaison S9 vs S10"
        ... )
    """
    df = data.copy()
    
    # Couleurs par défaut
    if couleurs is None:
        couleurs = settings.COULEURS_GRAPHIQUES
    
    fig = go.Figure()
    
    # Ajouter une barre pour chaque série
    for i, col in enumerate(categories_cols):
        couleur = couleurs[i % len(couleurs)]
        
        if orientation == 'v':
            fig.add_trace(go.Bar(
                name=col,
                x=df[x_col],
                y=df[col],
                marker_color=couleur,
                text=df[col],
                textposition='outside',
                texttemplate='%{text:,}'.replace(',', ' '),
                hovertemplate='<b>%{x}</b><br>' + col + ': %{y:,}<extra></extra>'.replace(',', ' ')
            ))
        else:
            fig.add_trace(go.Bar(
                name=col,
                x=df[col],
                y=df[x_col],
                marker_color=couleur,
                orientation='h',
                text=df[col],
                textposition='outside',
                texttemplate='%{text:,}'.replace(',', ' '),
                hovertemplate='<b>%{y}</b><br>' + col + ': %{x:,}<extra></extra>'.replace(',', ' ')
            ))
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=x_col if orientation == 'v' else "Valeur",
        yaxis_title="Valeur" if orientation == 'v' else x_col,
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        barmode='group',
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size'],
        plot_bgcolor='white'
    )
    
    return fig

# ==============================================================================
# FONCTION 5 : HEATMAP (CARTE DE CHALEUR)
# ==============================================================================

def creer_heatmap(
    data,
    x_col,
    y_col,
    z_col,
    titre="Carte de Chaleur",
    colorscale='Greens',
    show_values=True,
    height=600
):
    """
    Crée une carte de chaleur (heatmap).
    
    Args:
        data (pd.DataFrame): Données du graphique
        x_col (str): Colonne X
        y_col (str): Colonne Y
        z_col (str): Colonne des valeurs (couleur)
        titre (str): Titre du graphique
        colorscale (str): Échelle de couleurs Plotly
        show_values (bool): Afficher les valeurs dans les cellules
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    
    Example:
        >>> fig = creer_heatmap(df, 'Jour', 'Semaine', 'Appels', titre="Intensité des appels")
    """
    # Pivoter les données pour la heatmap
    df_pivot = data.pivot(index=y_col, columns=x_col, values=z_col)
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale=colorscale,
        text=df_pivot.values if show_values else None,
        texttemplate='%{text:,}'.replace(',', ' ') if show_values else None,
        hovertemplate='%{x}<br>%{y}<br>Valeur: %{z:,}<extra></extra>'.replace(',', ' ')
    ))
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size']
    )
    
    return fig

# ==============================================================================
# FONCTION 6 : GRAPHIQUE D'ÉVOLUTION AVANCÉ
# ==============================================================================

def creer_graphique_evolution(
    data,
    x_col,
    y_col,
    titre="Évolution Temporelle",
    ajouter_tendance=False,
    ajouter_moyenne=True,
    couleur=None,
    height=500
):
    """
    Crée un graphique d'évolution avancé avec tendance et moyenne.
    
    Args:
        data (pd.DataFrame): Données du graphique
        x_col (str): Colonne X (temporelle)
        y_col (str): Colonne Y (valeurs)
        titre (str): Titre du graphique
        ajouter_tendance (bool): Ajouter ligne de tendance (régression linéaire)
        ajouter_moyenne (bool): Ajouter ligne de moyenne
        couleur (str, optional): Couleur principale
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    """
    df = data.copy()
    
    if couleur is None:
        couleur = settings.COULEURS_CAMEROUN['vert']
    
    fig = go.Figure()
    
    # Courbe principale
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        name='Données',
        line=dict(color=couleur, width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(0, 122, 51, 0.2)',
        hovertemplate='<b>%{x}</b><br>Valeur: %{y:,}<extra></extra>'.replace(',', ' ')
    ))
    
    # Ligne de moyenne
    if ajouter_moyenne:
        moyenne = df[y_col].mean()
        fig.add_hline(
            y=moyenne,
            line_dash="dash",
            line_color=settings.COULEURS_CAMEROUN['jaune'],
            annotation_text=f"Moyenne: {int(moyenne):,}".replace(',', ' '),
            annotation_position="right"
        )
    
    # Ligne de tendance (régression linéaire)
    if ajouter_tendance and len(df) > 1:
        x_numeric = np.arange(len(df))
        coeffs = np.polyfit(x_numeric, df[y_col], 1)
        tendance = coeffs[0] * x_numeric + coeffs[1]
        
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=tendance,
            mode='lines',
            name='Tendance',
            line=dict(color=settings.COULEURS_CAMEROUN['jaune'], width=2, dash='dash'),
            hovertemplate='Tendance: %{y:,.0f}<extra></extra>'.replace(',', ' ')
        ))
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        hovermode='x unified',
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size'],
        plot_bgcolor='white'
    )
    
    return fig

# ==============================================================================
# FONCTION 7 : GRAPHIQUE DE VARIATION (+/-)
# ==============================================================================

def creer_graphique_variation(
    data,
    x_col,
    y_col,
    titre="Variations",
    couleur_positive=None,
    couleur_negative=None,
    height=500
):
    """
    Crée un graphique de variations avec couleurs différentes pour +/-.
    
    Args:
        data (pd.DataFrame): Données avec variations
        x_col (str): Colonne X (catégories/périodes)
        y_col (str): Colonne Y (valeurs de variation)
        titre (str): Titre du graphique
        couleur_positive (str, optional): Couleur pour valeurs positives
        couleur_negative (str, optional): Couleur pour valeurs négatives
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    """
    df = data.copy()
    
    if couleur_positive is None:
        couleur_positive = '#28a745'
    if couleur_negative is None:
        couleur_negative = '#dc3545'
    
    # Déterminer les couleurs selon le signe
    couleurs = [couleur_positive if x > 0 else couleur_negative for x in df[y_col]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker_color=couleurs,
            text=df[y_col],
            textposition='outside',
            texttemplate='%{text:+,.0f}'.replace(',', ' '),
            hovertemplate='<b>%{x}</b><br>Variation: %{y:+,}<extra></extra>'.replace(',', ' ')
        )
    ])
    
    # Ajouter ligne de référence à zéro
    fig.add_hline(y=0, line_width=2, line_color='black')
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=x_col,
        yaxis_title="Variation",
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        showlegend=False,
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size'],
        plot_bgcolor='white'
    )
    
    return fig

# ==============================================================================
# FONCTION 8 : GRAPHIQUE DE COMPARAISON MULTI-CRITÈRES
# ==============================================================================

def creer_graphique_comparaison(
    data,
    categories,
    series_dict,
    titre="Comparaison",
    type_graphique='barres',
    height=500
):
    """
    Crée un graphique de comparaison pour plusieurs séries.
    
    Args:
        data (pd.DataFrame): Données
        categories (str): Nom de la colonne des catégories
        series_dict (dict): {nom_serie: nom_colonne}
        titre (str): Titre du graphique
        type_graphique (str): 'barres' ou 'lignes'
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    """
    df = data.copy()
    fig = go.Figure()
    
    couleurs = settings.COULEURS_GRAPHIQUES
    
    for i, (nom_serie, col_data) in enumerate(series_dict.items()):
        couleur = couleurs[i % len(couleurs)]
        
        if type_graphique == 'barres':
            fig.add_trace(go.Bar(
                name=nom_serie,
                x=df[categories],
                y=df[col_data],
                marker_color=couleur,
                hovertemplate='<b>%{x}</b><br>' + nom_serie + ': %{y:,}<extra></extra>'.replace(',', ' ')
            ))
        else:  # lignes
            fig.add_trace(go.Scatter(
                name=nom_serie,
                x=df[categories],
                y=df[col_data],
                mode='lines+markers',
                line=dict(color=couleur, width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{x}</b><br>' + nom_serie + ': %{y:,}<extra></extra>'.replace(',', ' ')
            ))
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=categories,
        yaxis_title="Valeur",
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        barmode='group' if type_graphique == 'barres' else None,
        hovermode='x unified',
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size'],
        plot_bgcolor='white'
    )
    
    return fig

# ==============================================================================
# FONCTION 9 : GRAPHIQUE DE DISTRIBUTION
# ==============================================================================

def creer_graphique_distribution(
    data,
    valeurs_col,
    titre="Distribution",
    bins=20,
    couleur=None,
    show_moyenne=True,
    height=500
):
    """
    Crée un histogramme de distribution.
    
    Args:
        data (pd.DataFrame): Données
        valeurs_col (str): Colonne des valeurs
        titre (str): Titre du graphique
        bins (int): Nombre de barres
        couleur (str, optional): Couleur de l'histogramme
        show_moyenne (bool): Afficher la ligne de moyenne
        height (int): Hauteur du graphique
    
    Returns:
        plotly.graph_objects.Figure: Graphique Plotly
    """
    df = data.copy()
    
    if couleur is None:
        couleur = settings.COULEURS_CAMEROUN['vert']
    
    fig = go.Figure(data=[
        go.Histogram(
            x=df[valeurs_col],
            nbinsx=bins,
            marker_color=couleur,
            opacity=0.75,
            hovertemplate='Intervalle: %{x}<br>Fréquence: %{y}<extra></extra>'
        )
    ])
    
    # Ligne de moyenne
    if show_moyenne:
        moyenne = df[valeurs_col].mean()
        fig.add_vline(
            x=moyenne,
            line_dash="dash",
            line_color=settings.COULEURS_CAMEROUN['jaune'],
            line_width=3,
            annotation_text=f"Moyenne: {moyenne:.1f}",
            annotation_position="top"
        )
    
    # Mise en forme
    fig.update_layout(
        title=titre,
        xaxis_title=valeurs_col,
        yaxis_title="Fréquence",
        height=height,
        template=settings.PLOTLY_TEMPLATE,
        showlegend=False,
        font=dict(family=settings.GRAPH_CONFIG['font_family'], size=settings.GRAPH_CONFIG['font_size']),
        title_font_size=settings.GRAPH_CONFIG['title_font_size'],
        plot_bgcolor='white'
    )
    
    return fig

# ==============================================================================
# FIN DU MODULE
# ==============================================================================