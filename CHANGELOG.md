# 📋 Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [2.0.0] - 2025-12-04

### 🎉 Version Majeure - Architecture Professionnelle

Cette version majeure apporte une refonte complète de l'architecture avec une réduction significative du code et l'introduction de modules réutilisables.

### ✨ Ajouté

#### Configuration Centralisée (`config/`)
- ✅ **settings.py** (550 lignes) : Configuration globale centralisée
  - `APP_CONFIG` : Configuration application (titre, version, auteur)
  - `CATEGORIES_APPELS` : 17 catégories d'appels
  - `REGROUPEMENTS` : 5 regroupements thématiques
  - `COULEURS_CAMEROUN` : Palette officielle (vert, jaune, rouge)
  - `PLOTLY_CONFIG` : Configuration graphiques standardisée
  - `CACHE_CONFIG` : Paramètres cache (ttl: 3600s)
  - `LOGGING_CONFIG` : Configuration logs avec rotation
  - `MESSAGES` : Messages standardisés (success, error, warning, info)
  - Fonctions : `get_config()`, `get_color()`, `get_label_categorie()`

- ✅ **styles.css** (650 lignes) : CSS centralisé
  - Variables CSS pour couleurs Cameroun
  - 22 sections organisées (main-title, metric-card, info-box, etc.)
  - Responsive design (mobile <768px, tablette 769-1024px)
  - Animations (fadeIn, slideIn, pulse)
  - Classes utilitaires (espacements, texte, affichage)

- ✅ **__init__.py** : Exports simplifiés pour imports faciles

#### Module Utilitaires (`utils/`)
- ✅ **data_loader.py** (550 lignes) - 6 fonctions :
  - `charger_donnees_appels()` : Validation colonnes, conversion dates
  - `charger_calendrier_epidemiologique()` : Détection auto colonnes
  - `charger_toutes_les_donnees()` : Fonction principale avec agrégation
  - `verifier_coherence_donnees()` : 5 vérifications (dates, semaines, totaux, valeurs, doublons)
  - `detecter_fichiers_data()` : Détection auto fichiers Excel
  - `mettre_a_jour_chemins_config()` : MAJ auto configuration

- ✅ **data_processor.py** (650 lignes) - 7 fonctions :
  - `calculer_totaux_hebdomadaires()` : Agrégation jour→semaine
  - `calculer_totaux_semaine()` : Totaux semaine spécifique + stats
  - `calculer_variations()` : Variations absolues/relatives + tendance
  - `calculer_regroupements()` : Agrégation par 5 thématiques
  - `obtenir_statistiques_globales()` : Stats complètes (période, totaux, moyennes, extrêmes)
  - `regrouper_par_mois()` : Conversion semaines→mois avec approximation
  - `comparer_periodes()` : Comparaison multi-semaines

- ✅ **helpers.py** (550 lignes) - 14 fonctions :
  - `extraire_numero_semaine()` : 'S10_2025' → 10
  - `obtenir_derniere_semaine()` : Dernière semaine avec tri intelligent
  - `obtenir_semaine_precedente()` : Navigation temporelle
  - `obtenir_info_semaine_calendrier()` : Infos détaillées depuis calendrier
  - `obtenir_evolution_temporelle()` : Données pour graphiques
  - `convert_df_to_csv()` : Export CSV UTF-8-SIG compatible Excel
  - `convert_df_to_excel()` : Export Excel natif
  - `formater_nombre()` : Format milliers avec espaces
  - `obtenir_mois_francais()` : Dictionnaire centralisé
  - `formater_date_francais()` : Format français standard
  - `formater_periode_semaine()` : "01 au 07 Novembre 2025"
  - `generer_nom_fichier()` : Noms standardisés avec date
  - `valider_format_semaine()` : Validation S1_2025 à S53_2025
  - `calculer_duree_jours()` : Durée entre 2 dates

- ✅ **logger.py** (650 lignes) - 12 fonctions :
  - `setup_logger()` : Configuration avec rotation (10 MB, 5 backups)
  - `log_chargement_donnees()` : Log chargement fichiers
  - `log_erreur()` : Log erreurs avec traceback
  - `log_generation_rapport()` : Log génération PowerPoint
  - `log_upload_fichier()` : Log uploads
  - `log_export()` : Log exports CSV/Excel
  - `log_aggregation()` : Log agrégations
  - `log_session()` : Log actions utilisateur
  - `log_performance()` : Log performances
  - `log_validation()` : Log validations
  - `nettoyer_vieux_logs()` : Suppression logs anciens
  - `obtenir_stats_logs()` : Statistiques fichiers logs

- ✅ **charts.py** (680 lignes) - 9 fonctions :
  - `creer_graphique_barres()` : Graphique barres (vertical/horizontal)
  - `creer_graphique_camembert()` : Pie/Donut avec pourcentages
  - `creer_graphique_ligne()` : Évolution temporelle
  - `creer_graphique_barres_groupees()` : Comparaison multi-séries
  - `creer_heatmap()` : Carte de chaleur
  - `creer_graphique_evolution()` : Version avancée avec tendance + moyenne
  - `creer_graphique_variation()` : Barres +/- avec couleurs conditionnelles
  - `creer_graphique_comparaison()` : Multi-critères
  - `creer_graphique_distribution()` : Histogramme

- ✅ **__init__.py** : Exports de 48 fonctions utilitaires

#### Module Composants (`components/`)
- ✅ **layout.py** (650 lignes) - 13 fonctions :
  - `apply_custom_css()` : Charge config/styles.css
  - `page_header()` : Header avec bannière gradient + drapeau
  - `section_header()` : Headers sections avec bordure jaune
  - `page_footer()` : Footer standard MINSANTE
  - `info_box()` : Boîtes info/success/warning/danger
  - `modele_selection_card()` : Cartes sélection modèles PowerPoint
  - 7 fonctions bonus (metric_card_simple, alert_banner, custom_divider, breadcrumb, badge, custom_spinner, custom_progress_bar)

- ✅ **metrics.py** (630 lignes) - 7 fonctions :
  - `metric_card_html()` : Carte métrique avec gradient
  - `metric_row()` : Ligne de métriques avec colonnes auto
  - `kpi_card()` : KPI card sophistiquée
  - `comparison_metric()` : Métrique de comparaison avec variation
  - 3 fonctions bonus (mini_metric, stat_card, gauge_metric)

- ✅ **tables.py** (680 lignes) - 7 fonctions :
  - `display_dataframe_formatted()` : DataFrame avec formatage auto dates/nombres
  - `export_buttons()` : Boutons export CSV + Excel
  - `create_summary_table()` : Tableau récapitulatif stylisé HTML
  - `create_comparison_table()` : Tableau comparaison avec variations
  - 3 fonctions bonus (create_table_with_sparklines, create_pivot_table_interface, create_filtered_table)

- ✅ **charts.py** (450 lignes) - 8 fonctions wrappers :
  - `graphique_evolution_semaines()` : Évolution N dernières semaines (tri auto)
  - `graphique_top_categories()` : Top N catégories avec labels
  - `graphique_repartition_regroupements()` : Répartition thématique
  - `graphique_comparaison_semaines()` : Comparaison multi-semaines
  - `graphique_evolution_journaliere()` : Évolution jour par jour
  - `graphique_comparaison_mensuelle()` : Comparaison mensuelle
  - `afficher_graphique()` : Helper d'affichage avec config
  - `graphique_avec_export()` : Graphique + export PNG

- ✅ **__init__.py** : Exports de 35 composants réutilisables

#### Documentation
- ✅ **README.md** : Documentation complète (installation, utilisation, architecture)
- ✅ **ARCHITECTURE.md** : Documentation technique détaillée
- ✅ **CHANGELOG.md** : Historique des versions

### 🔄 Modifié

#### Pages Streamlit (Réduction -53%)
- ✅ **app.py** : 500 → 280 lignes (-44%)
  - Suppression CSS embarqué (150 lignes)
  - Utilisation composants réutilisables
  - Système de logs intégré

- ✅ **pages/1_Vue_Ensemble.py** : 700 → 320 lignes (-54%)
  - Suppression fonction `extraire_numero_semaine()` locale
  - Utilisation `metric_row()` et `comparison_metric()`
  - Intégration `export_buttons()`

- ✅ **pages/2_Analyse_Epidemiologique.py** : 600 → 270 lignes (-55%)
  - Mode comparaison avec `comparer_periodes()`
  - `stat_card()` pour statistiques
  - `info_box()` pour messages

- ✅ **pages/3_Comparaisons.py** : 700 → 310 lignes (-56%)
  - Utilisation `regrouper_par_mois()` centralisée
  - `creer_graphique_variation()` pour barres +/-
  - Comparaisons plus claires

- ✅ **pages/4_Donnees_Brutes.py** : 750 → 370 lignes (-51%)
  - `display_dataframe_formatted()` pour affichage
  - `export_buttons()` pour exports
  - `detecter_fichiers_data()` pour détection auto

- ✅ **pages/5_Generation_Rapports.py** : 650 → 290 lignes (-55%)
  - `modele_selection_card()` pour cartes modèles
  - `info_box()` pour instructions
  - Logs génération avec `log_generation_rapport()`

### 🗑️ Supprimé

- ❌ **CSS dupliqué** : 850 lignes éliminées dans 6 fichiers
  - Remplacé par `config/styles.css` centralisé
  - Un seul appel : `apply_custom_css()`

- ❌ **Fonctions dupliquées** : ~400 lignes
  - `extraire_numero_semaine()` répétée 4 fois → `utils.helpers`
  - `regrouper_par_mois()` répétée 2 fois → `utils.data_processor`
  - Exports CSV/Excel répétés → `utils.helpers`
  - Dictionnaire `mois_fr` répété → `config.settings`

- ❌ **Code HTML manuel** : ~600 lignes
  - Remplacé par composants réutilisables
  - Cartes métriques, headers, footers

### 🔧 Améliorations Techniques

- ⚡ **Performance** :
  - Cache Streamlit optimisé (ttl: 3600s)
  - Chargement lazy des données
  - Formatage optimisé avec regex

- 📝 **Logs** :
  - Rotation automatique (10 MB, 5 backups)
  - 12 fonctions de logging spécialisées
  - Format standardisé avec timestamps

- 🎨 **UI/UX** :
  - Design cohérent avec couleurs Cameroun
  - Animations CSS (fadeIn, slideIn, pulse)
  - Responsive (mobile, tablette, desktop)

- 📦 **Modularité** :
  - Fichiers `__init__.py` pour imports simplifiés
  - 75% de code réutilisable
  - Architecture en 4 couches

### 📊 Statistiques v2.0

| Métrique | v1.0 | v2.0 | Changement |
|----------|------|------|------------|
| **Lignes pages** | 3,900 | 1,840 | **-53%** (-2,060) |
| **CSS dupliqué** | 850 | 0 | **-100%** (-850) |
| **Fonctions dupliquées** | ~20 | 0 | **-100%** (-400) |
| **Modules** | 0 | 4 | **+4** |
| **Fonctions utils** | 0 | 48 | **+48** |
| **Composants** | 0 | 35 | **+35** |
| **Réutilisabilité** | 0% | 75% | **+75%** |
| **Fichiers doc** | 0 | 3 | **+3** |

### 🐛 Corrections

- 🔧 Correction validation dates dans `verifier_coherence_donnees()`
- 🔧 Gestion erreurs améliorée dans chargement données
- 🔧 Format nombres avec espaces (norme française)
- 🔧 Encodage UTF-8-SIG pour exports CSV

---

## [1.0.0] - 2025-11-15

### 🎉 Version Initiale

#### ✨ Ajouté

##### Fonctionnalités Principales
- 🏠 **Page d'accueil** : Vue d'ensemble et statistiques globales
- 👁️ **Vue d'Ensemble** : Analyse dernière semaine épidémiologique
- 🔬 **Analyse Épidémiologique** : Analyse détaillée par semaine
- 📊 **Comparaisons** : Comparaisons temporelles
- 📋 **Données Brutes** : Consultation et export
- 📊 **Génération Rapports** : 3 modèles PowerPoint

##### Analyses
- 📈 **17 catégories d'appels** : CSU, Urgence médicale, Informations, etc.
- 🔵 **5 regroupements thématiques** : Renseignements, Assistances, Signaux, etc.
- 📅 **52 semaines épidémiologiques** : Calendrier 2025 complet
- 📊 **Statistiques globales** : Total, moyenne, min, max, tendances

##### Visualisations
- 📊 Graphiques Plotly interactifs
- 📈 Évolution temporelle
- 🥧 Graphiques camemberts
- 📉 Graphiques en barres
- 🔥 Cartes de chaleur

##### Exports
- 📄 Export CSV (UTF-8)
- 📊 Export Excel (.xlsx)
- 📑 Rapports PowerPoint (3 modèles)

##### Fichiers Initiaux
- `app.py` (500 lignes)
- `config.py` (400 lignes)
- `utils/data_processing.py` (600 lignes)
- `utils/charts.py` (500 lignes)
- `pptx_generator.py` (800 lignes)
- `pptx_generator_advanced.py` (1000 lignes)
- `pages/1_Vue_Ensemble.py` (700 lignes)
- `pages/2_Analyse_Epidemiologique.py` (600 lignes)
- `pages/3_Comparaisons.py` (700 lignes)
- `pages/4_Donnees_Brutes.py` (750 lignes)
- `pages/5_Generation_Rapports.py` (650 lignes)

##### Technologies
- Python 3.12.2
- Streamlit 1.39.0
- Pandas 2.2.3
- Plotly 5.24.1
- python-pptx 1.0.2
- openpyxl 3.1.5

### 🐛 Problèmes Connus v1.0

- ⚠️ CSS dupliqué dans 6 fichiers (850 lignes)
- ⚠️ Fonctions répétées (`extraire_numero_semaine`, `regrouper_par_mois`)
- ⚠️ Pas de système de logs structuré
- ⚠️ Code HTML manuel répété
- ⚠️ Pas de modularité (0% de réutilisabilité)
- ⚠️ Pas de documentation technique

---

## [0.5.0-beta] - 2025-11-01

### 🧪 Version Beta - Tests Internes

#### ✨ Ajouté
- Prototype initial avec 3 pages
- Chargement données Excel basique
- Graphiques Plotly de base
- Export CSV simple

#### 🐛 Corrections
- Correction bugs chargement données
- Amélioration performance graphiques
- Correction exports CSV

---

## Typologie des Changements

- `✨ Ajouté` : Nouvelles fonctionnalités
- `🔄 Modifié` : Changements dans fonctionnalités existantes
- `🗑️ Supprimé` : Fonctionnalités supprimées
- `🐛 Corrections` : Corrections de bugs
- `🔧 Améliorations` : Améliorations techniques
- `📝 Documentation` : Ajouts/modifications documentation
- `⚡ Performance` : Améliorations de performance
- `🔒 Sécurité` : Corrections de vulnérabilités

---

## Roadmap Future

### [2.1.0] - Prévu Q1 2026

#### 🎯 Planifié
- [ ] Tests unitaires (pytest)
- [ ] Tests d'intégration
- [ ] CI/CD avec GitHub Actions
- [ ] Mode sombre (dark mode)
- [ ] Export PDF des graphiques
- [ ] Personnalisation thèmes
- [ ] Multi-langues (FR/EN)

### [3.0.0] - Prévu Q2 2026

#### 🎯 Planifié
- [ ] Base de données (PostgreSQL)
- [ ] API REST (FastAPI)
- [ ] Authentification utilisateurs
- [ ] Gestion des droits (RBAC)
- [ ] Dashboard administrateur
- [ ] Notifications par email
- [ ] Rapports programmés (cron)

---

## Contributions

### Comment Contribuer

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Convention de Commits

Format : `<type>(<scope>): <description>`

**Types :**
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction de bug
- `docs` : Documentation
- `style` : Formatage, CSS
- `refactor` : Refactoring
- `test` : Ajout de tests
- `chore` : Maintenance

**Exemples :**
```
feat(pages): ajouter page analyses avancées
fix(charts): correction affichage graphique camembert
docs(readme): mettre à jour guide installation
refactor(utils): optimiser fonction calcul_totaux
```

---

## Support

- 📧 Email : [votre-email]
- 🔗 Issues : [GitHub Issues](https://github.com/your-repo/issues)
- 📚 Wiki : [GitHub Wiki](https://github.com/your-repo/wiki)

---

## Remerciements

### Version 2.0
- **Fred** : Développement et architecture
- **Christian MOUANGUE** : Supervision technique (Centre Pasteur)
- **Jules TCHATCHUENG** : Supervision technique (Centre Pasteur)
- **Dr. Antem Yolande Ebude EBONG** : Supervision académique (AIMS)
- **MINSANTE** : Cahier des charges et validation
- **Communauté Streamlit** : Support technique

### Version 1.0
- **AIMS-Cameroun** : Formation et encadrement
- **Centre Pasteur du Cameroun** : Données et expertise
- **CCOUSP/MINSANTE** : Plateforme et retours

---

**Maintenu par : Fred - AIMS Cameroon / MINSANTE**  
**Dernière mise à jour : 2025-12-04**  
**Licence : MIT**