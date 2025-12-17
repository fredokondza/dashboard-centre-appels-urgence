"""
==============================================================================
MODULE DE TRAITEMENT DES DONNÉES - VERSION CORRIGÉE
==============================================================================
Ce module gère le traitement, l'agrégation et les calculs statistiques
des données pour le Dashboard Centre d'Appels d'Urgence.

CORRECTION v2.2 :
- comparer_periodes() : Affiche par REGROUPEMENTS au lieu de par catégories
  Résultat : 6 lignes (5 regroupements + TOTAL) au lieu de 18 lignes

Fonctions principales :
- calculer_totaux_hebdomadaires() : Agrégation par semaine
- calculer_totaux_semaine() : Totaux d'une semaine spécifique
- calculer_variations() : Variations entre périodes
- calculer_regroupements() : Agrégation par thématiques
- obtenir_statistiques_globales() : Stats descriptives
- regrouper_par_mois() : Conversion semaines → mois
- calculer_top_categories() : Top N des catégories
- comparer_periodes() : Comparaison multi-périodes [CORRIGÉE]

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: 17 Décembre 2025
Version: 2.2 - Correction comparer_periodes (regroupements)
==============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Import de la configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import settings
from utils.helpers import extraire_numero_semaine

# ==============================================================================
# FONCTION 1 : AGRÉGATION HEBDOMADAIRE
# ==============================================================================

def calculer_totaux_hebdomadaires(df_appels):
    """
    Agrège les données journalières par semaine épidémiologique.
    
    Cette fonction :
    - Groupe les données par semaine épidémiologique
    - Somme les appels de chaque catégorie sur les 7 jours
    - Calcule le total hebdomadaire
    - Trie les semaines par ordre chronologique
    
    Args:
        df_appels (pd.DataFrame): DataFrame des appels journaliers
            Doit contenir :
            - 'Semaine épidémiologique' (str)
            - Colonnes des catégories d'appels
    
    Returns:
        pd.DataFrame: DataFrame agrégé avec :
            - 'Semaine épidémiologique' (str)
            - 'TOTAL_APPELS_SEMAINE' (int)
            - [17 catégories]_SEMAINE (int)
    
    Example:
        >>> df_hebdo = calculer_totaux_hebdomadaires(df_appels)
        >>> print(df_hebdo.shape)
        (52, 19)
    """
    try:
        # Vérifier la présence de la colonne semaine
        if 'Semaine épidémiologique' not in df_appels.columns:
            raise ValueError("Colonne 'Semaine épidémiologique' manquante")
        
        # Identifier les colonnes de catégories présentes
        colonnes_categories = [
            col for col in settings.CATEGORIES_APPELS 
            if col in df_appels.columns
        ]
        
        if not colonnes_categories:
            raise ValueError("Aucune catégorie d'appels trouvée dans le DataFrame")
        
        # Grouper par semaine et sommer
        df_hebdo = df_appels.groupby('Semaine épidémiologique')[colonnes_categories].sum().reset_index()
        
        # Renommer les colonnes : _JOUR → _SEMAINE
        colonnes_renommees = {
            col: col.replace('_JOUR', '_SEMAINE') 
            for col in colonnes_categories
        }
        df_hebdo = df_hebdo.rename(columns=colonnes_renommees)
        
        # Calculer le total hebdomadaire
        colonnes_semaine = [col.replace('_JOUR', '_SEMAINE') for col in colonnes_categories]
        df_hebdo['TOTAL_APPELS_SEMAINE'] = df_hebdo[colonnes_semaine].sum(axis=1)
        
        # Trier par numéro de semaine
        df_hebdo['_sort_key'] = df_hebdo['Semaine épidémiologique'].apply(extraire_numero_semaine)
        df_hebdo = df_hebdo.sort_values('_sort_key').drop('_sort_key', axis=1).reset_index(drop=True)
        
        print(f"✅ Agrégation hebdomadaire : {len(df_hebdo)} semaines")
        print(f"📊 Total général : {df_hebdo['TOTAL_APPELS_SEMAINE'].sum():,} appels".replace(',', ' '))
        
        return df_hebdo
        
    except Exception as e:
        print(f"❌ Erreur lors de l'agrégation hebdomadaire : {str(e)}")
        raise

# ==============================================================================
# FONCTION 2 : TOTAUX D'UNE SEMAINE SPÉCIFIQUE
# ==============================================================================

def calculer_totaux_semaine(df_appels, semaine):
    """
    Calcule les totaux pour une semaine épidémiologique spécifique.
    
    Args:
        df_appels (pd.DataFrame): DataFrame des appels journaliers
        semaine (str): Label de la semaine (ex: 'S10_2025')
    
    Returns:
        dict: Dictionnaire contenant :
            - 'semaine' (str) : Label de la semaine
            - 'total' (int) : Total des appels
            - 'categories' (dict) : Total par catégorie
            - 'regroupements' (dict) : Total par regroupement thématique
            - 'nb_jours' (int) : Nombre de jours dans la semaine
            - 'moyenne_jour' (float) : Moyenne par jour
    
    Raises:
        ValueError: Si la semaine n'existe pas dans les données
    
    Example:
        >>> totaux = calculer_totaux_semaine(df_appels, 'S10_2025')
        >>> print(totaux['total'])
        1250
    """
    try:
        # Filtrer les données de la semaine
        df_semaine = df_appels[df_appels['Semaine épidémiologique'] == semaine]
        
        if len(df_semaine) == 0:
            raise ValueError(f"Aucune donnée trouvée pour la semaine {semaine}")
        
        # Calculer le total
        total = int(df_semaine['TOTAL_APPELS_JOUR'].sum())
        
        # Calculer par catégorie
        categories = {}
        for categorie in settings.CATEGORIES_APPELS:
            if categorie in df_semaine.columns:
                valeur = int(df_semaine[categorie].sum())
                if valeur > 0:  # Ne garder que les catégories non nulles
                    label = settings.LABELS_CATEGORIES.get(categorie, categorie)
                    categories[label] = valeur
        
        # Calculer par regroupement
        regroupements = calculer_regroupements(df_semaine)
        
        # Statistiques complémentaires
        nb_jours = len(df_semaine)
        moyenne_jour = total / nb_jours if nb_jours > 0 else 0
        
        resultat = {
            'semaine': semaine,
            'total': total,
            'categories': categories,
            'regroupements': regroupements,
            'nb_jours': nb_jours,
            'moyenne_jour': round(moyenne_jour, 2),
            'date_debut': df_semaine['DATE'].min() if 'DATE' in df_semaine.columns else None,
            'date_fin': df_semaine['DATE'].max() if 'DATE' in df_semaine.columns else None
        }
        
        return resultat
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des totaux : {str(e)}")
        raise

# ==============================================================================
# FONCTION 3 : CALCUL DES VARIATIONS
# ==============================================================================

def calculer_variations(df_appels, semaine_actuelle, semaine_precedente):
    """
    Calcule les variations entre deux semaines épidémiologiques.
    
    Args:
        df_appels (pd.DataFrame): DataFrame des appels journaliers
        semaine_actuelle (str): Semaine de référence
        semaine_precedente (str): Semaine à comparer
    
    Returns:
        dict: Dictionnaire contenant :
            - 'total_actuel' (int)
            - 'total_precedent' (int)
            - 'variation_absolue' (int)
            - 'variation_relative' (float) : En pourcentage
            - 'tendance' (str) : 'hausse', 'baisse' ou 'stable'
            - 'categories' (dict) : Variations par catégorie
            - 'regroupements' (dict) : Variations par regroupement
    
    Example:
        >>> variations = calculer_variations(df, 'S10_2025', 'S9_2025')
        >>> print(f"Variation : {variations['variation_relative']:.1f}%")
        Variation : +15.3%
    """
    try:
        # Calculer les totaux des deux semaines
        totaux_actuel = calculer_totaux_semaine(df_appels, semaine_actuelle)
        totaux_precedent = calculer_totaux_semaine(df_appels, semaine_precedente)
        
        # Variation totale
        total_actuel = totaux_actuel['total']
        total_precedent = totaux_precedent['total']
        variation_abs = total_actuel - total_precedent
        variation_rel = (variation_abs / total_precedent * 100) if total_precedent != 0 else 0
        
        # Déterminer la tendance
        if abs(variation_rel) < 2:  # Moins de 2% = stable
            tendance = 'stable'
        elif variation_rel > 0:
            tendance = 'hausse'
        else:
            tendance = 'baisse'
        
        # Variations par catégorie
        variations_categories = {}
        for categorie in settings.CATEGORIES_APPELS:
            label = settings.LABELS_CATEGORIES.get(categorie, categorie)
            
            val_actuel = totaux_actuel['categories'].get(label, 0)
            val_precedent = totaux_precedent['categories'].get(label, 0)
            
            if val_actuel > 0 or val_precedent > 0:  # Au moins une valeur non nulle
                var_abs = val_actuel - val_precedent
                var_rel = (var_abs / val_precedent * 100) if val_precedent != 0 else 100
                
                variations_categories[label] = {
                    'actuel': val_actuel,
                    'precedent': val_precedent,
                    'variation_absolue': var_abs,
                    'variation_relative': round(var_rel, 2)
                }
        
        # Variations par regroupement
        variations_regroupements = {}
        for groupe in settings.REGROUPEMENTS.keys():
            label_groupe = settings.LABELS_REGROUPEMENTS.get(groupe, groupe)
            
            val_actuel = totaux_actuel['regroupements'].get(label_groupe, 0)
            val_precedent = totaux_precedent['regroupements'].get(label_groupe, 0)
            
            if val_actuel > 0 or val_precedent > 0:
                var_abs = val_actuel - val_precedent
                var_rel = (var_abs / val_precedent * 100) if val_precedent != 0 else 100
                
                variations_regroupements[label_groupe] = {
                    'actuel': val_actuel,
                    'precedent': val_precedent,
                    'variation_absolue': var_abs,
                    'variation_relative': round(var_rel, 2)
                }
        
        resultat = {
            'semaine_actuelle': semaine_actuelle,
            'semaine_precedente': semaine_precedente,
            'total_actuel': total_actuel,
            'total_precedent': total_precedent,
            'variation_absolue': variation_abs,
            'variation_relative': round(variation_rel, 2),
            'tendance': tendance,
            'categories': variations_categories,
            'regroupements': variations_regroupements
        }
        
        return resultat
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des variations : {str(e)}")
        raise

# ==============================================================================
# FONCTION 4 : REGROUPEMENTS THÉMATIQUES
# ==============================================================================

def calculer_regroupements(df_data):
    """
    Calcule les totaux par regroupement thématique.
    
    Les 5 regroupements définis dans la configuration :
    - Renseignements Santé
    - Assistances Médicales
    - Assistances Psycho-Sociales
    - Signaux d'Alerte
    - Autres Appels
    
    Args:
        df_data (pd.DataFrame): DataFrame (journalier ou filtré)
    
    Returns:
        dict: Totaux par regroupement
            Clé : Label du regroupement
            Valeur : Total des appels
    
    Example:
        >>> regroupements = calculer_regroupements(df_appels)
        >>> print(regroupements['Renseignements Santé'])
        450
    """
    try:
        regroupements_totaux = {}
        
        for groupe, categories in settings.REGROUPEMENTS.items():
            # Filtrer les catégories présentes dans le DataFrame
            categories_existantes = [
                cat for cat in categories 
                if cat in df_data.columns
            ]
            
            # Calculer le total
            if categories_existantes:
                total = int(df_data[categories_existantes].sum().sum())
            else:
                total = 0
            
            # Utiliser le label du regroupement
            label_groupe = settings.LABELS_REGROUPEMENTS.get(groupe, groupe)
            regroupements_totaux[label_groupe] = total
        
        return regroupements_totaux
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des regroupements : {str(e)}")
        raise

# ==============================================================================
# FONCTION 5 : STATISTIQUES GLOBALES
# ==============================================================================

def obtenir_statistiques_globales(df_appels, df_hebdo=None):
    """
    Calcule des statistiques descriptives globales.
    
    Args:
        df_appels (pd.DataFrame): Données journalières
        df_hebdo (pd.DataFrame, optional): Données hebdomadaires
    
    Returns:
        dict: Statistiques globales :
            - 'periode' : Période couverte
            - 'totaux' : Totaux par période
            - 'moyennes' : Moyennes par période
            - 'extremes' : Min/Max
            - 'tendance' : Tendance générale
            - 'top_categories' : Top 5 des catégories
            - 'repartition_regroupements' : Répartition par thématique
    
    Example:
        >>> stats = obtenir_statistiques_globales(df_appels, df_hebdo)
        >>> print(stats['totaux']['total'])
        15000
    """
    try:
        stats = {}
        
        # === PÉRIODE ===
        date_min = df_appels['DATE'].min()
        date_max = df_appels['DATE'].max()
        nb_jours = len(df_appels)
        
        stats['periode'] = {
            'date_debut': date_min,
            'date_fin': date_max,
            'nb_jours': nb_jours,
            'nb_semaines': df_appels['Semaine épidémiologique'].nunique()
        }
        
        # === TOTAUX ===
        total_general = int(df_appels['TOTAL_APPELS_JOUR'].sum())
        
        stats['totaux'] = {
            'total': total_general,
            'par_jour': int(df_appels['TOTAL_APPELS_JOUR'].sum()),
            'par_semaine': int(df_hebdo['TOTAL_APPELS_SEMAINE'].sum()) if df_hebdo is not None else total_general
        }
        
        # === MOYENNES ===
        stats['moyennes'] = {
            'jour': round(df_appels['TOTAL_APPELS_JOUR'].mean(), 2),
            'semaine': round(df_hebdo['TOTAL_APPELS_SEMAINE'].mean(), 2) if df_hebdo is not None else 0
        }
        
        # === EXTREMES ===
        stats['extremes'] = {
            'min_jour': int(df_appels['TOTAL_APPELS_JOUR'].min()),
            'max_jour': int(df_appels['TOTAL_APPELS_JOUR'].max()),
            'min_semaine': int(df_hebdo['TOTAL_APPELS_SEMAINE'].min()) if df_hebdo is not None else 0,
            'max_semaine': int(df_hebdo['TOTAL_APPELS_SEMAINE'].max()) if df_hebdo is not None else 0
        }
        
        # === TENDANCE ===
        if df_hebdo is not None and len(df_hebdo) > 1:
            premiere_semaine = df_hebdo.iloc[0]['TOTAL_APPELS_SEMAINE']
            derniere_semaine = df_hebdo.iloc[-1]['TOTAL_APPELS_SEMAINE']
            variation = ((derniere_semaine - premiere_semaine) / premiere_semaine * 100) if premiere_semaine != 0 else 0
            
            if abs(variation) < 5:
                tendance_label = 'stable'
            elif variation > 0:
                tendance_label = 'croissante'
            else:
                tendance_label = 'décroissante'
            
            stats['tendance'] = {
                'label': tendance_label,
                'variation': round(variation, 2),
                'premiere_valeur': int(premiere_semaine),
                'derniere_valeur': int(derniere_semaine)
            }
        
        # === TOP CATÉGORIES ===
        top_categories = []
        for categorie in settings.CATEGORIES_APPELS:
            if categorie in df_appels.columns:
                total = int(df_appels[categorie].sum())
                if total > 0:
                    label = settings.LABELS_CATEGORIES.get(categorie, categorie)
                    pourcentage = (total / total_general * 100) if total_general > 0 else 0
                    top_categories.append({
                        'categorie': label,
                        'total': total,
                        'pourcentage': round(pourcentage, 2)
                    })
        
        # Trier par total décroissant et garder le top 5
        top_categories = sorted(top_categories, key=lambda x: x['total'], reverse=True)[:5]
        stats['top_categories'] = top_categories
        
        # === RÉPARTITION PAR REGROUPEMENTS ===
        regroupements = calculer_regroupements(df_appels)
        repartition = {}
        
        for groupe, total in regroupements.items():
            pourcentage = (total / total_general * 100) if total_general > 0 else 0
            repartition[groupe] = {
                'total': total,
                'pourcentage': round(pourcentage, 2)
            }
        
        stats['repartition_regroupements'] = repartition
        
        return stats
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des statistiques : {str(e)}")
        raise

# ==============================================================================
# FONCTION 6 : REGROUPEMENT PAR MOIS
# ==============================================================================

def regrouper_par_mois(df_hebdo):
    """
    Regroupe les données hebdomadaires par mois.
    
    Conversion basée sur une approximation :
    - Semaines 1-4 : Janvier
    - Semaines 5-8 : Février
    - etc.
    
    Args:
        df_hebdo (pd.DataFrame): Données hebdomadaires
    
    Returns:
        pd.DataFrame: Données mensuelles avec :
            - 'Mois' (str)
            - 'TOTAL_APPELS_SEMAINE' (int) : Total du mois
            - Colonnes des catégories
    
    Example:
        >>> df_mois = regrouper_par_mois(df_hebdo)
        >>> print(df_mois.shape)
        (12, 19)
    """
    try:
        # Copier le DataFrame
        df = df_hebdo.copy()
        
        # Extraire le numéro de semaine
        df['num_semaine'] = df['Semaine épidémiologique'].apply(extraire_numero_semaine)
        
        # Fonction de conversion semaine → mois
        def semaine_to_mois(num_semaine):
            """Convertit un numéro de semaine en nom de mois (approximation)."""
            if num_semaine <= 4:
                return "Janvier"
            elif num_semaine <= 8:
                return "Février"
            elif num_semaine <= 13:
                return "Mars"
            elif num_semaine <= 17:
                return "Avril"
            elif num_semaine <= 22:
                return "Mai"
            elif num_semaine <= 26:
                return "Juin"
            elif num_semaine <= 30:
                return "Juillet"
            elif num_semaine <= 35:
                return "Août"
            elif num_semaine <= 39:
                return "Septembre"
            elif num_semaine <= 43:
                return "Octobre"
            elif num_semaine <= 48:
                return "Novembre"
            else:
                return "Décembre"
        
        # Appliquer la conversion
        df['Mois'] = df['num_semaine'].apply(semaine_to_mois)
        
        # Identifier les colonnes à sommer
        colonnes_a_sommer = ['TOTAL_APPELS_SEMAINE']
        for categorie in settings.CATEGORIES_APPELS:
            col_semaine = categorie.replace('_JOUR', '_SEMAINE')
            if col_semaine in df.columns:
                colonnes_a_sommer.append(col_semaine)
        
        # Grouper par mois
        df_mois = df.groupby('Mois')[colonnes_a_sommer].sum().reset_index()
        
        # Ordonner les mois
        ordre_mois = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        
        df_mois['ordre'] = df_mois['Mois'].apply(
            lambda x: ordre_mois.index(x) if x in ordre_mois else 99
        )
        df_mois = df_mois.sort_values('ordre').drop('ordre', axis=1).reset_index(drop=True)
        
        print(f"✅ Regroupement mensuel : {len(df_mois)} mois")
        
        return df_mois
        
    except Exception as e:
        print(f"❌ Erreur lors du regroupement par mois : {str(e)}")
        raise

# ==============================================================================
# FONCTION 7 : TOP CATÉGORIES
# ==============================================================================

def calculer_top_categories(df_data, nb_top=10):
    """
    Calcule le top N des catégories d'appels.
    
    Args:
        df_data (pd.DataFrame): DataFrame (journalier ou filtré)
        nb_top (int): Nombre de catégories à retourner (défaut: 10)
    
    Returns:
        dict: Dictionnaire {label_categorie: total}
              Trié par ordre décroissant
    
    Example:
        >>> top_10 = calculer_top_categories(df_appels, nb_top=10)
        >>> print(top_10)
        {'Urgences Médicales': 450, 'CSU': 320, ...}
    """
    try:
        categories_totaux = {}
        
        for categorie in settings.CATEGORIES_APPELS:
            if categorie in df_data.columns:
                total = int(df_data[categorie].sum())
                
                if total > 0:
                    # Récupérer le label depuis settings
                    label = settings.LABELS_CATEGORIES.get(categorie, categorie)
                    categories_totaux[label] = total
        
        # Trier par valeur décroissante et prendre le top N
        top_categories = dict(
            sorted(categories_totaux.items(), key=lambda x: x[1], reverse=True)[:nb_top]
        )
        
        return top_categories
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul du top catégories : {str(e)}")
        raise

# ==============================================================================
# FONCTION 8 : COMPARAISON MULTI-PÉRIODES [CORRIGÉE]
# ==============================================================================

def comparer_periodes(df_appels, liste_semaines):
    """
    Compare plusieurs semaines simultanément.
    VERSION CORRIGÉE v2.2 : Affiche par REGROUPEMENTS au lieu de par catégories.
    
    Args:
        df_appels (pd.DataFrame): Données journalières
        liste_semaines (list): Liste des semaines à comparer
    
    Returns:
        pd.DataFrame: Tableau comparatif avec :
            - Une ligne par regroupement (5 lignes au lieu de 17)
            - Une colonne par semaine
            - Une ligne TOTAL
    
    Example:
        >>> df_comp = comparer_periodes(df, ['S46_2025', 'S47_2025'])
        >>> print(df_comp)
        # Résultat : 6 lignes (5 regroupements + TOTAL)
        #   1. Renseignements Santé
        #   2. Assistances Médicales
        #   3. Assistances Psycho-Sociales
        #   4. Signaux d'Alerte
        #   5. Autres Appels
        #   6. TOTAL
    """
    try:
        donnees_comparaison = []
        
        # ✅ CORRECTION : Boucler sur les REGROUPEMENTS (au lieu des catégories)
        for nom_groupe, categories in settings.REGROUPEMENTS.items():
            ligne = {
                'Catégorie': settings.LABELS_REGROUPEMENTS.get(nom_groupe, nom_groupe)
            }
            
            # Pour chaque semaine
            for semaine in liste_semaines:
                df_sem = df_appels[df_appels['Semaine épidémiologique'] == semaine]
                
                # Sommer toutes les catégories du regroupement
                total = 0
                for categorie in categories:
                    if categorie in df_sem.columns:
                        total += int(df_sem[categorie].sum())
                
                ligne[semaine] = total
            
            donnees_comparaison.append(ligne)
        
        # Créer le DataFrame
        df_comparaison = pd.DataFrame(donnees_comparaison)
        
        # Ajouter une ligne de totaux
        ligne_totaux = {'Catégorie': 'TOTAL'}
        for semaine in liste_semaines:
            ligne_totaux[semaine] = df_comparaison[semaine].sum()
        
        df_comparaison = pd.concat([
            df_comparaison,
            pd.DataFrame([ligne_totaux])
        ], ignore_index=True)
        
        print(f"✅ Comparaison : {len(df_comparaison)} lignes (5 regroupements + TOTAL)")
        
        return df_comparaison
        
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison : {str(e)}")
        raise

# ==============================================================================
# FIN DU MODULE
# ==============================================================================