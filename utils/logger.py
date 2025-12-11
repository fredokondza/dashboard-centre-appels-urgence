"""
==============================================================================
MODULE DE GESTION DES LOGS
==============================================================================
Ce module gère les logs de l'application avec rotation automatique des fichiers.

Fonctionnalités :
- Logs avec différents niveaux (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Rotation automatique des fichiers (10 MB max, 5 backups)
- Logs console + fichier simultanés
- Fonctions spécialisées pour chaque type d'opération
- Format standardisé avec timestamps

Fonctions principales :
- setup_logger() : Configuration du logger
- log_chargement_donnees() : Log chargement fichiers
- log_erreur() : Log erreurs avec traceback
- log_generation_rapport() : Log génération PowerPoint
- log_upload_fichier() : Log uploads
- log_export() : Log exports CSV/Excel

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 2.0
==============================================================================
"""

import logging
import sys
import traceback
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Import de la configuration
sys.path.append(str(Path(__file__).parent.parent))

from config import settings

# ==============================================================================
# VARIABLES GLOBALES
# ==============================================================================

# Dictionnaire pour stocker les loggers configurés
_loggers = {}

# ==============================================================================
# FONCTION 1 : CONFIGURATION DU LOGGER
# ==============================================================================

def setup_logger(name='dashboard', log_file=None, level=None, console_output=True):
    """
    Configure et retourne un logger avec rotation de fichiers.
    
    Cette fonction crée un logger qui :
    - Écrit dans un fichier avec rotation automatique (10 MB max, 5 backups)
    - Affiche également dans la console (optionnel)
    - Utilise un format standardisé avec timestamp
    
    Args:
        name (str): Nom du logger (ex: 'dashboard', 'data_loader', etc.)
        log_file (str, optional): Chemin du fichier de log.
            Si None, utilise settings.LOGGING_CONFIG['log_file']
        level (str, optional): Niveau de log ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
            Si None, utilise settings.LOGGING_CONFIG['level']
        console_output (bool): Si True, affiche aussi les logs dans la console
    
    Returns:
        logging.Logger: Logger configuré
    
    Example:
        >>> logger = setup_logger('mon_module')
        >>> logger.info("Application démarrée")
        >>> logger.error("Une erreur est survenue")
    """
    # Vérifier si le logger existe déjà
    if name in _loggers:
        return _loggers[name]
    
    # Créer le logger
    logger = logging.getLogger(name)
    
    # Éviter la duplication des handlers
    if logger.handlers:
        return logger
    
    # Définir le niveau de log
    if level is None:
        level = settings.LOGGING_CONFIG.get('level', 'INFO')
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Créer le format des logs
    log_format = settings.LOGGING_CONFIG.get(
        'format',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    date_format = settings.LOGGING_CONFIG.get('date_format', '%Y-%m-%d %H:%M:%S')
    formatter = logging.Formatter(log_format, datefmt=date_format)
    
    # === HANDLER FICHIER avec ROTATION ===
    if log_file is None:
        log_file = settings.LOGGING_CONFIG.get('log_file', str(settings.LOGS_DIR / 'dashboard.log'))
    
    # Créer le dossier logs si nécessaire
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configurer la rotation (10 MB max, 5 backups)
    max_bytes = settings.LOGGING_CONFIG.get('max_bytes', 10 * 1024 * 1024)  # 10 MB
    backup_count = settings.LOGGING_CONFIG.get('backup_count', 5)
    encoding = settings.LOGGING_CONFIG.get('encoding', 'utf-8')
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # === HANDLER CONSOLE (optionnel) ===
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Éviter la propagation aux loggers parents
    logger.propagate = False
    
    # Stocker le logger
    _loggers[name] = logger
    
    # Log de démarrage
    logger.info(f"Logger '{name}' initialisé - Niveau: {level}")
    
    return logger

# ==============================================================================
# FONCTION 2 : LOG CHARGEMENT DE DONNÉES
# ==============================================================================

def log_chargement_donnees(fichier, nb_lignes=None, success=True, message=None, logger_name='data_loader'):
    """
    Log le chargement d'un fichier de données.
    
    Args:
        fichier (str): Nom ou chemin du fichier chargé
        nb_lignes (int, optional): Nombre de lignes chargées
        success (bool): Si True, log en INFO, sinon en ERROR
        message (str, optional): Message personnalisé
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_chargement_donnees('Appels_hebdomadaires.xlsx', nb_lignes=365, success=True)
        2025-12-04 14:30:25 - data_loader - INFO - ✅ Chargement réussi : Appels_hebdomadaires.xlsx (365 lignes)
    """
    logger = setup_logger(logger_name)
    
    # Extraire juste le nom du fichier si c'est un chemin complet
    nom_fichier = Path(fichier).name if fichier else 'fichier inconnu'
    
    if success:
        if message:
            log_message = message
        else:
            if nb_lignes is not None:
                log_message = f"✅ Chargement réussi : {nom_fichier} ({nb_lignes} lignes)"
            else:
                log_message = f"✅ Chargement réussi : {nom_fichier}"
        
        logger.info(log_message)
    else:
        if message:
            log_message = message
        else:
            log_message = f"❌ Échec du chargement : {nom_fichier}"
        
        logger.error(log_message)

# ==============================================================================
# FONCTION 3 : LOG ERREUR AVEC TRACEBACK
# ==============================================================================

def log_erreur(source, message, exception=None, logger_name='dashboard'):
    """
    Log une erreur avec le traceback complet.
    
    Args:
        source (str): Source de l'erreur (nom de la fonction, module, etc.)
        message (str): Message d'erreur descriptif
        exception (Exception, optional): Exception Python capturée
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> try:
        >>>     result = 1 / 0
        >>> except Exception as e:
        >>>     log_erreur('calcul_statistiques', 'Division par zéro', exception=e)
    """
    logger = setup_logger(logger_name)
    
    log_message = f"❌ ERREUR [{source}] : {message}"
    
    if exception:
        # Log l'erreur avec l'exception
        logger.error(log_message, exc_info=True)
        
        # Log également le traceback complet
        tb_str = ''.join(traceback.format_exception(
            type(exception), 
            exception, 
            exception.__traceback__
        ))
        logger.debug(f"Traceback complet:\n{tb_str}")
    else:
        logger.error(log_message)

# ==============================================================================
# FONCTION 4 : LOG GÉNÉRATION DE RAPPORT POWERPOINT
# ==============================================================================

def log_generation_rapport(modele, nb_slides=None, success=True, duree=None, message=None, logger_name='pptx_generator'):
    """
    Log la génération d'un rapport PowerPoint.
    
    Args:
        modele (str): Type de modèle ('ORIGINAL', 'A', 'B')
        nb_slides (int, optional): Nombre de slides générées
        success (bool): Si True, log en INFO, sinon en ERROR
        duree (float, optional): Durée de génération en secondes
        message (str, optional): Message personnalisé
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_generation_rapport('A', nb_slides=16, success=True, duree=25.3)
        2025-12-04 14:35:10 - pptx_generator - INFO - ✅ Rapport Modèle A généré : 16 slides en 25.3s
    """
    logger = setup_logger(logger_name)
    
    if success:
        if message:
            log_message = message
        else:
            parts = [f"✅ Rapport Modèle {modele} généré"]
            
            if nb_slides is not None:
                parts.append(f": {nb_slides} slides")
            
            if duree is not None:
                parts.append(f" en {duree:.1f}s")
            
            log_message = ''.join(parts)
        
        logger.info(log_message)
    else:
        if message:
            log_message = message
        else:
            log_message = f"❌ Échec de la génération du rapport Modèle {modele}"
        
        logger.error(log_message)

# ==============================================================================
# FONCTION 5 : LOG UPLOAD DE FICHIER
# ==============================================================================

def log_upload_fichier(nom_fichier, taille=None, success=True, type_fichier=None, message=None, logger_name='upload'):
    """
    Log l'upload d'un fichier par l'utilisateur.
    
    Args:
        nom_fichier (str): Nom du fichier uploadé
        taille (int, optional): Taille du fichier en octets
        success (bool): Si True, log en INFO, sinon en ERROR
        type_fichier (str, optional): Type de fichier ('appels', 'calendrier', etc.)
        message (str, optional): Message personnalisé
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_upload_fichier('nouveaux_appels.xlsx', taille=524288, success=True, type_fichier='appels')
        2025-12-04 14:40:15 - upload - INFO - ✅ Upload réussi : nouveaux_appels.xlsx (512.0 KB) - Type: appels
    """
    logger = setup_logger(logger_name)
    
    if success:
        if message:
            log_message = message
        else:
            parts = [f"✅ Upload réussi : {nom_fichier}"]
            
            if taille is not None:
                # Convertir en unité lisible
                if taille < 1024:
                    taille_str = f"{taille} B"
                elif taille < 1024 * 1024:
                    taille_str = f"{taille / 1024:.1f} KB"
                else:
                    taille_str = f"{taille / (1024 * 1024):.1f} MB"
                
                parts.append(f" ({taille_str})")
            
            if type_fichier:
                parts.append(f" - Type: {type_fichier}")
            
            log_message = ''.join(parts)
        
        logger.info(log_message)
    else:
        if message:
            log_message = message
        else:
            log_message = f"❌ Échec de l'upload : {nom_fichier}"
        
        logger.error(log_message)

# ==============================================================================
# FONCTION 6 : LOG EXPORT DE DONNÉES
# ==============================================================================

def log_export(format_export, nb_lignes=None, destination=None, success=True, message=None, logger_name='export'):
    """
    Log l'export de données (CSV, Excel, etc.).
    
    Args:
        format_export (str): Format d'export ('CSV', 'Excel', 'PDF', etc.)
        nb_lignes (int, optional): Nombre de lignes exportées
        destination (str, optional): Nom du fichier de destination
        success (bool): Si True, log en INFO, sinon en ERROR
        message (str, optional): Message personnalisé
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_export('CSV', nb_lignes=365, destination='donnees_2025.csv', success=True)
        2025-12-04 14:45:20 - export - INFO - ✅ Export CSV réussi : 365 lignes → donnees_2025.csv
    """
    logger = setup_logger(logger_name)
    
    if success:
        if message:
            log_message = message
        else:
            parts = [f"✅ Export {format_export} réussi"]
            
            if nb_lignes is not None:
                parts.append(f" : {nb_lignes} lignes")
            
            if destination:
                parts.append(f" → {destination}")
            
            log_message = ''.join(parts)
        
        logger.info(log_message)
    else:
        if message:
            log_message = message
        else:
            log_message = f"❌ Échec de l'export {format_export}"
        
        logger.error(log_message)

# ==============================================================================
# FONCTION BONUS 1 : LOG AGRÉGATION
# ==============================================================================

def log_aggregation(type_aggregation, nb_lignes_in, nb_lignes_out, duree=None, logger_name='data_processor'):
    """
    Log une opération d'agrégation de données.
    
    Args:
        type_aggregation (str): Type d'agrégation ('hebdomadaire', 'mensuelle', etc.)
        nb_lignes_in (int): Nombre de lignes en entrée
        nb_lignes_out (int): Nombre de lignes en sortie
        duree (float, optional): Durée en secondes
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_aggregation('hebdomadaire', nb_lignes_in=365, nb_lignes_out=52, duree=0.5)
        2025-12-04 14:50:00 - data_processor - INFO - 📊 Agrégation hebdomadaire : 365 → 52 lignes (0.5s)
    """
    logger = setup_logger(logger_name)
    
    parts = [f"📊 Agrégation {type_aggregation} : {nb_lignes_in} → {nb_lignes_out} lignes"]
    
    if duree is not None:
        parts.append(f" ({duree:.1f}s)")
    
    log_message = ''.join(parts)
    logger.info(log_message)

# ==============================================================================
# FONCTION BONUS 2 : LOG SESSION UTILISATEUR
# ==============================================================================

def log_session(action, details=None, logger_name='session'):
    """
    Log les actions de session utilisateur.
    
    Args:
        action (str): Type d'action ('start', 'page_change', 'end', etc.)
        details (dict, optional): Détails supplémentaires
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_session('start', details={'ip': '192.168.1.1'})
        >>> log_session('page_change', details={'page': 'Vue d\'Ensemble'})
    """
    logger = setup_logger(logger_name)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if action == 'start':
        log_message = f"🚀 Session démarrée - {timestamp}"
    elif action == 'page_change':
        page = details.get('page', 'Inconnue') if details else 'Inconnue'
        log_message = f"📄 Navigation : {page}"
    elif action == 'end':
        log_message = f"🏁 Session terminée - {timestamp}"
    else:
        log_message = f"📌 Action : {action}"
    
    if details and action != 'page_change':
        log_message += f" - Détails: {details}"
    
    logger.info(log_message)

# ==============================================================================
# FONCTION BONUS 3 : LOG PERFORMANCE
# ==============================================================================

def log_performance(operation, duree, nb_elements=None, logger_name='performance'):
    """
    Log les performances d'une opération.
    
    Args:
        operation (str): Nom de l'opération
        duree (float): Durée en secondes
        nb_elements (int, optional): Nombre d'éléments traités
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_performance('chargement_donnees', duree=2.5, nb_elements=10000)
        2025-12-04 15:00:00 - performance - INFO - ⚡ chargement_donnees : 2.5s (10000 éléments)
    """
    logger = setup_logger(logger_name)
    
    parts = [f"⚡ {operation} : {duree:.2f}s"]
    
    if nb_elements is not None:
        parts.append(f" ({nb_elements} éléments)")
        
        # Calculer le débit si possible
        if duree > 0:
            debit = nb_elements / duree
            parts.append(f" - {debit:.0f} éléments/s")
    
    log_message = ''.join(parts)
    
    # WARNING si trop lent
    if duree > 10:
        logger.warning(log_message + " ⚠️ LENT")
    else:
        logger.info(log_message)

# ==============================================================================
# FONCTION BONUS 4 : LOG VALIDATION
# ==============================================================================

def log_validation(type_validation, resultat, nb_erreurs=0, details=None, logger_name='validation'):
    """
    Log les résultats de validation des données.
    
    Args:
        type_validation (str): Type de validation
        resultat (bool): True si validation réussie
        nb_erreurs (int): Nombre d'erreurs détectées
        details (list, optional): Liste des erreurs
        logger_name (str): Nom du logger à utiliser
    
    Example:
        >>> log_validation('coherence_donnees', resultat=False, nb_erreurs=3, 
        ...                details=['Doublons détectés', 'Valeurs négatives', 'Dates manquantes'])
    """
    logger = setup_logger(logger_name)
    
    if resultat:
        log_message = f"✅ Validation {type_validation} : OK"
        logger.info(log_message)
    else:
        log_message = f"⚠️ Validation {type_validation} : {nb_erreurs} erreur(s) détectée(s)"
        logger.warning(log_message)
        
        if details:
            for i, erreur in enumerate(details, 1):
                logger.warning(f"  {i}. {erreur}")

# ==============================================================================
# FONCTION UTILITAIRE : NETTOYER LES VIEUX LOGS
# ==============================================================================

def nettoyer_vieux_logs(jours_retention=30, logger_name='dashboard'):
    """
    Supprime les fichiers de logs plus vieux que X jours.
    
    Args:
        jours_retention (int): Nombre de jours à conserver
        logger_name (str): Nom du logger à utiliser
    
    Returns:
        int: Nombre de fichiers supprimés
    
    Example:
        >>> nb_supprimes = nettoyer_vieux_logs(jours_retention=30)
        >>> print(f"{nb_supprimes} fichiers de logs supprimés")
    """
    logger = setup_logger(logger_name)
    
    try:
        logs_dir = settings.LOGS_DIR
        if not logs_dir.exists():
            return 0
        
        date_limite = datetime.now() - timedelta(days=jours_retention)
        nb_supprimes = 0
        
        for fichier in logs_dir.glob('*.log*'):
            # Vérifier la date de modification
            timestamp = fichier.stat().st_mtime
            date_fichier = datetime.fromtimestamp(timestamp)
            
            if date_fichier < date_limite:
                fichier.unlink()
                nb_supprimes += 1
                logger.info(f"🗑️ Log supprimé : {fichier.name}")
        
        if nb_supprimes > 0:
            logger.info(f"✅ Nettoyage terminé : {nb_supprimes} fichier(s) supprimé(s)")
        
        return nb_supprimes
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du nettoyage des logs : {str(e)}")
        return 0

# ==============================================================================
# FONCTION UTILITAIRE : OBTENIR STATISTIQUES DES LOGS
# ==============================================================================

def obtenir_stats_logs(logger_name='dashboard'):
    """
    Retourne des statistiques sur les fichiers de logs.
    
    Args:
        logger_name (str): Nom du logger
    
    Returns:
        dict: Statistiques des logs
    
    Example:
        >>> stats = obtenir_stats_logs()
        >>> print(f"Taille totale : {stats['taille_totale_mb']:.2f} MB")
    """
    logger = setup_logger(logger_name)
    
    try:
        logs_dir = settings.LOGS_DIR
        if not logs_dir.exists():
            return {'nb_fichiers': 0, 'taille_totale_mb': 0}
        
        fichiers_logs = list(logs_dir.glob('*.log*'))
        nb_fichiers = len(fichiers_logs)
        
        taille_totale = sum(f.stat().st_size for f in fichiers_logs)
        taille_totale_mb = taille_totale / (1024 * 1024)
        
        stats = {
            'nb_fichiers': nb_fichiers,
            'taille_totale_mb': round(taille_totale_mb, 2),
            'fichiers': [f.name for f in fichiers_logs]
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des stats : {str(e)}")
        return {'nb_fichiers': 0, 'taille_totale_mb': 0}

# ==============================================================================
# FIN DU MODULE
# ==============================================================================