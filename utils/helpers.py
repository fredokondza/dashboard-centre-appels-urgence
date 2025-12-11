"""
==============================================================================
MODULE DES FONCTIONS UTILITAIRES
==============================================================================
Ce module centralise les fonctions utilitaires répétées dans l'application.

Fonctions principales :
- extraire_numero_semaine() : Extraction numéro depuis 'S10_2025'
- obtenir_derniere_semaine() : Dernière semaine disponible
- obtenir_semaine_precedente() : Semaine précédente
- obtenir_info_semaine_calendrier() : Info détaillée d'une semaine
- obtenir_evolution_temporelle() : Données pour graphique évolution
- convert_df_to_csv() : Export CSV
- convert_df_to_excel() : Export Excel
- formater_nombre() : Format avec espaces milliers
- obtenir_mois_francais() : Dictionnaire mois en français
- formater_date_francais() : Format date français
- formater_periode_semaine() : Format période

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

import pandas as pd
import io
from datetime import datetime, timedelta
from pathlib import Path

# Import de la configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import settings

# ==============================================================================
# FONCTION 1 : EXTRACTION NUMÉRO DE SEMAINE (⭐ LA PLUS RÉPÉTÉE)
# ==============================================================================

def extraire_numero_semaine(semaine_label):
    """
    Extrait le numéro de la semaine depuis le label.
    
    Cette fonction était répétée dans 4 pages différentes !
    
    Args:
        semaine_label (str): Label de la semaine (ex: 'S10_2025', 'S5_2025')
    
    Returns:
        int: Numéro de la semaine (10, 5, etc.)
             Retourne 0 si l'extraction échoue
    
    Example:
        >>> extraire_numero_semaine('S10_2025')
        10
        >>> extraire_numero_semaine('S5_2025')
        5
        >>> extraire_numero_semaine('invalid')
        0
    """
    try:
        # Format attendu : S[numéro]_[année]
        # Exemple : S10_2025 → 10
        if isinstance(semaine_label, str) and '_' in semaine_label:
            partie_semaine = semaine_label.split('_')[0]  # 'S10'
            numero = partie_semaine.replace('S', '').replace('s', '')  # '10'
            return int(numero)
        else:
            return 0
    except (ValueError, IndexError, AttributeError):
        return 0

# ==============================================================================
# FONCTION 2 : OBTENIR LA DERNIÈRE SEMAINE
# ==============================================================================

def obtenir_derniere_semaine(df_hebdo):
    """
    Retourne la dernière semaine épidémiologique disponible.
    
    Args:
        df_hebdo (pd.DataFrame): DataFrame des données hebdomadaires
            Doit contenir la colonne 'Semaine épidémiologique'
    
    Returns:
        str: Label de la dernière semaine (ex: 'S45_2025')
             None si le DataFrame est vide
    
    Example:
        >>> derniere = obtenir_derniere_semaine(df_hebdo)
        >>> print(derniere)
        'S45_2025'
    """
    try:
        if df_hebdo is None or len(df_hebdo) == 0:
            return None
        
        if 'Semaine épidémiologique' not in df_hebdo.columns:
            return None
        
        # Trier par numéro de semaine et prendre la dernière
        semaines = df_hebdo['Semaine épidémiologique'].tolist()
        semaines_triees = sorted(semaines, key=extraire_numero_semaine)
        
        return semaines_triees[-1] if semaines_triees else None
        
    except Exception as e:
        print(f"⚠️ Erreur dans obtenir_derniere_semaine : {str(e)}")
        return None

# ==============================================================================
# FONCTION 3 : OBTENIR LA SEMAINE PRÉCÉDENTE
# ==============================================================================

def obtenir_semaine_precedente(df_hebdo, semaine_actuelle):
    """
    Retourne la semaine épidémiologique précédente.
    
    Args:
        df_hebdo (pd.DataFrame): DataFrame des données hebdomadaires
        semaine_actuelle (str): Semaine de référence
    
    Returns:
        str: Label de la semaine précédente
             None si pas de semaine précédente
    
    Example:
        >>> precedente = obtenir_semaine_precedente(df_hebdo, 'S10_2025')
        >>> print(precedente)
        'S9_2025'
    """
    try:
        if df_hebdo is None or len(df_hebdo) == 0:
            return None
        
        if 'Semaine épidémiologique' not in df_hebdo.columns:
            return None
        
        # Trier toutes les semaines
        semaines = df_hebdo['Semaine épidémiologique'].tolist()
        semaines_triees = sorted(semaines, key=extraire_numero_semaine)
        
        # Trouver l'index de la semaine actuelle
        if semaine_actuelle not in semaines_triees:
            return None
        
        index_actuel = semaines_triees.index(semaine_actuelle)
        
        # Retourner la précédente si elle existe
        if index_actuel > 0:
            return semaines_triees[index_actuel - 1]
        else:
            return None
        
    except Exception as e:
        print(f"⚠️ Erreur dans obtenir_semaine_precedente : {str(e)}")
        return None

# ==============================================================================
# FONCTION 4 : INFORMATIONS D'UNE SEMAINE DEPUIS LE CALENDRIER
# ==============================================================================

def obtenir_info_semaine_calendrier(df_calendrier, semaine):
    """
    Récupère les informations détaillées d'une semaine depuis le calendrier.
    
    Args:
        df_calendrier (pd.DataFrame): Calendrier épidémiologique
        semaine (str): Label de la semaine (ex: 'S10_2025')
    
    Returns:
        dict: Informations de la semaine :
            - 'numero' (int) : Numéro de la semaine
            - 'label' (str) : Label de la semaine
            - 'mois' (str) : Mois
            - 'date_debut' (datetime) : Date de début
            - 'date_fin' (datetime) : Date de fin
            - 'nb_jours' (int) : Nombre de jours
        None si la semaine n'existe pas
    
    Example:
        >>> info = obtenir_info_semaine_calendrier(df_cal, 'S10_2025')
        >>> print(info['mois'])
        'Mars'
    """
    try:
        if df_calendrier is None or len(df_calendrier) == 0:
            return None
        
        # Rechercher la semaine dans le calendrier
        if 'Week_Label' in df_calendrier.columns:
            df_sem = df_calendrier[df_calendrier['Week_Label'] == semaine]
        else:
            return None
        
        if len(df_sem) == 0:
            return None
        
        ligne = df_sem.iloc[0]
        
        info = {
            'numero': int(ligne['Week_No']) if 'Week_No' in ligne else extraire_numero_semaine(semaine),
            'label': semaine,
            'mois': ligne['Month'] if 'Month' in ligne else None,
            'date_debut': ligne['Date_Start'] if 'Date_Start' in ligne else None,
            'date_fin': ligne['Date_End'] if 'Date_End' in ligne else None
        }
        
        # Calculer le nombre de jours
        if info['date_debut'] and info['date_fin']:
            info['nb_jours'] = (info['date_fin'] - info['date_debut']).days + 1
        else:
            info['nb_jours'] = 7  # Par défaut
        
        return info
        
    except Exception as e:
        print(f"⚠️ Erreur dans obtenir_info_semaine_calendrier : {str(e)}")
        return None

# ==============================================================================
# FONCTION 5 : DONNÉES POUR GRAPHIQUE D'ÉVOLUTION
# ==============================================================================

def obtenir_evolution_temporelle(df_hebdo, nb_semaines=10, semaine_fin=None):
    """
    Prépare les données pour un graphique d'évolution temporelle.
    
    Args:
        df_hebdo (pd.DataFrame): Données hebdomadaires
        nb_semaines (int): Nombre de semaines à afficher
        semaine_fin (str, optional): Semaine de fin. Si None, prend la dernière.
    
    Returns:
        dict: Données pour le graphique :
            - 'semaines' (list) : Liste des labels de semaines
            - 'valeurs' (list) : Liste des totaux correspondants
            - 'titre' (str) : Titre suggéré pour le graphique
    
    Example:
        >>> evolution = obtenir_evolution_temporelle(df_hebdo, nb_semaines=10)
        >>> print(evolution['semaines'])
        ['S36_2025', 'S37_2025', ..., 'S45_2025']
    """
    try:
        if df_hebdo is None or len(df_hebdo) == 0:
            return {'semaines': [], 'valeurs': [], 'titre': 'Évolution'}
        
        # Trier par numéro de semaine
        df_sorted = df_hebdo.copy()
        df_sorted['_sort_key'] = df_sorted['Semaine épidémiologique'].apply(extraire_numero_semaine)
        df_sorted = df_sorted.sort_values('_sort_key').reset_index(drop=True)
        
        # Déterminer la semaine de fin
        if semaine_fin is None:
            semaine_fin = df_sorted['Semaine épidémiologique'].iloc[-1]
        
        # Trouver l'index de la semaine de fin
        if semaine_fin in df_sorted['Semaine épidémiologique'].values:
            index_fin = df_sorted[df_sorted['Semaine épidémiologique'] == semaine_fin].index[0]
        else:
            index_fin = len(df_sorted) - 1
        
        # Calculer l'index de début
        index_debut = max(0, index_fin - nb_semaines + 1)
        
        # Extraire les données
        df_evolution = df_sorted.iloc[index_debut:index_fin+1]
        
        semaines = df_evolution['Semaine épidémiologique'].tolist()
        valeurs = df_evolution['TOTAL_APPELS_SEMAINE'].tolist()
        
        # Créer le titre
        if len(semaines) > 0:
            premiere = semaines[0]
            derniere = semaines[-1]
            titre = f"Évolution de {premiere} à {derniere}"
        else:
            titre = "Évolution temporelle"
        
        return {
            'semaines': semaines,
            'valeurs': valeurs,
            'titre': titre
        }
        
    except Exception as e:
        print(f"⚠️ Erreur dans obtenir_evolution_temporelle : {str(e)}")
        return {'semaines': [], 'valeurs': [], 'titre': 'Évolution'}

# ==============================================================================
# FONCTION 6 : EXPORT CSV
# ==============================================================================

def convert_df_to_csv(df):
    """
    Convertit un DataFrame en CSV avec encodage UTF-8.
    
    Cette fonction était répétée dans pages/4_Donnees_Brutes.py
    
    Args:
        df (pd.DataFrame): DataFrame à exporter
    
    Returns:
        bytes: Contenu du CSV encodé en UTF-8-SIG (avec BOM pour Excel)
    
    Example:
        >>> csv_data = convert_df_to_csv(df)
        >>> # Utiliser avec st.download_button
    """
    try:
        return df.to_csv(
            index=False, 
            encoding='utf-8-sig',  # BOM pour Excel
            sep=','
        ).encode('utf-8-sig')
    except Exception as e:
        print(f"❌ Erreur lors de l'export CSV : {str(e)}")
        raise

# ==============================================================================
# FONCTION 7 : EXPORT EXCEL
# ==============================================================================

def convert_df_to_excel(df, sheet_name='Données'):
    """
    Convertit un DataFrame en fichier Excel (.xlsx).
    
    Cette fonction était répétée dans pages/4_Donnees_Brutes.py
    
    Args:
        df (pd.DataFrame): DataFrame à exporter
        sheet_name (str): Nom de la feuille Excel
    
    Returns:
        bytes: Contenu du fichier Excel
    
    Example:
        >>> excel_data = convert_df_to_excel(df, 'Appels 2025')
        >>> # Utiliser avec st.download_button
    """
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        return output.getvalue()
    except Exception as e:
        print(f"❌ Erreur lors de l'export Excel : {str(e)}")
        raise

# ==============================================================================
# FONCTION 8 : FORMATAGE DE NOMBRES
# ==============================================================================

def formater_nombre(nombre, decimales=0, separateur=' '):
    """
    Formate un nombre avec séparateur de milliers.
    
    Args:
        nombre (int, float): Nombre à formater
        decimales (int): Nombre de décimales
        separateur (str): Séparateur de milliers (espace par défaut)
    
    Returns:
        str: Nombre formaté
    
    Example:
        >>> formater_nombre(1500)
        '1 500'
        >>> formater_nombre(1500.5, decimales=2)
        '1 500,50'
        >>> formater_nombre(1000000)
        '1 000 000'
    """
    try:
        if pd.isna(nombre):
            return '0'
        
        # Convertir en float
        nombre = float(nombre)
        
        if decimales == 0:
            # Format entier
            nombre_str = f"{int(nombre):,}".replace(',', separateur)
        else:
            # Format décimal
            nombre_str = f"{nombre:,.{decimales}f}".replace(',', separateur).replace('.', ',')
        
        return nombre_str
        
    except (ValueError, TypeError):
        return str(nombre)

# ==============================================================================
# FONCTION 9 : OBTENIR MOIS EN FRANÇAIS
# ==============================================================================

def obtenir_mois_francais():
    """
    Retourne le dictionnaire des mois en français.
    
    Cette fonction était répétée (dictionnaire local) dans plusieurs pages.
    
    Returns:
        dict: Dictionnaire {numéro: nom}
    
    Example:
        >>> mois = obtenir_mois_francais()
        >>> print(mois[3])
        'Mars'
    """
    return settings.MOIS_FRANCAIS.copy()

# ==============================================================================
# FONCTION 10 : FORMATER DATE EN FRANÇAIS
# ==============================================================================

def formater_date_francais(date_obj, format_long=False):
    """
    Formate une date en français.
    
    Args:
        date_obj (datetime): Date à formater
        format_long (bool): Si True, format long avec jour de la semaine
    
    Returns:
        str: Date formatée
    
    Example:
        >>> from datetime import datetime
        >>> date = datetime(2025, 11, 15)
        >>> formater_date_francais(date)
        '15 Novembre 2025'
        >>> formater_date_francais(date, format_long=True)
        'Samedi 15 Novembre 2025'
    """
    try:
        if pd.isna(date_obj):
            return ''
        
        # Convertir en datetime si nécessaire
        if isinstance(date_obj, str):
            date_obj = pd.to_datetime(date_obj)
        
        mois_fr = obtenir_mois_francais()
        
        if format_long:
            jours_fr = settings.JOURS_FRANCAIS
            jour_semaine = jours_fr.get(date_obj.weekday(), '')
            return f"{jour_semaine} {date_obj.day} {mois_fr[date_obj.month]} {date_obj.year}"
        else:
            return f"{date_obj.day:02d} {mois_fr[date_obj.month]} {date_obj.year}"
        
    except Exception as e:
        print(f"⚠️ Erreur dans formater_date_francais : {str(e)}")
        return str(date_obj)

# ==============================================================================
# FONCTION 11 : FORMATER PÉRIODE DE SEMAINE
# ==============================================================================

def formater_periode_semaine(date_min, date_max):
    """
    Formate une période de semaine en français.
    
    Args:
        date_min (datetime): Date de début
        date_max (datetime): Date de fin
    
    Returns:
        str: Période formatée
    
    Example:
        >>> from datetime import datetime
        >>> debut = datetime(2025, 11, 1)
        >>> fin = datetime(2025, 11, 7)
        >>> formater_periode_semaine(debut, fin)
        '01 au 07 Novembre 2025'
    """
    try:
        if pd.isna(date_min) or pd.isna(date_max):
            return ''
        
        mois_fr = obtenir_mois_francais()
        
        # Si même mois
        if date_min.month == date_max.month and date_min.year == date_max.year:
            return f"{date_min.day:02d} au {date_max.day:02d} {mois_fr[date_max.month]} {date_max.year}"
        # Si mois différents mais même année
        elif date_min.year == date_max.year:
            return f"{date_min.day:02d} {mois_fr[date_min.month]} au {date_max.day:02d} {mois_fr[date_max.month]} {date_max.year}"
        # Si années différentes
        else:
            return f"{date_min.day:02d} {mois_fr[date_min.month]} {date_min.year} au {date_max.day:02d} {mois_fr[date_max.month]} {date_max.year}"
        
    except Exception as e:
        print(f"⚠️ Erreur dans formater_periode_semaine : {str(e)}")
        return f"{date_min} au {date_max}"

# ==============================================================================
# FONCTION BONUS 1 : GÉNÉRER NOM DE FICHIER AVEC DATE
# ==============================================================================

def generer_nom_fichier(prefixe, extension='xlsx', include_timestamp=True):
    """
    Génère un nom de fichier standardisé avec date.
    
    Args:
        prefixe (str): Préfixe du nom de fichier
        extension (str): Extension sans le point
        include_timestamp (bool): Inclure l'heure ou seulement la date
    
    Returns:
        str: Nom de fichier généré
    
    Example:
        >>> generer_nom_fichier('rapport_minsante', 'pptx')
        'rapport_minsante_2025-11-15.pptx'
        >>> generer_nom_fichier('export', 'csv', include_timestamp=True)
        'export_2025-11-15_14-30-25.csv'
    """
    now = datetime.now()
    
    if include_timestamp:
        date_str = now.strftime('%Y-%m-%d_%H-%M-%S')
    else:
        date_str = now.strftime('%Y-%m-%d')
    
    return f"{prefixe}_{date_str}.{extension}"

# ==============================================================================
# FONCTION BONUS 2 : VALIDER FORMAT SEMAINE
# ==============================================================================

def valider_format_semaine(semaine_label):
    """
    Vérifie si le format d'une semaine est valide.
    
    Args:
        semaine_label (str): Label de la semaine
    
    Returns:
        bool: True si le format est valide (S[1-52]_[année])
    
    Example:
        >>> valider_format_semaine('S10_2025')
        True
        >>> valider_format_semaine('invalid')
        False
        >>> valider_format_semaine('S60_2025')
        False
    """
    try:
        if not isinstance(semaine_label, str):
            return False
        
        if '_' not in semaine_label:
            return False
        
        parties = semaine_label.split('_')
        if len(parties) != 2:
            return False
        
        # Vérifier la partie semaine (S1 à S52)
        partie_semaine = parties[0]
        if not partie_semaine.startswith('S') and not partie_semaine.startswith('s'):
            return False
        
        numero = extraire_numero_semaine(semaine_label)
        if numero < 1 or numero > 53:  # 53 pour les années avec 53 semaines
            return False
        
        # Vérifier la partie année
        partie_annee = parties[1]
        if not partie_annee.isdigit():
            return False
        
        annee = int(partie_annee)
        if annee < 2000 or annee > 2100:  # Plage raisonnable
            return False
        
        return True
        
    except Exception:
        return False

# ==============================================================================
# FONCTION BONUS 3 : CALCULER DURÉE ENTRE DEUX DATES
# ==============================================================================

def calculer_duree_jours(date_debut, date_fin):
    """
    Calcule le nombre de jours entre deux dates.
    
    Args:
        date_debut (datetime): Date de début
        date_fin (datetime): Date de fin
    
    Returns:
        int: Nombre de jours (inclus)
    
    Example:
        >>> from datetime import datetime
        >>> debut = datetime(2025, 11, 1)
        >>> fin = datetime(2025, 11, 7)
        >>> calculer_duree_jours(debut, fin)
        7
    """
    try:
        if pd.isna(date_debut) or pd.isna(date_fin):
            return 0
        
        delta = date_fin - date_debut
        return delta.days + 1  # +1 pour inclure le dernier jour
        
    except Exception:
        return 0

# ==============================================================================
# FIN DU MODULE
# ==============================================================================