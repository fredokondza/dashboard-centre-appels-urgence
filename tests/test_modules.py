"""
==============================================================================
SCRIPT DE TEST DES MODULES
==============================================================================
Ce script teste que tous les modules s'importent correctement.

Usage:
    python test_modules.py

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
==============================================================================
"""

import sys
from pathlib import Path

# Ajouter le projet au path
sys.path.insert(0, str(Path(__file__).parent))

def test_config():
    """Test du module config."""
    print("📦 Test module config...")
    try:
        from config import settings
        from config import APP_CONFIG, CATEGORIES_APPELS, COULEURS_CAMEROUN
        
        assert APP_CONFIG is not None
        assert len(CATEGORIES_APPELS) == 17
        assert 'vert' in COULEURS_CAMEROUN
        
        print("✅ Config OK")
        return True
    except Exception as e:
        print(f"❌ Config ERREUR: {e}")
        return False

def test_utils():
    """Test du module utils."""
    print("\n📦 Test module utils...")
    try:
        from utils import (
            charger_toutes_les_donnees,
            calculer_totaux_semaine,
            formater_nombre,
            extraire_numero_semaine,
            setup_logger
        )
        
        # Tests de base
        assert formater_nombre(15234) == '15 234'
        assert extraire_numero_semaine('S10_2025') == 10
        
        print("✅ Utils OK")
        return True
    except Exception as e:
        print(f"❌ Utils ERREUR: {e}")
        return False

def test_components():
    """Test du module components."""
    print("\n📦 Test module components...")
    try:
        from components import (
            apply_custom_css,
            page_header,
            metric_row,
            export_buttons
        )
        
        print("✅ Components OK")
        return True
    except Exception as e:
        print(f"❌ Components ERREUR: {e}")
        return False

def test_imports_pages():
    """Test que les pages peuvent importer les modules."""
    print("\n📦 Test imports pages...")
    try:
        # Simuler les imports d'une page
        from config import settings
        from utils import charger_toutes_les_donnees
        from components import page_header, metric_row
        
        print("✅ Imports pages OK")
        return True
    except Exception as e:
        print(f"❌ Imports pages ERREUR: {e}")
        return False

def test_all():
    """Lance tous les tests."""
    print("="*60)
    print("🧪 TESTS DES MODULES - Dashboard Urgence 1510")
    print("="*60)
    
    results = []
    
    # Tests individuels
    results.append(("Config", test_config()))
    results.append(("Utils", test_utils()))
    results.append(("Components", test_components()))
    results.append(("Imports Pages", test_imports_pages()))
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    failed = total - passed
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "-"*60)
    print(f"Total: {total} tests")
    print(f"✅ Réussis: {passed}")
    print(f"❌ Échoués: {failed}")
    
    if failed == 0:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ Les modules sont prêts à être utilisés")
        return True
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Vérifiez les erreurs ci-dessus")
        return False

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)