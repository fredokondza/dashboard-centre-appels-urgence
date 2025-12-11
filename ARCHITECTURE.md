# 🏗️ Architecture Technique du Dashboard

> Documentation technique détaillée de l'architecture modulaire v2.0

---

## 📋 Table des Matières

- [Vue d'Ensemble](#-vue-densemble)
- [Principes Architecturaux](#-principes-architecturaux)
- [Structure des Modules](#-structure-des-modules)
- [Flux de Données](#-flux-de-données)
- [Système de Cache](#-système-de-cache)
- [Gestion des Logs](#-gestion-des-logs)
- [Composants Réutilisables](#-composants-réutilisables)
- [Patterns Utilisés](#-patterns-utilisés)
- [Performance](#-performance)
- [Sécurité](#-sécurité)
- [Évolutivité](#-évolutivité)

---

## 🎯 Vue d'Ensemble

### Architecture en 4 Couches

```
┌─────────────────────────────────────────────────────────────┐
│                    COUCHE PRÉSENTATION                       │
│                    (Streamlit Pages)                         │
│  app.py | Page 1 | Page 2 | Page 3 | Page 4 | Page 5       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   COUCHE COMPOSANTS                          │
│              (Components - Réutilisables)                    │
│    Layout | Metrics | Tables | Charts                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   COUCHE MÉTIER                              │
│                 (Utils - Logique)                            │
│  Data Loader | Data Processor | Helpers | Logger | Charts   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 COUCHE CONFIGURATION                         │
│                   (Config - Settings)                        │
│         Settings.py | Styles.css | Constants                │
└─────────────────────────────────────────────────────────────┘
```

### Statistiques de l'Architecture

| Métriques | Valeur |
|-----------|--------|
| **Modules principaux** | 4 (config, utils, components, pages) |
| **Fichiers Python** | 21 |
| **Fonctions totales** | 120+ |
| **Lignes de code** | ~9,880 |
| **Taux de réutilisation** | 75% |
| **Réduction code pages** | -53% |

---

## 🎨 Principes Architecturaux

### 1. Séparation des Préoccupations (SoC)

Chaque module a une responsabilité unique :

- **Config** : Configuration et constantes
- **Utils** : Logique métier et traitement
- **Components** : Composants UI réutilisables
- **Pages** : Orchestration et présentation

### 2. DRY (Don't Repeat Yourself)

**Avant v2.0 :**
```python
# Répété dans 6 fichiers (850 lignes)
st.markdown("""
<style>
.main-title { /* ... */ }
.metric-card { /* ... */ }
/* ... 150 lignes de CSS ... */
</style>
""", unsafe_allow_html=True)
```

**Après v2.0 :**
```python
# Une seule fois
from components import apply_custom_css
apply_custom_css()  # Charge config/styles.css
```

**Économie : 850 → 0 lignes dupliquées (-100%)**

### 3. Single Source of Truth

Toutes les configurations dans `config/settings.py` :

```python
# Catégories centralisées
CATEGORIES_APPELS = [...]  # 1 seule définition

# Couleurs centralisées
COULEURS_CAMEROUN = {
    'vert': '#007A33',
    'jaune': '#FFD700',
    'rouge': '#CE1126'
}
```

### 4. Modularité et Réutilisabilité

**Taux de réutilisation : 75%**

```python
# Fonction utilisée dans 4+ pages
from utils import calculer_totaux_semaine

# Au lieu de répéter le calcul
totaux = calculer_totaux_semaine(df_appels, semaine)
```

### 5. Immutabilité des Données

```python
# Toujours copier avant modification
df_filtered = df_appels.copy()
df_filtered = df_filtered[condition]
```

---

## 📦 Structure des Modules

### Module 1 : `config/`

**Responsabilité** : Configuration centralisée

```
config/
├── __init__.py          # Exports simplifiés
├── settings.py          # 550 lignes - Toutes les configurations
└── styles.css           # 650 lignes - CSS centralisé
```

**Contenu de `settings.py` :**

```python
# Configuration application
APP_CONFIG = {
    'page_title': '...',
    'version': '2.0',
    'author': 'Fred',
    'organisation': 'AIMS / MINSANTE'
}

# Chemins automatiques (Path)
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# Catégories (17)
CATEGORIES_APPELS = ['CSU_JOUR', 'URGENCE_MEDICALE_JOUR', ...]

# Regroupements (5)
REGROUPEMENTS = {
    'Renseignements Santé': [...],
    'Assistances Médicales': [...],
    # ...
}

# Couleurs officielles Cameroun
COULEURS_CAMEROUN = {'vert': '#007A33', ...}

# Configuration Plotly
PLOTLY_CONFIG = {'displayModeBar': True, ...}

# Configuration Cache
CACHE_CONFIG = {'ttl': 3600, 'show_spinner': True}

# Configuration Logs
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': str(LOGS_DIR / 'dashboard.log'),
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5
}

# Messages standardisés
MESSAGES = {
    'success': {...},
    'error': {...},
    'warning': {...},
    'info': {...}
}
```

**Variables CSS centralisées :**

```css
:root {
    /* Couleurs Cameroun */
    --color-vert-cameroun: #007A33;
    --color-jaune-cameroun: #FFD700;
    --color-rouge-cameroun: #CE1126;
    
    /* Espacements */
    --spacing-xs: 5px;
    --spacing-sm: 10px;
    --spacing-md: 20px;
    --spacing-lg: 30px;
    
    /* Bordures */
    --border-radius: 10px;
    --border-width: 3px;
}
```

---

### Module 2 : `utils/`

**Responsabilité** : Logique métier et traitement des données

```
utils/
├── __init__.py                      # Exports (48 fonctions)
├── data_loader.py                   # 550 lignes - 6 fonctions
├── data_processor.py                # 650 lignes - 7 fonctions
├── helpers.py                       # 550 lignes - 14 fonctions
├── logger.py                        # 650 lignes - 12 fonctions
├── charts.py                        # 680 lignes - 9 fonctions
├── pptx_generator_minsante.py       # 800 lignes
└── pptx_generator_advanced.py       # 1000 lignes
```

#### `data_loader.py` (6 fonctions)

```python
def charger_donnees_appels(chemin)
    """Charge Excel appels, valide colonnes, convertit dates."""
    
def charger_calendrier_epidemiologique(chemin)
    """Charge calendrier, détecte auto colonnes."""
    
def charger_toutes_les_donnees()
    """Fonction principale: charge tout + vérifications."""
    
def verifier_coherence_donnees(df_appels, df_calendrier)
    """5 vérifications: dates, semaines, totaux, valeurs, doublons."""
    
def detecter_fichiers_data()
    """Détection auto fichiers avec mots-clés intelligents."""
    
def mettre_a_jour_chemins_config()
    """MAJ auto configuration après uploads."""
```

#### `data_processor.py` (7 fonctions)

```python
def calculer_totaux_hebdomadaires(df_appels)
    """Agrégation jour→semaine."""
    
def calculer_totaux_semaine(df_appels, semaine)
    """Totaux semaine spécifique + stats."""
    
def calculer_variations(df_appels, semaine1, semaine2)
    """Variations absolues/relatives + tendance."""
    
def calculer_regroupements(df_appels, semaine)
    """Agrégation par 5 thématiques."""
    
def obtenir_statistiques_globales(df_appels, df_hebdo)
    """Stats complètes: période, totaux, moyennes, extrêmes."""
    
def regrouper_par_mois(df_hebdo)
    """Conversion semaines→mois avec approximation."""
    
def comparer_periodes(df_appels, semaines_list)
    """Comparaison multi-semaines, tableau croisé."""
```

#### `helpers.py` (14 fonctions)

```python
def extraire_numero_semaine(semaine_str)
    """'S10_2025' → 10"""
    
def obtenir_derniere_semaine(df_hebdo)
def obtenir_semaine_precedente(df_hebdo, semaine)
def obtenir_info_semaine_calendrier(df_calendrier, semaine)
def obtenir_evolution_temporelle(df_hebdo, nb_semaines)

def convert_df_to_csv(df)
    """Export CSV UTF-8-SIG compatible Excel."""
    
def convert_df_to_excel(df, sheet_name)
    """Export Excel natif avec personnalisation."""

def formater_nombre(nombre)
    """Format milliers: 1500 → '1 500'"""
    
def obtenir_mois_francais()
def formater_date_francais(date)
def formater_periode_semaine(date_debut, date_fin)

def generer_nom_fichier(prefix, extension, timestamp)
def valider_format_semaine(semaine_str)
def calculer_duree_jours(date_debut, date_fin)
```

#### `logger.py` (12 fonctions)

```python
def setup_logger(name, log_file, level)
    """Configure logger avec rotation (10MB, 5 backups)."""

def log_chargement_donnees(fichier, nb_lignes, success)
def log_erreur(source, message, exception)
def log_generation_rapport(modele, nb_slides, success, duree)
def log_upload_fichier(nom_fichier, taille, success)
def log_export(format_export, nb_lignes, destination)

# Bonus
def log_aggregation(type_aggregation, nb_lignes_in, nb_lignes_out)
def log_session(action, details)
def log_performance(operation, duree, nb_elements)
def log_validation(type_validation, resultat, nb_erreurs)

def nettoyer_vieux_logs(jours_retention)
def obtenir_stats_logs()
```

#### `charts.py` (9 fonctions)

```python
def creer_graphique_barres(data, x_col, y_col, titre, orientation)
def creer_graphique_camembert(data, labels_col, values_col, type_graphique)
def creer_graphique_ligne(data, x_col, y_col, titre, show_markers)
def creer_graphique_barres_groupees(data, x_col, categories_cols)
def creer_heatmap(data, x_col, y_col, z_col)
def creer_graphique_evolution(data, x_col, y_col, ajouter_tendance)
def creer_graphique_variation(data, x_col, y_col)
def creer_graphique_comparaison(data, categories, series_dict)
def creer_graphique_distribution(data, valeurs_col, bins)
```

---

### Module 3 : `components/`

**Responsabilité** : Composants UI réutilisables

```
components/
├── __init__.py          # Exports (35 fonctions)
├── layout.py            # 650 lignes - 13 fonctions
├── metrics.py           # 630 lignes - 7 fonctions
├── tables.py            # 680 lignes - 7 fonctions
└── charts.py            # 450 lignes - 8 fonctions
```

#### `layout.py` (13 fonctions)

```python
def apply_custom_css()
    """Charge config/styles.css."""
    
def page_header(title, subtitle, icon, show_flag)
    """Header avec bannière gradient + drapeau."""
    
def section_header(title, subtitle, icon, level)
    """Header section avec bordure jaune."""
    
def page_footer(show_credits, show_version, custom_text)
    """Footer standard MINSANTE."""
    
def info_box(message, box_type, icon, title)
    """Boîtes info/success/warning/danger."""
    
def modele_selection_card(title, description, features_list)
    """Cartes sélection modèles PowerPoint."""

# 7 fonctions bonus
def metric_card_simple(label, value, icon, color)
def alert_banner(message, alert_type)
def custom_divider(text, color)
def breadcrumb(items)
def badge(text, badge_type)
def custom_spinner(text)
def custom_progress_bar(progress, text)
```

#### `metrics.py` (7 fonctions)

```python
def metric_card_html(label, value, delta, icon, color)
    """Carte métrique avec gradient."""
    
def metric_row(metrics_list, columns)
    """Ligne de métriques avec colonnes auto."""
    
def kpi_card(title, value, subtitle, comparison_value)
    """KPI card sophistiquée."""
    
def comparison_metric(label, value1, value2, label1, label2)
    """Métrique de comparaison avec variation."""

# 3 fonctions bonus
def mini_metric(label, value, icon)
def stat_card(title, stats_dict, icon)
def gauge_metric(label, value, max_value, unit)
```

#### `tables.py` (7 fonctions)

```python
def display_dataframe_formatted(df, format_dates, format_numbers)
    """DataFrame avec formatage auto dates/nombres."""
    
def export_buttons(df, filename_prefix, formats)
    """Boutons export CSV + Excel."""
    
def create_summary_table(data_dict, title, show_total)
    """Tableau récapitulatif stylisé HTML."""
    
def create_comparison_table(df, columns_to_compare, category_column)
    """Tableau comparaison avec variations."""

# 3 fonctions bonus
def create_table_with_sparklines(df, value_column, sparkline_columns)
def create_pivot_table_interface(df, title)
def create_filtered_table(df, title, filterable_columns)
```

#### `charts.py` (8 fonctions - Wrappers)

```python
def graphique_evolution_semaines(df_hebdo, nb_semaines, titre)
    """Évolution N dernières semaines (tri auto)."""
    
def graphique_top_categories(df_appels, semaine, top_n)
    """Top N catégories avec labels."""
    
def graphique_repartition_regroupements(regroupements_data, titre)
    """Répartition thématique donut."""
    
def graphique_comparaison_semaines(df_appels, semaines_list, categories)
    """Comparaison multi-semaines."""
    
def graphique_evolution_journaliere(df_appels, semaine)
    """Évolution jour par jour."""
    
def graphique_comparaison_mensuelle(df_mois)
    """Comparaison mensuelle."""
    
def afficher_graphique(fig, key)
    """Helper d'affichage avec config."""
    
def graphique_avec_export(fig, filename_prefix)
    """Graphique + export PNG."""
```

---

### Module 4 : `pages/`

**Responsabilité** : Orchestration et présentation

```
pages/
├── 1_Vue_Ensemble.py                # 320 lignes (-54%)
├── 2_Analyse_Epidemiologique.py     # 270 lignes (-55%)
├── 3_Comparaisons.py                # 310 lignes (-56%)
├── 4_Donnees_Brutes.py              # 370 lignes (-51%)
└── 5_Generation_Rapports.py         # 290 lignes (-55%)
```

**Structure type d'une page :**

```python
"""Docstring avec description."""

import streamlit as st
from config import settings
from utils import (charger_toutes_les_donnees, calculer_totaux_semaine)
from components import (page_header, metric_row, export_buttons)

# Configuration
st.set_page_config(...)

# Initialisation
apply_custom_css()
logger = setup_logger('page_name')

# Header
page_header(title="...", subtitle="...")

# Chargement données avec cache
@st.cache_data(ttl=settings.CACHE_CONFIG['ttl'])
def load_data():
    return charger_toutes_les_donnees()

# Logique métier
donnees = load_data()
totaux = calculer_totaux_semaine(...)

# Affichage
metric_row(metrics)
st.plotly_chart(fig)
export_buttons(df)

# Footer
page_footer()
```

---

## 🔄 Flux de Données

### Pipeline de Traitement

```
┌─────────────────┐
│  Fichiers Excel │
│   (data/)       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   data_loader.py                │
│   - charger_donnees_appels()    │
│   - charger_calendrier()        │
│   - verifier_coherence()        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Cache Streamlit (@cache_data) │
│   TTL: 3600s (1 heure)          │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   data_processor.py             │
│   - calculer_totaux()           │
│   - calculer_variations()       │
│   - obtenir_statistiques()      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Pages Streamlit               │
│   - Affichage                   │
│   - Interaction utilisateur     │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Exports / Rapports            │
│   - CSV, Excel, PowerPoint      │
└─────────────────────────────────┘
```

### Exemple de Flux Complet

```python
# 1. Chargement (data_loader.py)
donnees = charger_toutes_les_donnees()
# → Retourne: {'appels', 'calendrier', 'hebdomadaire', 'statistiques'}

# 2. Cache Streamlit
@st.cache_data(ttl=3600)
def load_data():
    return charger_toutes_les_donnees()

# 3. Traitement (data_processor.py)
totaux = calculer_totaux_semaine(donnees['appels'], 'S10_2025')
# → Retourne: {'total', 'moyenne_jour', 'categories', 'regroupements', ...}

# 4. Affichage (components)
metrics = [
    {'label': 'Total', 'value': totaux['total'], 'icon': '📞'}
]
metric_row(metrics)

# 5. Export (helpers + tables)
export_buttons(df, filename_prefix="rapport")
```

---

## 💾 Système de Cache

### Configuration Cache Streamlit

```python
# config/settings.py
CACHE_CONFIG = {
    'ttl': 3600,  # Time To Live: 1 heure
    'show_spinner': True,
    'spinner_text': '⏳ Chargement des données...'
}
```

### Utilisation du Cache

```python
@st.cache_data(ttl=settings.CACHE_CONFIG['ttl'])
def load_data():
    """
    Fonction cachée pendant 1 heure.
    Le cache est invalidé si:
    - TTL expiré (3600s)
    - Paramètres changent
    - Cache manuellement effacé
    """
    return charger_toutes_les_donnees()
```

### Avantages du Cache

| Aspect | Sans Cache | Avec Cache |
|--------|------------|------------|
| **Chargement initial** | ~3-5s | ~3-5s |
| **Chargements suivants** | ~3-5s | <0.1s |
| **Gain** | - | **97%** |

### Effacer le Cache

```python
# Programmatique
st.cache_data.clear()

# Interface utilisateur
# Streamlit UI: Settings > Clear cache
```

---

## 📝 Gestion des Logs

### Configuration Logs

```python
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'log_file': str(LOGS_DIR / 'dashboard.log'),
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,  # 5 fichiers de backup
    'encoding': 'utf-8'
}
```

### Rotation Automatique

```
logs/
├── dashboard.log          # Fichier actuel
├── dashboard.log.1        # Backup 1 (plus récent)
├── dashboard.log.2        # Backup 2
├── dashboard.log.3        # Backup 3
├── dashboard.log.4        # Backup 4
└── dashboard.log.5        # Backup 5 (plus ancien)
```

### Exemple de Logs

```
2025-12-04 14:30:25 - app - INFO - === Page d'accueil chargée ===
2025-12-04 14:30:26 - data_loader - INFO - ✅ Chargement réussi : Appels_hebdomadaires.xlsx (365 lignes)
2025-12-04 14:30:26 - data_loader - INFO - ✅ Chargement réussi : CALENDRIER_EPIDEMIOLOGIQUE_2025_cm.xlsx (52 lignes)
2025-12-04 14:30:27 - data_processor - INFO - 📊 Agrégation hebdomadaire : 365 → 52 lignes (0.5s)
2025-12-04 14:35:10 - pptx_generator - INFO - ✅ Rapport Modèle A généré : 16 slides en 25.3s
2025-12-04 14:40:15 - upload - INFO - ✅ Upload réussi : nouveaux_appels.xlsx (512.0 KB) - Type: appels
```

### Utilisation dans le Code

```python
from utils import setup_logger, log_erreur, log_chargement_donnees

logger = setup_logger('mon_module')

try:
    df = pd.read_excel(fichier)
    log_chargement_donnees(fichier, len(df), success=True)
except Exception as e:
    log_erreur('chargement', 'Erreur lecture fichier', exception=e)
```

---

## 🎨 Composants Réutilisables

### Principe de Composition

Au lieu de répéter du code HTML/CSS, on compose des pages avec des composants :

**Avant (v1.0) :**
```python
# Répété dans chaque page (150 lignes)
st.markdown(f"""
<div style="background: linear-gradient(...); padding: 20px;">
    <h1>{title}</h1>
    <p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)
```

**Après (v2.0) :**
```python
# 1 seule ligne
page_header(title="...", subtitle="...")
```

### Bibliothèque de Composants

| Composant | Module | Usage |
|-----------|--------|-------|
| `page_header()` | layout | Header de page |
| `section_header()` | layout | Header de section |
| `metric_row()` | metrics | Ligne de métriques |
| `kpi_card()` | metrics | Carte KPI |
| `comparison_metric()` | metrics | Métrique comparaison |
| `export_buttons()` | tables | Boutons export |
| `display_dataframe_formatted()` | tables | DataFrame formaté |
| `graphique_evolution_semaines()` | charts | Graphique évolution |

### Exemple de Composition

```python
# Page complète en ~30 lignes au lieu de ~150

from components import (
    apply_custom_css,
    page_header,
    section_header,
    metric_row,
    page_footer
)

apply_custom_css()

page_header("Mon Dashboard", subtitle="Analyse")

section_header("Statistiques", icon="📊")

metrics = [
    {'label': 'Total', 'value': 1500, 'icon': '📞'},
    {'label': 'Moyenne', 'value': 450, 'icon': '📊'}
]
metric_row(metrics)

page_footer()
```

---

## 🎯 Patterns Utilisés

### 1. Factory Pattern

Création de graphiques avec configuration automatique :

```python
def creer_graphique_barres(data, **kwargs):
    """Factory qui crée un graphique configuré."""
    return go.Figure(data=[
        go.Bar(
            x=data.keys(),
            y=data.values(),
            marker_color=settings.COULEURS_CAMEROUN['vert'],
            # ... config automatique
        )
    ])
```

### 2. Decorator Pattern

Cache Streamlit avec décorateur :

```python
@st.cache_data(ttl=3600)
def load_data():
    return charger_toutes_les_donnees()
```

### 3. Strategy Pattern

Différentes stratégies de génération de rapports :

```python
if modele == "ORIGINAL":
    generer_rapport_minsante(...)
elif modele == "A":
    generer_rapport_avance(..., modele="A")
elif modele == "B":
    generer_rapport_avance(..., modele="B")
```

### 4. Singleton Pattern

Logger unique par module :

```python
_loggers = {}  # Dictionnaire de singletons

def setup_logger(name):
    if name in _loggers:
        return _loggers[name]  # Retourne l'existant
    
    logger = logging.getLogger(name)
    # ... configuration ...
    _loggers[name] = logger
    return logger
```

### 5. Template Method Pattern

Structure commune des pages :

```python
# Template de page
def page_template():
    # 1. Configuration
    st.set_page_config(...)
    
    # 2. Initialisation
    apply_custom_css()
    logger = setup_logger()
    
    # 3. Header
    page_header(...)
    
    # 4. Chargement données
    data = load_data()
    
    # 5. Logique spécifique (varie selon la page)
    # ...
    
    # 6. Footer
    page_footer()
```

---

## ⚡ Performance

### Optimisations Implémentées

1. **Cache Streamlit**
   - Évite rechargement données (gain 97%)
   - TTL configurable (1 heure)

2. **Chargement Lazy**
   - Données chargées une seule fois
   - Cache partagé entre pages

3. **Formatage Optimisé**
   - `formater_nombre()` avec regex optimisé
   - Conversion dates en batch

4. **Tri Intelligent**
   - `extraire_numero_semaine()` avec cache
   - Tri une seule fois puis réutilisé

### Métriques de Performance

| Opération | Temps |
|-----------|-------|
| Chargement initial | 3-5s |
| Navigation entre pages | <0.5s |
| Génération graphique | <0.2s |
| Export CSV | <0.5s |
| Export Excel | <1s |
| Génération PowerPoint | 20-40s |

### Profiling

```python
from utils import log_performance

start = time.time()
resultat = operation_longue()
duree = time.time() - start

log_performance('operation_longue', duree, nb_elements=len(resultat))
```

---

## 🔒 Sécurité

### Validation des Données

```python
def verifier_coherence_donnees(df_appels, df_calendrier):
    """5 vérifications de cohérence."""
    erreurs = []
    
    # 1. Plage de dates valide
    if df_appels['DATE'].min() > df_appels['DATE'].max():
        erreurs.append("Dates incohérentes")
    
    # 2. Semaines manquantes
    # ...
    
    # 3. Totaux cohérents (±1%)
    # ...
    
    return erreurs
```

### Protection contre Injection

- Pas d'exécution de code utilisateur
- Validation des formats de fichiers
- Sanitization des noms de fichiers

### Gestion des Erreurs

```python
try:
    df = charger_donnees_appels(fichier)
except FileNotFoundError:
    st.error("Fichier introuvable")
    logger.error(f"Fichier {fichier} introuvable")
except pd.errors.ParserError:
    st.error("Format Excel invalide")
    logger.error("Erreur parsing Excel")
except Exception as e:
    st.error("Erreur inattendue")
    log_erreur('chargement', str(e), exception=e)
```

---

## 🚀 Évolutivité

### Ajout d'une Nouvelle Page

1. **Créer le fichier**
```python
# pages/6_Nouvelle_Page.py
from config import settings
from utils import charger_toutes_les_donnees
from components import page_header, page_footer

st.set_page_config(...)
apply_custom_css()

page_header("Nouvelle Page", subtitle="...")

# Logique spécifique

page_footer()
```

2. **Streamlit détecte automatiquement**
   - Fichier dans `pages/`
   - Préfixe numérique pour ordre
   - Apparaît dans menu latéral

### Ajout d'une Nouvelle Fonction Utils

1. **Créer la fonction**
```python
# utils/helpers.py
def nouvelle_fonction(param):
    """Docstring."""
    return resultat
```

2. **Exporter dans `__init__.py`**
```python
# utils/__init__.py
from utils.helpers import nouvelle_fonction

__all__ = [
    # ... autres exports
    'nouvelle_fonction'
]
```

3. **Utiliser partout**
```python
from utils import nouvelle_fonction
```

### Ajout d'un Nouveau Composant

```python
# components/layout.py
def nouveau_composant(params):
    """Docstring."""
    html = f"<div>...</div>"
    st.markdown(html, unsafe_allow_html=True)

# components/__init__.py
from components.layout import nouveau_composant

__all__ = [..., 'nouveau_composant']
```

---

## 📊 Diagrammes

### Diagramme de Classes Simplifié

```
┌──────────────────┐
│   ConfigModule   │
├──────────────────┤
│ + settings       │
│ + styles.css     │
└──────────────────┘
         △
         │ uses
         │
┌──────────────────┐
│   UtilsModule    │
├──────────────────┤
│ + DataLoader     │
│ + DataProcessor  │
│ + Helpers        │
│ + Logger         │
│ + Charts         │
└──────────────────┘
         △
         │ uses
         │
┌──────────────────┐
│ ComponentsModule │
├──────────────────┤
│ + Layout         │
│ + Metrics        │
│ + Tables         │
│ + Charts         │
└──────────────────┘
         △
         │ uses
         │
┌──────────────────┐
│   PagesModule    │
├──────────────────┤
│ + Page1          │
│ + Page2          │
│ + Page3          │
│ + Page4          │
│ + Page5          │
└──────────────────┘
```

---

## 📚 Références

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Python Best Practices](https://docs.python-guide.org/)
- [Clean Code Principles](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

**Dernière mise à jour : Décembre 2025**  
**Version : 2.0**  
**Auteur : Fred - AIMS Cameroon / MINSANTE**