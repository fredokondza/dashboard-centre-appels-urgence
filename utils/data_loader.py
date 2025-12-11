"""
==============================================================================
MODULE DE CHARGEMENT DES DONNÉES
==============================================================================
Ce module gère le chargement, la validation et la détection automatique
des fichiers de données pour le Dashboard Centre d'Appels d'Urgence.

Fonctions principales :
- charger_donnees_appels() : Charge les appels journaliers
- charger_calendrier_epidemiologique() : Charge le calendrier
- charger_toutes_les_donnees() : Charge tout avec agrégation
- verifier_coherence_donnees() : Valide la cohérence
- detecter_fichiers_data() : Détection automatique des fichiers

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.1 - Correction incohérence des totaux (suppression doublons)
==============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import os

# Import de la configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import settings

# ==============================================================================
# FONCTION 1 : CHARGEMENT DES APPELS JOURNALIERS
# ==============================================================================

def charger_donnees_appels(fichier_path=None):
    """
    Charge les données des appels journaliers depuis un fichier Excel.
    
    Args:
        fichier_path (str, optional): Chemin du fichier Excel.
            Si None, utilise le chemin par défaut de la configuration.
    
    Returns:
        pd.DataFrame: DataFrame avec les colonnes :
            - DATE (datetime)
            - Semaine épidémiologique (str)
            - TOTAL_APPELS_JOUR (int)
            - [17 catégories d'appels] (int)
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le format du fichier est invalide
    """
    try:
        # Utiliser le chemin par défaut si non spécifié
        if fichier_path is None:
            fichier_path = settings.CHEMINS_FICHIERS['appels']
        
        # Vérifier l'existence du fichier
        if not os.path.exists(fichier_path):
            raise FileNotFoundError(
                f"Le fichier des appels n'existe pas : {fichier_path}"
            )
        
        # Charger le fichier Excel
        df = pd.read_excel(
            fichier_path,
            sheet_name=settings.SHEET_APPELS,
            engine='openpyxl'
        )
        
        # Vérifier les colonnes requises
        colonnes_requises = ['DATE'] + settings.CATEGORIES_APPELS
        colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]
        
        if colonnes_manquantes:
            raise ValueError(
                f"Colonnes manquantes dans le fichier : {', '.join(colonnes_manquantes)}"
            )
        
        # Convertir la colonne DATE en datetime
        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        
        # Supprimer les lignes avec des dates invalides
        lignes_avant = len(df)
        df = df.dropna(subset=['DATE'])
        lignes_apres = len(df)
        
        if lignes_avant != lignes_apres:
            print(f"⚠️ {lignes_avant - lignes_apres} lignes avec dates invalides ont été supprimées")
        
        # Vérifier la présence de la colonne 'Semaine épidémiologique'
        if 'Semaine épidémiologique' not in df.columns:
            print("⚠️ Colonne 'Semaine épidémiologique' manquante, elle sera ajoutée")
            # Créer une semaine épidémiologique basique si absente
            df['Semaine épidémiologique'] = 'S' + df['DATE'].dt.isocalendar().week.astype(str) + '_' + df['DATE'].dt.year.astype(str)
        
        # Remplacer les valeurs manquantes par 0 pour les catégories d'appels
        for categorie in settings.CATEGORIES_APPELS:
            if categorie in df.columns:
                df[categorie] = df[categorie].fillna(0).astype(int)
        
        # Calculer le total des appels par jour si absent
        if 'TOTAL_APPELS_JOUR' not in df.columns:
            colonnes_categories = [col for col in settings.CATEGORIES_APPELS if col in df.columns]
            df['TOTAL_APPELS_JOUR'] = df[colonnes_categories].sum(axis=1)
        else:
            df['TOTAL_APPELS_JOUR'] = df['TOTAL_APPELS_JOUR'].fillna(0).astype(int)
        
        # Trier par date
        df = df.sort_values('DATE').reset_index(drop=True)
        
        print(f"✅ {len(df)} lignes chargées depuis {os.path.basename(fichier_path)}")
        print(f"📅 Période : {df['DATE'].min().strftime('%d/%m/%Y')} - {df['DATE'].max().strftime('%d/%m/%Y')}")
        
        return df
        
    except FileNotFoundError as e:
        print(f"❌ Erreur : {str(e)}")
        raise
    except ValueError as e:
        print(f"❌ Erreur de validation : {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Erreur inattendue lors du chargement : {str(e)}")
        raise

# ==============================================================================
# FONCTION 2 : CHARGEMENT DU CALENDRIER ÉPIDÉMIOLOGIQUE
# ==============================================================================

def charger_calendrier_epidemiologique(fichier_path=None):
    """
    Charge le calendrier épidémiologique depuis un fichier Excel.
    
    Args:
        fichier_path (str, optional): Chemin du fichier Excel.
            Si None, utilise le chemin par défaut de la configuration.
    
    Returns:
        pd.DataFrame: DataFrame avec les colonnes :
            - DATE (datetime) : Chaque date de l'année
            - Semaine épidémiologique (str) : Label S[num]_2025
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        Exception: Pour toute autre erreur
    """
    try:
        # Utiliser le chemin par défaut si non spécifié
        if fichier_path is None:
            fichier_path = settings.CHEMINS_FICHIERS['calendrier']
        
        # Vérifier l'existence du fichier
        if not os.path.exists(fichier_path):
            raise FileNotFoundError(
                f"Le fichier du calendrier n'existe pas : {fichier_path}"
            )
        
        print(f"📅 Chargement calendrier : {os.path.basename(fichier_path)}")
        
        # Charger le fichier avec skiprows
        df = pd.read_excel(
            fichier_path,
            sheet_name=settings.SHEET_CALENDRIER,
            skiprows=1,
            engine='openpyxl'
        )
        
        # Renommer les colonnes
        df.columns = [
            'Unnamed_0', 'Week_No', 'Month', 'From_Label', 
            'Day_Start', 'Date_Start', 'To_Label', 'Day_End', 'Date_End'
        ]
        
        # Créer le label de semaine épidémiologique
        df['Week_Label'] = 'S' + df['Week_No'].astype(str) + '_2025'
        
        # Convertir les dates en datetime
        df['Date_Start'] = pd.to_datetime(df['Date_Start'])
        df['Date_End'] = pd.to_datetime(df['Date_End'])
        
        # NOUVEAU : Créer une ligne par date (pour éviter les doublons)
        # Générer toutes les dates entre Date_Start et Date_End pour chaque semaine
        liste_dates = []
        
        for _, row in df.iterrows():
            dates_semaine = pd.date_range(
                start=row['Date_Start'],
                end=row['Date_End'],
                freq='D'
            )
            for date in dates_semaine:
                liste_dates.append({
                    'DATE': date,
                    'Semaine épidémiologique': row['Week_Label'],
                    'Week_No': row['Week_No'],
                    'Month': row['Month']
                })
        
        df_calendrier_expanded = pd.DataFrame(liste_dates)
        
        # Supprimer les doublons de dates (garder la première occurrence)
        df_calendrier_expanded = df_calendrier_expanded.drop_duplicates(subset=['DATE'], keep='first')
        
        print(f"✅ Calendrier chargé : {df['Week_No'].nunique()} semaines")
        
        return df_calendrier_expanded
        
    except FileNotFoundError as e:
        print(f"❌ Erreur : {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Erreur lors du chargement calendrier : {str(e)}")
        raise

# ==============================================================================
# FONCTION 3 : CHARGEMENT COMPLET AVEC AGRÉGATION (VERSION CORRIGÉE)
# ==============================================================================

def charger_toutes_les_donnees():
    """
    Charge toutes les données et effectue l'agrégation hebdomadaire.
    VERSION CORRIGÉE : Suppression des doublons avant agrégation.
    
    Returns:
        dict: Dictionnaire contenant :
            - 'appels' (pd.DataFrame) : Données journalières
            - 'calendrier' (pd.DataFrame) : Calendrier épidémiologique
            - 'hebdomadaire' (pd.DataFrame) : Données agrégées par semaine
            - 'statistiques' (dict) : Statistiques globales
    
    Raises:
        Exception: Si une erreur se produit lors du chargement
    """
    try:
        print("🔄 Chargement des données en cours...")
        
        # 1. Charger les appels journaliers
        df_appels = charger_donnees_appels()
        
        # 2. Charger le calendrier (version expanded avec une ligne par date)
        df_calendrier = charger_calendrier_epidemiologique()
        
        # 3. Fusion avec le calendrier (mise à jour de la semaine épidémiologique)
        # Remplacer la colonne 'Semaine épidémiologique' par celle du calendrier
        df_appels = df_appels.drop(columns=['Semaine épidémiologique'], errors='ignore')
        df_appels = df_appels.merge(
            df_calendrier[['DATE', 'Semaine épidémiologique']],
            on='DATE',
            how='left'
        )
        
        # Remplir les semaines manquantes si besoin
        if df_appels['Semaine épidémiologique'].isna().any():
            print("⚠️ Certaines dates n'ont pas de semaine dans le calendrier")
            df_appels['Semaine épidémiologique'] = df_appels['Semaine épidémiologique'].fillna(
                'S' + df_appels['DATE'].dt.isocalendar().week.astype(str) + '_' + 
                df_appels['DATE'].dt.year.astype(str)
            )
        
        # 4. CORRECTION : Supprimer les doublons de dates avant agrégation
        nb_lignes_avant = len(df_appels)
        df_appels_unique = df_appels.drop_duplicates(subset=['DATE'], keep='first').copy()
        nb_lignes_apres = len(df_appels_unique)
        
        if nb_lignes_avant != nb_lignes_apres:
            print(f"⚠️ {nb_lignes_avant - nb_lignes_apres} doublons de dates supprimés")
        
        # 5. Agrégation hebdomadaire (sur données sans doublons)
        print("📊 Agrégation des données par semaine...")
        
        # Préparer le dictionnaire d'agrégation
        agg_dict = {}
        for categorie in settings.CATEGORIES_APPELS:
            if categorie in df_appels_unique.columns:
                col_semaine = categorie.replace('_JOUR', '_SEMAINE')
                agg_dict[categorie] = 'sum'
        
        # Ajouter les agrégations pour les dates
        agg_dict['DATE'] = ['min', 'max', 'count']
        agg_dict['TOTAL_APPELS_JOUR'] = 'sum'
        
        # Grouper par semaine
        df_hebdo = df_appels_unique.groupby('Semaine épidémiologique').agg(agg_dict).reset_index()
        
        # Aplatir les colonnes multi-index
        df_hebdo.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col 
                            for col in df_hebdo.columns.values]
        
        # Renommer les colonnes
        df_hebdo = df_hebdo.rename(columns={
            'DATE_min': 'date_debut',
            'DATE_max': 'date_fin',
            'DATE_count': 'nb_jours',
            'TOTAL_APPELS_JOUR_sum': 'TOTAL_APPELS_SEMAINE'
        })
        
        # Renommer les catégories en _SEMAINE
        for categorie in settings.CATEGORIES_APPELS:
            if categorie in df_hebdo.columns:
                col_semaine = categorie.replace('_JOUR', '_SEMAINE')
                df_hebdo = df_hebdo.rename(columns={categorie: col_semaine})
        
        print(f"✅ Agrégation hebdomadaire : {len(df_hebdo)} semaines")
        print(f"📊 Total général : {df_hebdo['TOTAL_APPELS_SEMAINE'].sum():,.0f} appels")
        
        # 6. Vérification de la cohérence (VERSION CORRIGÉE)
        print("🔍 Vérification de la cohérence des données...")
        
        total_journalier = df_appels_unique['TOTAL_APPELS_JOUR'].sum()
        total_hebdomadaire = df_hebdo['TOTAL_APPELS_SEMAINE'].sum()
        
        difference = abs(total_journalier - total_hebdomadaire)
        pourcentage_diff = (difference / total_journalier * 100) if total_journalier > 0 else 0
        
        if pourcentage_diff > 1:  # Tolérance de 1%
            print("⚠️ Avertissement : Incohérences détectées")
            print(f"  - Différence entre totaux journaliers ({total_journalier:,.0f}) et hebdomadaires ({total_hebdomadaire:,.0f}) : {pourcentage_diff:.2f}%")
        else:
            print(f"✅ Données cohérentes (différence : {pourcentage_diff:.2f}%)")
        
        # 7. Statistiques globales
        statistiques = {
            'nb_jours': len(df_appels_unique),
            'nb_semaines': len(df_hebdo),
            'total_appels': int(total_journalier),
            'moyenne_jour': float(df_appels_unique['TOTAL_APPELS_JOUR'].mean()),
            'moyenne_semaine': float(df_hebdo['TOTAL_APPELS_SEMAINE'].mean()) if len(df_hebdo) > 0 else 0,
            'date_min': df_appels_unique['DATE'].min(),
            'date_max': df_appels_unique['DATE'].max()
        }
        
        print(f"✅ Chargement terminé !")
        print(f"📊 {statistiques['nb_jours']} jours | {statistiques['nb_semaines']} semaines | {statistiques['total_appels']:,} appels")
        
        return {
            'appels': df_appels,  # Retourner le DataFrame ORIGINAL (avec potentiels doublons pour analyse)
            'calendrier': df_calendrier,
            'hebdomadaire': df_hebdo,
            'statistiques': statistiques
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement complet : {str(e)}")
        import traceback
        traceback.print_exc()
        raise

# ==============================================================================
# FONCTION 4 : VÉRIFICATION DE LA COHÉRENCE DES DONNÉES
# ==============================================================================

def verifier_coherence_donnees(df_appels, df_calendrier, df_hebdo):
    """
    Vérifie la cohérence entre les différentes sources de données.
    
    Args:
        df_appels (pd.DataFrame): Données journalières
        df_calendrier (pd.DataFrame): Calendrier épidémiologique
        df_hebdo (pd.DataFrame): Données hebdomadaires agrégées
    
    Returns:
        dict: Résultat de la vérification
    """
    messages = []
    details = {}
    
    # Vérification 1 : Doublons de dates
    doublons = df_appels[df_appels.duplicated(subset=['DATE'], keep=False)]
    if len(doublons) > 0:
        messages.append(f"{len(doublons)} lignes avec des dates en double détectées")
    
    details['doublons'] = len(doublons)
    
    # Vérification 2 : Cohérence des totaux
    df_appels_unique = df_appels.drop_duplicates(subset=['DATE'], keep='first')
    
    if len(df_hebdo) > 0:
        total_journalier = df_appels_unique['TOTAL_APPELS_JOUR'].sum()
        total_hebdo = df_hebdo['TOTAL_APPELS_SEMAINE'].sum()
        
        difference = abs(total_journalier - total_hebdo)
        pourcentage_diff = (difference / total_journalier * 100) if total_journalier > 0 else 0
        
        if pourcentage_diff > 1:
            messages.append(
                f"Différence entre totaux journaliers ({total_journalier:,.0f}) "
                f"et hebdomadaires ({total_hebdo:,.0f}) : {pourcentage_diff:.2f}%"
            )
        
        details['totaux'] = {
            'journalier': int(total_journalier),
            'hebdomadaire': int(total_hebdo),
            'difference': int(difference),
            'pourcentage': round(pourcentage_diff, 2)
        }
    
    # Vérification 3 : Valeurs négatives
    for col in settings.CATEGORIES_APPELS:
        if col in df_appels.columns:
            nb_negatifs = (df_appels[col] < 0).sum()
            if nb_negatifs > 0:
                messages.append(f"Colonne {col} : {nb_negatifs} valeurs négatives détectées")
    
    # Résultat final
    valide = len(messages) == 0
    
    return {
        'valide': valide,
        'messages': messages,
        'details': details
    }

# ==============================================================================
# FONCTION 5 : DÉTECTION AUTOMATIQUE DES FICHIERS
# ==============================================================================

def detecter_fichiers_data(data_dir=None):
    """
    Détecte automatiquement les fichiers Excel dans le dossier data/.
    
    Args:
        data_dir (str, optional): Chemin du dossier data.
    
    Returns:
        dict: Dictionnaire avec les chemins détectés
    """
    if data_dir is None:
        data_dir = settings.DATA_DIR
    else:
        data_dir = Path(data_dir)
    
    fichiers_detectes = {
        'appels': None,
        'calendrier': None,
        'tous_fichiers': []
    }
    
    if not data_dir.exists():
        print(f"⚠️ Le dossier {data_dir} n'existe pas")
        return fichiers_detectes
    
    # Lister tous les fichiers Excel
    excel_files = []
    for ext in ['.xlsx', '.xls']:
        excel_files.extend([
            f for f in data_dir.glob(f'*{ext}')
            if f.parent.name != 'backups' and 'backup' not in f.name.lower()
        ])
    
    fichiers_detectes['tous_fichiers'] = [str(f) for f in excel_files]
    
    # Mots-clés pour identifier les fichiers
    mots_cles_appels = ['appel', 'hebdo', 'jour', 'call', 'daily']
    mots_cles_calendrier = ['calendrier', 'calendar', 'epidemio', 'semaine', 'week', 'epi']
    
    # Recherche des fichiers
    for fichier in excel_files:
        nom_lower = fichier.name.lower()
        
        if not fichiers_detectes['appels']:
            for mot in mots_cles_appels:
                if mot in nom_lower:
                    fichiers_detectes['appels'] = str(fichier)
                    print(f"✅ Fichier des appels détecté : {fichier.name}")
                    break
        
        if not fichiers_detectes['calendrier']:
            for mot in mots_cles_calendrier:
                if mot in nom_lower:
                    fichiers_detectes['calendrier'] = str(fichier)
                    print(f"✅ Calendrier détecté : {fichier.name}")
                    break
    
    if excel_files:
        print(f"📂 {len(excel_files)} fichier(s) Excel trouvé(s) dans data/")
    
    return fichiers_detectes

# ==============================================================================
# FONCTION BONUS : MISE À JOUR DES CHEMINS
# ==============================================================================

def mettre_a_jour_chemins_config():
    """
    Met à jour automatiquement les chemins dans la configuration.
    
    Returns:
        bool: True si les chemins ont été mis à jour
    """
    fichiers = detecter_fichiers_data()
    
    mise_a_jour = False
    
    if fichiers['appels']:
        settings.CHEMINS_FICHIERS['appels'] = fichiers['appels']
        mise_a_jour = True
    
    if fichiers['calendrier']:
        settings.CHEMINS_FICHIERS['calendrier'] = fichiers['calendrier']
        mise_a_jour = True
    
    if mise_a_jour:
        print("✅ Chemins mis à jour dans la configuration")
    else:
        print("⚠️ Aucun fichier détecté, chemins non modifiés")
    
    return mise_a_jour

# ==============================================================================
# FIN DU MODULE
# ==============================================================================