"""
Script de migration automatique pour appliquer la sidebar
minimaliste avec footer CCOUSP/MINSANTE à TOUTES les pages.

Usage: python migrate_sidebar_final.py
"""

import os
import re

# Fichiers à migrer
FILES = [
    'app.py',
    'pages/1_Vue_Ensemble.py',
    'pages/2_Analyse_Epidemiologique.py',
    'pages/3_Comparaisons.py',
    'pages/4_Donnees_Brutes.py',
    'pages/5_Generation_Rapports.py'
]

def migrate_file(filepath):
    """Migre un fichier pour utiliser render_sidebar()."""
    
    print(f"\n📄 {filepath}")
    
    if not os.path.exists(filepath):
        print(f"   ⚠️  Fichier introuvable")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Ajouter l'import
    if 'from components.sidebar import render_sidebar' not in content:
        # Chercher la ligne avec components.layout
        match = re.search(r'(from components\.layout import.*?\n)', content)
        if match:
            pos = match.end()
            content = content[:pos] + 'from components.sidebar import render_sidebar\n' + content[pos:]
            print("   ✅ Import ajouté")
        else:
            # Si pas de components.layout, ajouter après les imports
            match = re.search(r'(^from .+? import .+?\n)(?=\n)', content, re.MULTILINE)
            if match:
                pos = match.end()
                content = content[:pos] + 'from components.sidebar import render_sidebar\n' + content[pos:]
                print("   ✅ Import ajouté")
    
    # 2. Remplacer le bloc with st.sidebar par render_sidebar()
    # Pattern pour capturer tout le bloc sidebar
    pattern = r'# ?=+ ?SIDEBAR.*?\n.*?with st\.sidebar:.*?(?=\n# ?=+|$)'
    
    if re.search(pattern, content, re.DOTALL):
        # Trouver l'indentation
        match = re.search(r'^(\s*)with st\.sidebar:', content, re.MULTILINE)
        if match:
            indent = match.group(1)
            replacement = (
                f"\n{indent}# ==================== SIDEBAR ====================\n"
                f"{indent}render_sidebar()\n"
            )
            content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)
            print("   ✅ Sidebar remplacée")
    else:
        # Chercher juste "with st.sidebar:"
        pattern2 = r'with st\.sidebar:.*?(?=\n(?:st\.|page_header|#\s*=+|[a-z_]+\s*=))'
        if re.search(pattern2, content, re.DOTALL):
            match = re.search(r'^(\s*)with st\.sidebar:', content, re.MULTILINE)
            if match:
                indent = match.group(1)
                replacement = (
                    f"{indent}# ==================== SIDEBAR ====================\n"
                    f"{indent}render_sidebar()\n"
                )
                content = re.sub(pattern2, replacement, content, flags=re.DOTALL)
                print("   ✅ Sidebar remplacée")
    
    # 3. Sauvegarder
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   💾 Fichier sauvegardé")
        return True
    else:
        print("   ℹ️  Aucune modification")
        return False

def main():
    print("🚀 MIGRATION SIDEBAR MINIMALISTE + CCOUSP/MINSANTE")
    print("=" * 60)
    
    migrated = 0
    for filepath in FILES:
        if migrate_file(filepath):
            migrated += 1
    
    print("\n" + "=" * 60)
    print(f"✅ {migrated}/{len(FILES)} fichiers migrés")
    print("\n📋 PROCHAINES ÉTAPES :")
    print("   1. Tester : streamlit run app.py")
    print("   2. Vérifier toutes les pages")
    print("   3. Supprimer ce script si OK")

if __name__ == "__main__":
    main()