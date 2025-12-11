"""
==============================================================================
COMPOSANT : SIDEBAR MINIMALISTE
==============================================================================
Sidebar ultra-simple avec logo et footer CCOUSP/MINSANTE.

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
Version: 3.0 FINALE
==============================================================================
"""

import streamlit as st
from config import settings

def render_sidebar(page_info=None):
    """
    Affiche la sidebar minimaliste avec footer CCOUSP/MINSANTE.
    
    Args:
        page_info (dict, optional): Contenu personnalisé (rarement utilisé)
    
    Example:
        >>> render_sidebar()
    """
    
    with st.sidebar:
        # ==================== CONTENU PERSONNALISÉ (optionnel) ====================
        if page_info and 'content' in page_info and callable(page_info['content']):
            page_info['content']()
            st.markdown("---")
        
        # ==================== SPACER FLEXIBLE ====================
        st.markdown("<div style='flex: 1; min-height: 60vh;'></div>", unsafe_allow_html=True)
        
        # ==================== FOOTER ====================
        st.markdown(f"""
            <div class="sidebar-footer">
                <div style="text-align: center; padding: 0.8rem 0;">
                    <div style="color: #007A33; font-size: 0.95rem; font-weight: 700; line-height: 1.4;">
                        {settings.DRAPEAU_CAMEROUN} DASHBOARD 1510
                    </div>
                    <div style="color: #007A33; font-size: 0.95rem; font-weight: 700; margin-top: 0.3rem;">
                        CCOUSP / MINSANTE
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)