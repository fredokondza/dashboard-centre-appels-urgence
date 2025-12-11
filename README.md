# 🏥 Dashboard Centre d'Appels d'Urgence Sanitaire 1510

![Version](https://img.shields.io/badge/version-2.0-green.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.39.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

> Application Streamlit pour l'analyse et le suivi des appels du Centre d'Appels d'Urgence Sanitaire 1510 - MINSANTE Cameroun 🇨🇲

---

## 📋 Table des Matières

- [À Propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Configuration](#-configuration)
- [Pages du Dashboard](#-pages-du-dashboard)
- [Technologies](#-technologies)
- [Développement](#-développement)
- [Auteur](#-auteur)
- [License](#-license)

---

## 🎯 À Propos

Ce dashboard professionnel permet l'analyse épidémiologique des données d'appels du Centre 1510 avec :

- ✅ **Visualisations interactives** : Graphiques Plotly dynamiques
- ✅ **Analyse temporelle** : Évolution hebdomadaire et mensuelle
- ✅ **Comparaisons avancées** : Multi-périodes et multi-critères
- ✅ **Exports automatisés** : CSV, Excel, PowerPoint
- ✅ **Architecture professionnelle** : Code réutilisable et maintenable

### 🆕 Version 2.0 (Architecture Professionnelle)

Cette version majeure apporte :

- 🏗️ **Architecture modulaire** : Code organisé en modules réutilisables
- 📉 **Réduction de 53%** : 3,900 → 1,840 lignes pour les pages
- 🎨 **CSS centralisé** : 850 lignes dupliquées éliminées
- 🔄 **Composants réutilisables** : 35+ fonctions standardisées
- 📝 **Logs structurés** : Système de logs professionnel
- ⚡ **Performances optimisées** : Cache et chargement améliorés

---

## ✨ Fonctionnalités

### 📊 Analyses Disponibles

1. **Vue d'Ensemble**
   - KPIs de la dernière semaine
   - Top catégories d'appels
   - Répartition thématique
   - Comparaison semaine précédente

2. **Analyse Épidémiologique**
   - Analyse détaillée par semaine
   - Comparaison multi-semaines
   - Évolution journalière
   - Graphiques comparatifs

3. **Comparaisons Temporelles**
   - Comparaisons hebdomadaires
   - Agrégation mensuelle
   - Analyse des tendances
   - Régression linéaire

4. **Données Brutes**
   - Consultation des données
   - Filtrage avancé
   - Export CSV/Excel
   - Upload et mise à jour

5. **Génération de Rapports**
   - 3 modèles PowerPoint (Original, A, B)
   - Génération automatique
   - Téléchargement direct
   - Historique des rapports

### 📈 Indicateurs Suivis

- **17 catégories d'appels** : CSU, Urgence médicale, Informations, etc.
- **5 regroupements thématiques** : Renseignements, Assistances, Signaux, etc.
- **Statistiques globales** : Total, moyenne, min, max, tendances
- **52 semaines épidémiologiques** : Calendrier 2025 complet

---

## 🏗️ Architecture

### Structure Modulaire

```
dashboard_urgence_appel/
├── 📱 app.py                    # Page d'accueil
├── 📂 config/                   # Configuration centralisée
│   ├── __init__.py
│   ├── settings.py              # Paramètres globaux
│   └── styles.css               # CSS centralisé (650 lignes)
├── 📂 pages/                    # Pages Streamlit
│   ├── 1_Vue_Ensemble.py
│   ├── 2_Analyse_Epidemiologique.py
│   ├── 3_Comparaisons.py
│   ├── 4_Donnees_Brutes.py
│   └── 5_Generation_Rapports.py
├── 📂 utils/                    # Utilitaires
│   ├── __init__.py
│   ├── data_loader.py           # Chargement données (6 fonctions)
│   ├── data_processor.py        # Traitement données (7 fonctions)
│   ├── helpers.py               # Fonctions utilitaires (14 fonctions)
│   ├── logger.py                # Système de logs (12 fonctions)
│   ├── charts.py                # Graphiques Plotly (9 fonctions)
│   ├── pptx_generator_minsante.py
│   └── pptx_generator_advanced.py
├── 📂 components/               # Composants réutilisables
│   ├── __init__.py
│   ├── layout.py                # Mise en page (13 fonctions)
│   ├── metrics.py               # Métriques/KPIs (7 fonctions)
│   ├── tables.py                # Tableaux (7 fonctions)
│   └── charts.py                # Wrappers graphiques (8 fonctions)
├── 📂 data/                     # Données
│   ├── Appels_hebdomadaires.xlsx
│   ├── CALENDRIER_EPIDEMIOLOGIQUE_2025_cm.xlsx
│   └── backups/
├── 📂 logs/                     # Fichiers de logs
├── 📂 assets/                   # Ressources (images, etc.)
└── 📄 requirements.txt          # Dépendances Python
```

### Avantages de l'Architecture

| Aspect | Avant (v1.0) | Après (v2.0) | Gain |
|--------|--------------|--------------|------|
| **Lignes pages** | 3,900 | 1,840 | **-53%** |
| **CSS dupliqué** | 850 | 0 | **-100%** |
| **Fonctions dupliquées** | ~20 | 0 | **-100%** |
| **Modules** | 0 | 4 | **+4** |
| **Réutilisabilité** | 0% | 75% | **+75%** |

---

## 🚀 Installation

### Prérequis

- Python 3.12 ou supérieur
- pip (gestionnaire de packages Python)
- Git (optionnel)

### Étape 1 : Cloner le Projet

```bash
git clone https://github.com/your-username/dashboard-urgence-1510.git
cd dashboard-urgence-1510
```

### Étape 2 : Créer un Environnement Virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Préparer les Données

Placez vos fichiers Excel dans le dossier `data/` :

```
data/
├── Appels_hebdomadaires.xlsx
└── CALENDRIER_EPIDEMIOLOGIQUE_2025_cm.xlsx
```

### Étape 5 : Lancer l'Application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`

---

## 💻 Utilisation

### Navigation

Le dashboard comporte **6 pages principales** accessibles via le menu latéral :

1. **🏠 Accueil** : Vue d'ensemble et statistiques globales
2. **👁️ Vue d'Ensemble** : Analyse de la dernière semaine
3. **🔬 Analyse Épidémiologique** : Analyse détaillée par semaine
4. **📊 Comparaisons** : Comparaisons temporelles avancées
5. **📋 Données Brutes** : Consultation et export des données
6. **📊 Génération de Rapports** : Rapports PowerPoint automatiques

### Imports Simplifiés

Grâce aux fichiers `__init__.py`, les imports sont simplifiés :

```python
# ✅ Nouvelle syntaxe (v2.0)
from config import settings, CATEGORIES_APPELS, COULEURS_CAMEROUN
from utils import charger_toutes_les_donnees, calculer_totaux_semaine
from components import page_header, metric_row, export_buttons

# ❌ Ancienne syntaxe (v1.0)
from config.settings import APP_CONFIG, CATEGORIES_APPELS
from utils.data_loader import charger_toutes_les_donnees
from utils.data_processor import calculer_totaux_semaine
from components.layout import page_header
from components.metrics import metric_row
from components.tables import export_buttons
```

### Exemples de Code

#### Charger les Données

```python
from utils import charger_toutes_les_donnees

# Charge toutes les données avec vérifications
donnees = charger_toutes_les_donnees()

df_appels = donnees['appels']
df_calendrier = donnees['calendrier']
df_hebdo = donnees['hebdomadaire']
stats = donnees['statistiques']
```

#### Créer un Graphique

```python
from utils import creer_graphique_evolution

fig = creer_graphique_evolution(
    data=df_hebdo,
    x_col='Semaine épidémiologique',
    y_col='TOTAL_APPELS_SEMAINE',
    titre="Évolution des appels",
    ajouter_moyenne=True,
    ajouter_tendance=True
)

st.plotly_chart(fig, use_container_width=True)
```

#### Afficher des Métriques

```python
from components import metric_row

metrics = [
    {'label': 'Total Appels', 'value': 15234, 'icon': '📞'},
    {'label': 'Moyenne/Jour', 'value': 450, 'icon': '📊'},
    {'label': 'Semaines', 'value': 52, 'icon': '📅'}
]

metric_row(metrics, columns=3)
```

---

## ⚙️ Configuration

### Fichier `config/settings.py`

Toutes les configurations sont centralisées dans ce fichier :

```python
# Configuration application
APP_CONFIG = {
    'page_title': 'Dashboard Urgence 1510',
    'version': '2.0',
    'author': 'Fred - AIMS Cameroon'
}

# Catégories d'appels (17)
CATEGORIES_APPELS = [
    'CSU_JOUR',
    'URGENCE_MEDICALE_JOUR',
    'INFO_SANTE_JOUR',
    # ... 14 autres
]

# Couleurs officielles Cameroun
COULEURS_CAMEROUN = {
    'vert': '#007A33',
    'jaune': '#FFD700',
    'rouge': '#CE1126'
}

# Cache Streamlit
CACHE_CONFIG = {
    'ttl': 3600,  # 1 heure
    'show_spinner': True
}
```

### Personnalisation du CSS

Le fichier `config/styles.css` contient tous les styles :

```css
/* Couleurs Cameroun */
:root {
    --color-vert-cameroun: #007A33;
    --color-jaune-cameroun: #FFD700;
    --color-rouge-cameroun: #CE1126;
}

/* Titre principal */
.main-title {
    background: linear-gradient(135deg, #007A33 0%, #00a844 100%);
    /* ... */
}
```

### Variables d'Environnement

Créez un fichier `.env` (optionnel) :

```env
DATA_DIR=./data
LOGS_DIR=./logs
CACHE_TTL=3600
LOG_LEVEL=INFO
```

---

## 📊 Pages du Dashboard

### 1. 🏠 Page d'Accueil (`app.py`)

**Contenu :**
- Statistiques globales (total, moyenne, semaines)
- Évolution des 10 dernières semaines
- Top 8 catégories
- Répartition par regroupements thématiques
- Tableau de comparaison

**Fonctions clés :**
```python
load_data()  # Cache des données
metric_row()  # Affichage métriques
creer_graphique_evolution()  # Graphique temporel
```

### 2. 👁️ Vue d'Ensemble (`pages/1_Vue_Ensemble.py`)

**Contenu :**
- KPIs de la dernière semaine
- Répartition des 17 catégories
- Répartition des 5 regroupements
- Comparaison avec semaine précédente
- Évolution temporelle triée

**Fonctions clés :**
```python
obtenir_derniere_semaine()
calculer_totaux_semaine()
calculer_variations()
comparison_metric()
```

### 3. 🔬 Analyse Épidémiologique (`pages/2_Analyse_Epidemiologique.py`)

**Modes :**
1. **Analyse d'une semaine** : Détails complets pour une semaine
2. **Comparaison multi-semaines** : Comparer 2 à 10 semaines

**Fonctions clés :**
```python
create_comparison_table()
creer_graphique_barres_groupees()
comparer_periodes()
```

### 4. 📊 Comparaisons (`pages/3_Comparaisons.py`)

**Types de comparaison :**
1. **Hebdomadaire** : Période personnalisée
2. **Mensuelle** : Agrégation par mois
3. **Tendances** : Régression linéaire et volatilité

**Fonctions clés :**
```python
regrouper_par_mois()
creer_graphique_variation()
```

### 5. 📋 Données Brutes (`pages/4_Donnees_Brutes.py`)

**Fonctionnalités :**
- Consultation des 3 types de données
- Filtrage multi-critères
- Export CSV/Excel
- Upload de nouveaux fichiers
- Historique des backups

**Fonctions clés :**
```python
display_dataframe_formatted()
export_buttons()
detecter_fichiers_data()
```

### 6. 📊 Génération de Rapports (`pages/5_Generation_Rapports.py`)

**Modèles disponibles :**
- **Original** : 7 slides - Format standard
- **Modèle A** : 16 slides - Analyse détaillée
- **Modèle B** : 9 slides - Format condensé

**Fonctions clés :**
```python
generer_rapport_minsante()
generer_rapport_avance()
log_generation_rapport()
```

---

## 🛠️ Technologies

### Frameworks & Bibliothèques

| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.12.2 | Langage principal |
| **Streamlit** | 1.39.0 | Framework web |
| **Pandas** | 2.2.3 | Manipulation données |
| **Plotly** | 5.24.1 | Visualisations |
| **python-pptx** | 1.0.2 | Génération PowerPoint |
| **openpyxl** | 3.1.5 | Lecture/écriture Excel |

### Installation Complète

```bash
pip install streamlit==1.39.0
pip install pandas==2.2.3
pip install plotly==5.24.1
pip install python-pptx==1.0.2
pip install openpyxl==3.1.5
pip install numpy
pip install pillow
```

---

## 👨‍💻 Développement

### Structure des Modules

Chaque module a un rôle spécifique :

- **`config/`** : Configuration centralisée
- **`utils/`** : Fonctions utilitaires (48 fonctions)
- **`components/`** : Composants UI réutilisables (35 fonctions)
- **`pages/`** : Pages Streamlit (6 pages)

### Ajouter une Nouvelle Fonction

1. **Déterminer le module approprié**
   - Chargement/traitement données → `utils/`
   - Composant UI → `components/`
   - Configuration → `config/`

2. **Créer la fonction avec docstring**
```python
def ma_nouvelle_fonction(param1, param2):
    """
    Description de la fonction.
    
    Args:
        param1 (type): Description
        param2 (type): Description
    
    Returns:
        type: Description
    
    Example:
        >>> resultat = ma_nouvelle_fonction(val1, val2)
    """
    # Code ici
    return resultat
```

3. **Ajouter aux exports dans `__init__.py`**
```python
from module import ma_nouvelle_fonction

__all__ = [
    # ... autres exports
    'ma_nouvelle_fonction'
]
```

### Tests

Pour tester une page individuellement :

```bash
streamlit run pages/1_Vue_Ensemble.py
```

### Logs

Les logs sont automatiquement créés dans `logs/dashboard.log` :

```python
from utils import setup_logger, log_erreur

logger = setup_logger('mon_module')
logger.info("Information")
logger.warning("Avertissement")
log_erreur('fonction', 'message', exception=e)
```

---

## 👤 Auteur

**Fred**  
Master's Student in Data Science  
African Institute for Mathematical Sciences (AIMS-Cameroun)

**Stage Professionnel**  
CCOUSP/MINSANTE - Centre de Coordination des Opérations d'Urgence Sanitaire Publique  
Ministère de la Santé Publique du Cameroun

**Supervision :**
- Christian MOUANGUE (Centre Pasteur du Cameroun)
- Jules TCHATCHUENG (Centre Pasteur du Cameroun)
- Dr. Antem Yolande Ebude EBONG (AIMS-Cameroun)

**Contact**  
📧 Email : [votre-email]  
🔗 LinkedIn : [votre-linkedin]  
💻 GitHub : [votre-github]

---

## 📄 License

Ce projet est sous licence MIT.

```
MIT License

Copyright (c) 2025 Fred - AIMS Cameroon / MINSANTE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 🙏 Remerciements

- **MINSANTE** : Ministère de la Santé Publique du Cameroun
- **Centre Pasteur du Cameroun** : Supervision technique
- **AIMS-Cameroun** : Formation académique
- **Communauté Streamlit** : Framework et support

---

## 📚 Documentation Complémentaire

- [ARCHITECTURE.md](ARCHITECTURE.md) : Documentation technique détaillée
- [CHANGELOG.md](CHANGELOG.md) : Historique des versions
- [Streamlit Docs](https://docs.streamlit.io/) : Documentation officielle Streamlit

---

## 🔄 Mises à Jour

### Version 2.0 (Décembre 2025)
- ✨ Architecture professionnelle modulaire
- 🎨 CSS centralisé (650 lignes)
- 📦 Modules réutilisables (48+ fonctions utils)
- 🎯 Composants UI (35+ fonctions)
- 📉 Réduction de 53% du code des pages
- 📝 Système de logs professionnel
- ⚡ Performances optimisées

### Version 1.0 (Novembre 2025)
- 🚀 Version initiale fonctionnelle
- 📊 5 pages d'analyse
- 📈 Graphiques Plotly
- 📄 Génération rapports PowerPoint

---

**Fait avec ❤️ pour la santé publique au Cameroun 🇨🇲**