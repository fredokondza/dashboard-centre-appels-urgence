"""
==============================================================================
MODULE DES COMPOSANTS TABLEAUX
==============================================================================
Ce module fournit des composants pour l'affichage et l'export de tableaux
de données avec formatage automatique.

Composants disponibles :
- display_dataframe_formatted() : DataFrame avec formatage auto
- export_buttons() : Boutons d'export CSV et Excel
- create_summary_table() : Tableau récapitulatif stylisé
- create_comparison_table() : Tableau de comparaison avec mise en forme

Fonctionnalités :
- Formatage automatique des dates (DD/MM/YYYY)
- Formatage automatique des nombres (espaces milliers)
- Exports multiformats (CSV, Excel)
- Mise en forme conditionnelle
- Styles cohérents MINSANTE

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Import de la configuration
sys.path.append(str(Path(__file__).parent.parent))

from config import settings
from utils.helpers import formater_nombre, convert_df_to_csv, convert_df_to_excel, generer_nom_fichier

# ==============================================================================
# FONCTION 1 : AFFICHAGE DATAFRAME FORMATÉ
# ==============================================================================

def display_dataframe_formatted(
    df,
    format_dates=True,
    format_numbers=True,
    height=600,
    use_container_width=True,
    hide_index=True,
    title=None
):
    """
    Affiche un DataFrame avec formatage automatique.
    
    Cette fonction :
    - Formate les dates en DD/MM/YYYY
    - Formate les nombres avec espaces milliers
    - Applique un style cohérent
    - Gère l'affichage responsive
    
    Args:
        df (pd.DataFrame): DataFrame à afficher
        format_dates (bool): Formater les colonnes de dates
        format_numbers (bool): Formater les colonnes numériques
        height (int): Hauteur du tableau en pixels
        use_container_width (bool): Utiliser toute la largeur du conteneur
        hide_index (bool): Masquer l'index
        title (str, optional): Titre du tableau
    
    Returns:
        None (affiche directement dans Streamlit)
    
    Example:
        >>> display_dataframe_formatted(
        ...     df,
        ...     title="Données Journalières",
        ...     height=800
        ... )
    
    Note:
        Cette fonction remplace les appels répétés à st.dataframe()
        avec formatage manuel.
    """
    # Copier le DataFrame pour ne pas modifier l'original
    df_display = df.copy()
    
    # === FORMATAGE DES DATES ===
    if format_dates:
        for col in df_display.columns:
            if pd.api.types.is_datetime64_any_dtype(df_display[col]):
                df_display[col] = df_display[col].dt.strftime(settings.FORMAT_DATE)
    
    # === FORMATAGE DES NOMBRES ===
    if format_numbers:
        for col in df_display.columns:
            # Vérifier si c'est une colonne numérique (int ou float)
            if pd.api.types.is_numeric_dtype(df_display[col]):
                # Ne pas formater les colonnes qui ressemblent à des IDs ou années
                if not any(keyword in col.lower() for keyword in ['id', 'no', 'year', 'annee']):
                    # Formater avec espaces milliers
                    df_display[col] = df_display[col].apply(
                        lambda x: formater_nombre(x) if pd.notna(x) else ''
                    )
    
    # === AFFICHAGE ===
    if title:
        st.markdown(f"#### {title}")
    
    st.dataframe(
        df_display,
        height=height,
        use_container_width=use_container_width,
        hide_index=hide_index
    )

# ==============================================================================
# FONCTION 2 : BOUTONS D'EXPORT MULTIFORMATS
# ==============================================================================

def export_buttons(
    df,
    filename_prefix="export",
    formats=None,
    show_date=True,
    label_csv="📥 Télécharger CSV",
    label_excel="📥 Télécharger Excel",
    columns=None
):
    """
    Affiche des boutons pour exporter un DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame à exporter
        filename_prefix (str): Préfixe du nom de fichier
        formats (list, optional): Liste des formats ['csv', 'excel']
            Si None, affiche les deux formats
        show_date (bool): Inclure la date dans le nom de fichier
        label_csv (str): Label du bouton CSV
        label_excel (str): Label du bouton Excel
        columns (int, optional): Nombre de colonnes pour les boutons
            Si None, auto-détecté selon le nombre de formats
    
    Returns:
        None (affiche les boutons directement)
    
    Example:
        >>> export_buttons(
        ...     df,
        ...     filename_prefix="donnees_appels",
        ...     formats=['csv', 'excel']
        ... )
    
    Note:
        Cette fonction centralise la logique d'export répétée
        dans pages/4_Donnees_Brutes.py et autres pages.
    """
    # Formats par défaut
    if formats is None:
        formats = ['csv', 'excel']
    
    # Déterminer le nombre de colonnes
    if columns is None:
        columns = len(formats)
    
    # Créer les colonnes
    cols = st.columns(columns)
    
    # === EXPORT CSV ===
    if 'csv' in formats:
        col_index = formats.index('csv')
        
        with cols[col_index]:
            # Générer le nom de fichier
            if show_date:
                filename_csv = generer_nom_fichier(filename_prefix, 'csv', include_timestamp=False)
            else:
                filename_csv = f"{filename_prefix}.csv"
            
            # Convertir en CSV
            csv_data = convert_df_to_csv(df)
            
            # Bouton de téléchargement
            st.download_button(
                label=label_csv,
                data=csv_data,
                file_name=filename_csv,
                mime="text/csv",
                help="Télécharger au format CSV (compatible Excel)",
                use_container_width=True
            )
    
    # === EXPORT EXCEL ===
    if 'excel' in formats:
        col_index = formats.index('excel')
        
        with cols[col_index]:
            # Générer le nom de fichier
            if show_date:
                filename_excel = generer_nom_fichier(filename_prefix, 'xlsx', include_timestamp=False)
            else:
                filename_excel = f"{filename_prefix}.xlsx"
            
            # Convertir en Excel
            excel_data = convert_df_to_excel(df, sheet_name='Données')
            
            # Bouton de téléchargement
            st.download_button(
                label=label_excel,
                data=excel_data,
                file_name=filename_excel,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Télécharger au format Excel (.xlsx)",
                use_container_width=True
            )

# ==============================================================================
# FONCTION 3 : TABLEAU RÉCAPITULATIF STYLISÉ
# ==============================================================================

def create_summary_table(
    data_dict,
    title="Résumé",
    icon="📊",
    show_total=False,
    total_label="TOTAL"
):
    """
    Crée un tableau récapitulatif stylisé à partir d'un dictionnaire.
    
    Args:
        data_dict (dict): Dictionnaire {label: valeur}
        title (str): Titre du tableau
        icon (str): Emoji ou icône
        show_total (bool): Afficher une ligne de total
        total_label (str): Label de la ligne de total
    
    Returns:
        None (affiche directement)
    
    Example:
        >>> create_summary_table(
        ...     {'Renseignements': 3000, 'Assistances': 2000, 'Signaux': 500},
        ...     title="Répartition par Thématique",
        ...     show_total=True
        ... )
    
    Note:
        Affiche un tableau HTML stylisé avec les couleurs Cameroun
    """
    # Construire le HTML du tableau
    html = f'''
    <div style="
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    ">
        <!-- Titre -->
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #FFD700;
        ">
            <span style="font-size: 2em;">{icon}</span>
            <span style="font-size: 1.3em; font-weight: 600; color: #007A33;">{title}</span>
        </div>
        
        <!-- Tableau -->
        <table style="width: 100%; border-collapse: collapse;">
    '''
    
    # Lignes de données
    total = 0
    for i, (label, value) in enumerate(data_dict.items()):
        # Formater la valeur
        if isinstance(value, (int, float)):
            value_formatted = formater_nombre(value)
            total += value
        else:
            value_formatted = str(value)
        
        # Couleur de fond alternée
        bg_color = '#f8f9fa' if i % 2 == 0 else 'white'
        
        html += f'''
        <tr style="background-color: {bg_color};">
            <td style="padding: 12px; border-bottom: 1px solid #e9ecef; color: #343a40; font-weight: 500;">
                {label}
            </td>
            <td style="padding: 12px; border-bottom: 1px solid #e9ecef; text-align: right; font-weight: 600; color: #007A33; font-size: 1.1em;">
                {value_formatted}
            </td>
        </tr>
        '''
    
    # Ligne de total
    if show_total:
        html += f'''
        <tr style="background-color: #007A33; color: white; font-weight: bold;">
            <td style="padding: 15px; border-top: 3px solid #FFD700;">
                {total_label}
            </td>
            <td style="padding: 15px; text-align: right; font-size: 1.2em; border-top: 3px solid #FFD700;">
                {formater_nombre(total)}
            </td>
        </tr>
        '''
    
    html += '''
        </table>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# FONCTION 4 : TABLEAU DE COMPARAISON
# ==============================================================================

def create_comparison_table(
    df,
    columns_to_compare,
    category_column,
    labels=None,
    highlight_changes=True,
    show_variation=True
):
    """
    Crée un tableau de comparaison avec mise en forme conditionnelle.
    
    Args:
        df (pd.DataFrame): DataFrame source
        columns_to_compare (list): Liste des colonnes à comparer
        category_column (str): Nom de la colonne des catégories
        labels (dict, optional): Dictionnaire de renommage des colonnes
        highlight_changes (bool): Surligner les variations
        show_variation (bool): Ajouter une colonne de variation
    
    Returns:
        None (affiche directement)
    
    Example:
        >>> create_comparison_table(
        ...     df,
        ...     columns_to_compare=['S9_2025', 'S10_2025'],
        ...     category_column='Catégorie',
        ...     show_variation=True
        ... )
    
    Note:
        Utile pour comparer plusieurs périodes (semaines, mois, etc.)
    """
    # Copier le DataFrame
    df_comp = df.copy()
    
    # Renommer les colonnes si labels fournis
    if labels:
        df_comp = df_comp.rename(columns=labels)
        columns_to_compare = [labels.get(col, col) for col in columns_to_compare]
    
    # Calculer la variation si demandé
    if show_variation and len(columns_to_compare) >= 2:
        col1 = columns_to_compare[0]
        col2 = columns_to_compare[-1]
        
        df_comp['Variation'] = df_comp[col2] - df_comp[col1]
        df_comp['Variation %'] = df_comp.apply(
            lambda row: ((row[col2] - row[col1]) / row[col1] * 100) if row[col1] != 0 else 0,
            axis=1
        )
    
    # Sélectionner les colonnes à afficher
    display_columns = [category_column] + columns_to_compare
    if show_variation:
        display_columns += ['Variation', 'Variation %']
    
    df_display = df_comp[display_columns].copy()
    
    # Formater les nombres
    for col in columns_to_compare:
        if pd.api.types.is_numeric_dtype(df_display[col]):
            df_display[col] = df_display[col].apply(
                lambda x: formater_nombre(x) if pd.notna(x) else ''
            )
    
    if show_variation:
        df_display['Variation'] = df_display['Variation'].apply(
            lambda x: f"{formater_nombre(x):+}" if pd.notna(x) else ''
        )
        df_display['Variation %'] = df_display['Variation %'].apply(
            lambda x: f"{x:+.1f}%" if pd.notna(x) else ''
        )
    
    # Afficher le tableau
    st.markdown("#### Tableau Comparatif")
    
    # Utiliser st.dataframe avec style (si highlight_changes)
    if highlight_changes and show_variation:
        # Créer un styler
        def color_variation(val):
            """Colorer selon le signe de la variation."""
            try:
                if '+' in str(val):
                    return 'color: #28a745; font-weight: bold;'
                elif '-' in str(val):
                    return 'color: #dc3545; font-weight: bold;'
                else:
                    return 'color: #6c757d;'
            except:
                return ''
        
        # Afficher avec style
        st.dataframe(
            df_display,
            use_container_width=True,
            height=min(400, 50 + len(df_display) * 35),
            hide_index=True
        )
    else:
        # Afficher sans style
        st.dataframe(
            df_display,
            use_container_width=True,
            height=min(400, 50 + len(df_display) * 35),
            hide_index=True
        )

# ==============================================================================
# FONCTION BONUS 1 : TABLEAU AVEC SPARKLINES
# ==============================================================================

def create_table_with_sparklines(df, value_column, sparkline_columns, title="Tableau avec Tendances"):
    """
    Crée un tableau avec mini-graphiques sparkline.
    
    Args:
        df (pd.DataFrame): DataFrame source
        value_column (str): Colonne de la valeur principale
        sparkline_columns (list): Colonnes pour les sparklines
        title (str): Titre du tableau
    
    Note:
        Fonctionnalité avancée - sparklines en HTML/CSS pur sont limitées.
        Pour de vraies sparklines, utiliser Plotly ou matplotlib.
    """
    st.markdown(f"#### {title}")
    st.info("💡 Fonctionnalité sparklines : À implémenter avec Plotly pour de meilleurs résultats")
    
    # Pour l'instant, afficher un tableau standard
    display_dataframe_formatted(df)

# ==============================================================================
# FONCTION BONUS 2 : TABLEAU PIVOT INTERACTIF
# ==============================================================================

def create_pivot_table_interface(df, title="Tableau Croisé Dynamique"):
    """
    Interface pour créer un tableau croisé dynamique interactif.
    
    Args:
        df (pd.DataFrame): DataFrame source
        title (str): Titre de l'interface
    
    Example:
        >>> create_pivot_table_interface(df_appels)
    """
    st.markdown(f"#### {title}")
    
    # Sélecteurs pour le pivot
    col1, col2, col3 = st.columns(3)
    
    with col1:
        index_col = st.selectbox(
            "Lignes (Index)",
            options=df.columns.tolist(),
            help="Colonne pour les lignes du tableau"
        )
    
    with col2:
        columns_col = st.selectbox(
            "Colonnes",
            options=[None] + df.columns.tolist(),
            help="Colonne pour les colonnes du tableau"
        )
    
    with col3:
        values_col = st.selectbox(
            "Valeurs",
            options=df.select_dtypes(include=['int64', 'float64']).columns.tolist(),
            help="Colonne des valeurs à agréger"
        )
    
    # Fonction d'agrégation
    agg_func = st.radio(
        "Fonction d'agrégation",
        options=['sum', 'mean', 'count', 'min', 'max'],
        horizontal=True
    )
    
    # Créer le pivot
    if st.button("📊 Générer le Tableau Croisé"):
        try:
            if columns_col:
                pivot = pd.pivot_table(
                    df,
                    index=index_col,
                    columns=columns_col,
                    values=values_col,
                    aggfunc=agg_func
                )
            else:
                pivot = df.groupby(index_col)[values_col].agg(agg_func).to_frame()
            
            # Afficher
            st.success("✅ Tableau croisé généré !")
            display_dataframe_formatted(pivot.reset_index(), format_numbers=True)
            
            # Boutons d'export
            export_buttons(pivot.reset_index(), filename_prefix="tableau_croise")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la création du tableau croisé : {str(e)}")

# ==============================================================================
# FONCTION BONUS 3 : TABLEAU AVEC FILTRES
# ==============================================================================

def create_filtered_table(df, title="Tableau Filtrable", filterable_columns=None):
    """
    Crée un tableau avec interface de filtrage.
    
    Args:
        df (pd.DataFrame): DataFrame source
        title (str): Titre du tableau
        filterable_columns (list, optional): Liste des colonnes filtrables
            Si None, toutes les colonnes sont filtrables
    
    Example:
        >>> create_filtered_table(df_appels, filterable_columns=['Semaine épidémiologique'])
    """
    st.markdown(f"#### {title}")
    
    # Déterminer les colonnes filtrables
    if filterable_columns is None:
        filterable_columns = df.columns.tolist()
    
    # Interface de filtrage
    with st.expander("🔍 Filtres", expanded=False):
        filters = {}
        
        for col in filterable_columns[:5]:  # Limiter à 5 filtres max
            if pd.api.types.is_numeric_dtype(df[col]):
                # Filtre numérique (range)
                min_val = float(df[col].min())
                max_val = float(df[col].max())
                
                filter_range = st.slider(
                    f"{col}",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    key=f"filter_{col}"
                )
                filters[col] = filter_range
            
            elif df[col].nunique() < 50:  # Filtre catégoriel
                unique_values = df[col].unique().tolist()
                selected_values = st.multiselect(
                    f"{col}",
                    options=unique_values,
                    default=unique_values,
                    key=f"filter_{col}"
                )
                filters[col] = selected_values
    
    # Appliquer les filtres
    df_filtered = df.copy()
    
    for col, filter_val in filters.items():
        if isinstance(filter_val, tuple):  # Range numérique
            df_filtered = df_filtered[
                (df_filtered[col] >= filter_val[0]) & 
                (df_filtered[col] <= filter_val[1])
            ]
        else:  # Liste de valeurs
            if filter_val:  # Si au moins une valeur sélectionnée
                df_filtered = df_filtered[df_filtered[col].isin(filter_val)]
    
    # Afficher les résultats
    st.info(f"📊 **{len(df_filtered)}** lignes correspondent aux filtres (sur {len(df)} total)")
    
    # Afficher le tableau
    display_dataframe_formatted(df_filtered)
    
    # Boutons d'export
    if len(df_filtered) > 0:
        export_buttons(df_filtered, filename_prefix="donnees_filtrees")

# ==============================================================================
# FIN DU MODULE
# ==============================================================================