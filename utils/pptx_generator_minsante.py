"""
==============================================================================
GÉNÉRATEUR DE PRÉSENTATIONS POWERPOINT - MODÈLE MINSANTE
==============================================================================
Module pour générer automatiquement des présentations PowerPoint
suivant le modèle officiel du Centre d'Appels d'Urgence MINSANTE.

VERSION FINALE - Code original (document 3) + Wrapper pour nouvelle architecture

Auteur: Fred - AIMS Cameroon / MINSANTE
Date: Décembre 2025
==============================================================================
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.dml import MSO_THEME_COLOR
from datetime import datetime
import pandas as pd
import io
from pathlib import Path
from PIL import Image


class MinsantePPTXGenerator:
    """Classe pour générer des présentations PowerPoint selon le modèle MINSANTE."""
    
    def __init__(self, template_path=None, drapeau_path=None):
        """
        Initialise le générateur de présentation.
        
        Args:
            template_path (str): Chemin vers le template .pptx (optionnel)
            drapeau_path (str): Chemin vers l'image du drapeau (optionnel)
        """
        if template_path:
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()
            self.prs.slide_width = Inches(13.33)
            self.prs.slide_height = Inches(7.5)
        
        # Chemin du drapeau - chercher dans plusieurs emplacements
        if drapeau_path and Path(drapeau_path).exists():
            self.drapeau_path = Path(drapeau_path)
        else:
            # Chercher dans data/, assets/, uploads/
            possible_paths = [
                Path(__file__).parent.parent / "data" / "Flag_of_Cameroon.svg",
                Path(__file__).parent.parent / "data" / "Flag_of_Cameroon.png",
                Path(__file__).parent.parent / "assets" / "Flag_of_Cameroon.svg",
                Path(__file__).parent.parent / "assets" / "Flag_of_Cameroon.png",
                Path("/mnt/user-data/uploads/Flag_of_Cameroon.svg"),
                Path("/mnt/user-data/uploads/Flag_of_Cameroon.png"),
            ]
            
            self.drapeau_path = None
            for path in possible_paths:
                if path.exists():
                    self.drapeau_path = path
                    print(f"✅ Drapeau trouvé : {path}")
                    break
            
            if not self.drapeau_path:
                print("⚠️ Drapeau non trouvé, utilisation d'un placeholder")
        
        # Couleurs du thème MINSANTE/Cameroun
        self.color_vert = RGBColor(0, 122, 51)         # Vert Cameroun
        self.color_jaune = RGBColor(255, 215, 0)       # Jaune Cameroun
        self.color_rouge = RGBColor(206, 17, 38)       # Rouge Cameroun
        self.color_white = RGBColor(255, 255, 255)
        self.color_dark = RGBColor(33, 37, 41)
        self.color_gray = RGBColor(108, 117, 125)
        self.color_lightgray = RGBColor(233, 236, 239)
        self.color_blue = RGBColor(13, 110, 253)
    
    def _convertir_svg_en_png(self, svg_path):
        """
        Convertit un fichier SVG en PNG.
        
        Args:
            svg_path (Path): Chemin vers le fichier SVG
        
        Returns:
            BytesIO: Image PNG en bytes
        """
        try:
            import cairosvg
            # Convertir SVG en PNG avec cairosvg
            png_data = cairosvg.svg2png(
                url=str(svg_path),
                output_width=800,
                output_height=533
            )
            return io.BytesIO(png_data)
        
        except ImportError:
            print("⚠️ cairosvg non installé, tentative avec PIL")
            try:
                from PIL import Image
                img = Image.open(svg_path)
                img = img.resize((800, 533), Image.Resampling.LANCZOS)
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                return img_bytes
            except Exception as e:
                print(f"❌ Erreur PIL : {e}")
                return None
        
        except Exception as e:
            print(f"❌ Erreur lors de la conversion SVG: {e}")
            return None
    
    def _obtenir_image_drapeau(self):
        """
        Obtient l'image du drapeau (SVG ou PNG).
        
        Returns:
            BytesIO: Image du drapeau en bytes
        """
        if not self.drapeau_path or not self.drapeau_path.exists():
            print("⚠️ Fichier du drapeau introuvable")
            return None
        
        # Si c'est un SVG, le convertir en PNG
        if self.drapeau_path.suffix.lower() == '.svg':
            return self._convertir_svg_en_png(self.drapeau_path)
        
        # Si c'est déjà un PNG/JPG, le lire directement
        else:
            try:
                with open(self.drapeau_path, 'rb') as f:
                    return io.BytesIO(f.read())
            except Exception as e:
                print(f"❌ Erreur lecture image : {e}")
                return None
    
    def slide_1_titre(self, date_rapport):
        """Génère la Slide 1 : Page de titre avec drapeau du Cameroun"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Ajouter le vrai drapeau du Cameroun
        drapeau_bytes = self._obtenir_image_drapeau()
        
        if drapeau_bytes:
            try:
                left_drapeau = Inches(7.5)
                top_drapeau = Inches(1.5)
                width_drapeau = Inches(5.0)
                
                pic = slide.shapes.add_picture(
                    drapeau_bytes,
                    left_drapeau,
                    top_drapeau,
                    width=width_drapeau
                )
                print("✅ Drapeau ajouté à la slide 1")
            except Exception as e:
                print(f"❌ Erreur lors de l'ajout du drapeau: {e}")
        else:
            print("⚠️ Drapeau non ajouté - fichier introuvable ou erreur de conversion")
        
        # Bande verte en haut
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(0.8))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Logo/Titre MINSANTE dans la bande verte
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(8), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "MINISTÈRE DE LA SANTÉ PUBLIQUE - RÉPUBLIQUE DU CAMEROUN"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        p.alignment = PP_ALIGN.LEFT
        
        # Titre principal - SITUATION
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(6.0), Inches(1.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = "SITUATION"
        run.font.size = Pt(60)
        run.font.bold = True
        run.font.color.rgb = self.color_vert
        
        # Sous-titre - DU CENTRE D'APPELS
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(3.5), Inches(6.5), Inches(2.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = "DU CENTRE D'APPELS\nD'URGENCE SANITAIRE\n"
        run.font.size = Pt(36)
        run.font.bold = True
        run.font.color.rgb = self.color_dark
        
        # Date du rapport
        p2 = tf.add_paragraph()
        run2 = p2.add_run()
        run2.text = f"\nau {date_rapport}"
        run2.font.size = Pt(28)
        run2.font.bold = False
        run2.font.color.rgb = self.color_rouge
        
        # Pied de page
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(6.8), Inches(12.33), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "Centre d'Appels d'Urgence Sanitaire - Numéro d'urgence : 1510"
        p.font.size = Pt(14)
        p.font.color.rgb = self.color_gray
        p.alignment = PP_ALIGN.CENTER
    
    def slide_2_faits_saillants(self, periode, total_appels, 
                                 renseignements_data, assistance_data, 
                                 signaux_data, autres_data):
        """Génère la Slide 2 : Faits saillants avec graphiques"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Bande verte en haut avec titre
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Titre dans la bande
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.6))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"FAITS SAILLANTS DU {periode.upper()}"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        p.alignment = PP_ALIGN.CENTER
        
        # Texte principal - Total des appels
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(12), Inches(0.6))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"📞 {total_appels:,} NOUVEAUX APPELS REÇUS".replace(",", " ")
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = self.color_rouge
        p.alignment = PP_ALIGN.CENTER
        
        # Statistiques textuelles
        total_renseignements = sum(renseignements_data.values()) if renseignements_data else 0
        total_assistance = sum(assistance_data.values()) if assistance_data else 0
        total_signaux = sum(signaux_data.values()) if signaux_data else 0
        
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(12), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        stats_text = f"🏥 {total_renseignements} Renseignements Santé  |  "
        stats_text += f"🚑 {total_assistance} Assistances Médicales  |  "
        stats_text += f"📡 {total_signaux} Signaux de Surveillance"
        p.text = stats_text
        p.font.size = Pt(16)
        p.font.color.rgb = self.color_dark
        p.alignment = PP_ALIGN.CENTER
        
        # Ligne de séparation
        shape = slide.shapes.add_shape(1, Inches(1.5), Inches(2.6), Inches(10.33), Inches(0.02))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_jaune
        shape.line.fill.background()
        
        # Graphiques - TOUJOURS générés
        if renseignements_data:
            self._ajouter_graphique_camembert(
                slide, renseignements_data,
                left=Inches(0.8), top=Inches(3.0), width=Inches(3.8), height=Inches(3.8),
                titre="🏥 Renseignements Santé", couleur=self.color_vert
            )
        
        if assistance_data:
            self._ajouter_graphique_camembert(
                slide, assistance_data,
                left=Inches(4.8), top=Inches(3.0), width=Inches(3.8), height=Inches(3.8),
                titre="🚑 Assistances Médicales", couleur=self.color_rouge
            )
        
        if signaux_data:
            self._ajouter_graphique_camembert(
                slide, signaux_data,
                left=Inches(8.8), top=Inches(3.0), width=Inches(3.8), height=Inches(3.8),
                titre="📡 Signaux de Surveillance", couleur=self.color_blue
            )
        
        # Appels sortants (pied de page)
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(12), Inches(0.3))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"📞 {autres_data.get('appels_sortants', 0)} appel(s) sortant(s) émis  |  ⚠️ {autres_data.get('total', 0)} autres appels"
        p.font.size = Pt(14)
        p.font.color.rgb = self.color_gray
        p.alignment = PP_ALIGN.CENTER
    
    def _ajouter_graphique_camembert(self, slide, data_dict, left, top, width, height, titre="", couleur=None):
        """Ajoute un graphique camembert professionnel."""
        if not data_dict or sum(data_dict.values()) == 0:
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = f"{titre}\n\nAucune donnée disponible"
            p.font.size = Pt(14)
            p.font.color.rgb = self.color_gray
            p.alignment = PP_ALIGN.CENTER
            return
        
        # Ajouter le titre au-dessus du graphique
        txBox = slide.shapes.add_textbox(left, top - Inches(0.3), width, Inches(0.25))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = titre
        p.font.size = Pt(14)
        p.font.bold = True
        if couleur:
            p.font.color.rgb = couleur
        else:
            p.font.color.rgb = self.color_dark
        p.alignment = PP_ALIGN.CENTER
        
        # Créer les données du graphique
        chart_data = CategoryChartData()
        chart_data.categories = list(data_dict.keys())
        chart_data.add_series('Série 1', list(data_dict.values()))
        
        # Ajouter le graphique
        graphic_frame = slide.shapes.add_chart(
            XL_CHART_TYPE.PIE, left, top, width, height, chart_data
        )
        
        chart = graphic_frame.chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.font.size = Pt(9)
        chart.legend.include_in_layout = False
        
        if chart.has_title:
            chart.chart_title.text_frame.clear()
            chart.has_title = False
        
        plot = chart.plots[0]
        plot.has_data_labels = True
        data_labels = plot.data_labels
        data_labels.font.size = Pt(10)
        data_labels.font.bold = True
        data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    
    def slide_3_comparaison(self, semaine1, semaine2, df_comparaison):
        """Génère la Slide 3 : Tableau de comparaison entre 2 semaines"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Bande verte en haut avec titre
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Titre
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12), Inches(0.7))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"COMPARAISON DES APPELS"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        p.alignment = PP_ALIGN.CENTER
        
        # Sous-titre avec les semaines
        txBox = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.33), Inches(0.4))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"📊 {semaine1} vs {semaine2}"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = self.color_rouge
        p.alignment = PP_ALIGN.CENTER
        
        # Créer le tableau
        rows = len(df_comparaison) + 1
        cols = len(df_comparaison.columns)
        
        table = slide.shapes.add_table(rows, cols, Inches(1.5), Inches(1.9), Inches(10.33), Inches(5.0)).table
        
        # Ajuster la largeur des colonnes dynamiquement
        if cols == 3:
            table.columns[0].width = Inches(6.0)
            table.columns[1].width = Inches(2.16)
            table.columns[2].width = Inches(2.16)
        else:
            col_width = Inches(10.33 / cols)
            for i in range(cols):
                table.columns[i].width = col_width
        
        # En-têtes
        for col_idx, col_name in enumerate(df_comparaison.columns):
            cell = table.cell(0, col_idx)
            cell.text = str(col_name)
            cell.fill.solid()
            cell.fill.fore_color.rgb = self.color_vert
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)
            
            paragraph = cell.text_frame.paragraphs[0]
            paragraph.font.bold = True
            paragraph.font.size = Pt(13)
            paragraph.font.color.rgb = self.color_white
            paragraph.alignment = PP_ALIGN.CENTER
        
        # Données
        for row_idx, row in df_comparaison.iterrows():
            for col_idx, col_name in enumerate(df_comparaison.columns):
                cell = table.cell(row_idx + 1, col_idx)
                cell.text = str(row[col_name])
                cell.margin_top = Inches(0.05)
                cell.margin_bottom = Inches(0.05)
                
                if row_idx % 2 == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(248, 249, 250)
                
                paragraph = cell.text_frame.paragraphs[0]
                paragraph.font.size = Pt(11)
                paragraph.font.color.rgb = self.color_dark
                
                if col_idx == 0:
                    paragraph.font.bold = True
                    paragraph.alignment = PP_ALIGN.LEFT
                else:
                    paragraph.alignment = PP_ALIGN.CENTER
    
    def _trier_semaines(self, semaines, valeurs):
        """Trie les semaines par ordre chronologique (S1, S2, S3, ...)."""
        def extraire_numero(semaine_label):
            try:
                return int(semaine_label.split('_')[0][1:])
            except:
                return 0
        
        couples = list(zip(semaines, valeurs))
        couples_tries = sorted(couples, key=lambda x: extraire_numero(x[0]))
        semaines_triees = [c[0] for c in couples_tries]
        valeurs_triees = [c[1] for c in couples_tries]
        
        return semaines_triees, valeurs_triees
    
    def slide_4_evolution(self, semaines, valeurs, titre_periode=""):
        """Génère la Slide 4 : Graphique d'évolution en colonnes"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        semaines_triees, valeurs_triees = self._trier_semaines(semaines, valeurs)
        
        if not titre_periode and semaines_triees:
            titre_periode = f"{semaines_triees[0]} à {semaines_triees[-1]}"
        
        print(f"📈 Graphique d'évolution : {len(semaines_triees)} semaines de {semaines_triees[0]} à {semaines_triees[-1]}")
        
        # Bande verte en haut avec titre
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Titre
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12), Inches(0.7))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"ÉVOLUTION DES APPELS"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        p.alignment = PP_ALIGN.CENTER
        
        # Sous-titre avec période
        txBox = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.33), Inches(0.4))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"📈 Période : {titre_periode}"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = self.color_rouge
        p.alignment = PP_ALIGN.CENTER
        
        # Créer les données du graphique
        chart_data = CategoryChartData()
        chart_data.categories = semaines_triees
        chart_data.add_series('Nombre d\'appels', valeurs_triees)
        
        # Ajouter le graphique en colonnes
        graphic_frame = slide.shapes.add_chart(
            XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.9), Inches(11.73), Inches(5.2), chart_data
        )
        
        chart = graphic_frame.chart
        chart.has_legend = False
        
        if chart.has_title:
            chart.chart_title.text_frame.clear()
            chart.has_title = False
        
        series = chart.series[0]
        fill = series.format.fill
        fill.solid()
        fill.fore_color.rgb = self.color_vert
        
        value_axis = chart.value_axis
        value_axis.has_major_gridlines = True
        
        category_axis = chart.category_axis
        category_axis.tick_labels.font.size = Pt(9)
    
    def slide_5_questions_interet(self, periode, questions_list):
        """Génère la Slide 5 : Questions d'intérêt posées"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Bande verte en haut avec titre
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Titre
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(12), Inches(0.7))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"QUESTIONS D'INTÉRÊT POSÉES AU 1510"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        p.alignment = PP_ALIGN.CENTER
        
        # Sous-titre avec période
        txBox = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.33), Inches(0.4))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"📅 Période : {periode}"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = self.color_rouge
        p.alignment = PP_ALIGN.CENTER
        
        # Zone de texte pour les questions
        txBox = slide.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.33), Inches(4.8))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        for i, question in enumerate(questions_list, 1):
            if i > 1:
                p = tf.add_paragraph()
            else:
                p = tf.paragraphs[0]
            
            p.text = f"{i}. {question}"
            p.font.size = Pt(15)
            p.font.color.rgb = self.color_dark
            p.space_before = Pt(12)
            p.space_after = Pt(12)
            p.line_spacing = 1.3
            p.level = 0
    
    def slide_6_activites(self, activites_menees, activites_planifiees):
        """Génère la Slide 6 : Activités menées et planifiées"""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Bande verte en haut avec titre
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Titre
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.6))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "ACTIVITÉS MENÉES ET PLANIFIÉES"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        p.alignment = PP_ALIGN.CENTER
        
        # Créer le tableau 2x2
        table = slide.shapes.add_table(2, 2, Inches(1.0), Inches(1.5), Inches(11.33), Inches(5.5)).table
        
        table.columns[0].width = Inches(5.665)
        table.columns[1].width = Inches(5.665)
        
        # En-têtes
        headers = ["✅ ACTIVITÉS MENÉES", "📋 ACTIVITÉS PLANIFIÉES"]
        for col_idx, header_text in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.text = header_text
            cell.fill.solid()
            cell.fill.fore_color.rgb = self.color_vert
            cell.margin_top = Inches(0.1)
            cell.margin_bottom = Inches(0.1)
            
            paragraph = cell.text_frame.paragraphs[0]
            paragraph.font.bold = True
            paragraph.font.size = Pt(16)
            paragraph.font.color.rgb = self.color_white
            paragraph.alignment = PP_ALIGN.CENTER
        
        # Contenu - Activités menées
        cell_menees = table.cell(1, 0)
        cell_menees.margin_left = Inches(0.15)
        cell_menees.margin_right = Inches(0.15)
        cell_menees.margin_top = Inches(0.15)
        
        tf = cell_menees.text_frame
        tf.clear()
        
        for i, activite in enumerate(activites_menees):
            if i > 0:
                p = tf.add_paragraph()
            else:
                p = tf.paragraphs[0]
            p.text = f"• {activite}"
            p.font.size = Pt(13)
            p.font.color.rgb = self.color_dark
            p.space_before = Pt(8)
            p.space_after = Pt(8)
        
        # Contenu - Activités planifiées
        cell_planifiees = table.cell(1, 1)
        cell_planifiees.margin_left = Inches(0.15)
        cell_planifiees.margin_right = Inches(0.15)
        cell_planifiees.margin_top = Inches(0.15)
        
        tf = cell_planifiees.text_frame
        tf.clear()
        
        for i, activite in enumerate(activites_planifiees):
            if i > 0:
                p = tf.add_paragraph()
            else:
                p = tf.paragraphs[0]
            p.text = f"• {activite}"
            p.font.size = Pt(13)
            p.font.color.rgb = self.color_dark
            p.space_before = Pt(8)
            p.space_after = Pt(8)
    
    def slide_7_merci(self):
        """Génère la Slide 7 : Slide de remerciement."""
        slide_layout = self.prs.slide_layouts[6]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Fond avec dégradé vert
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = self.color_vert
        shape.line.fill.background()
        
        # Texte MERCI
        txBox = slide.shapes.add_textbox(Inches(2), Inches(2.0), Inches(9.33), Inches(2.0))
        tf = txBox.text_frame
        tf.text = "MERCI"
        
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(90)
        p.font.bold = True
        p.font.color.rgb = self.color_white
        
        # Sous-texte
        txBox = slide.shapes.add_textbox(Inches(2), Inches(4.2), Inches(9.33), Inches(1.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = "Pour votre attention"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(28)
        p.font.color.rgb = self.color_jaune
        
        p2 = tf.add_paragraph()
        p2.text = "\nCentre d'Appels d'Urgence Sanitaire - 1510"
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(18)
        p2.font.color.rgb = self.color_white
    
    def sauvegarder(self, nom_fichier="Situation_Centre_Appel.pptx"):
        """Sauvegarde la présentation."""
        pptx_stream = io.BytesIO()
        self.prs.save(pptx_stream)
        pptx_stream.seek(0)
        return pptx_stream.getvalue()


# ==============================================================================
# FONCTION ORIGINALE (pour compatibilité avec ancien code)
# ==============================================================================

def generer_rapport_minsante_old(donnees, date_rapport, periode_faits, drapeau_path=None):
    """
    Fonction ORIGINALE - pour compatibilité.
    Signature: generer_rapport_minsante(donnees, date_rapport, periode_faits, drapeau_path)
    """
    gen = MinsantePPTXGenerator(drapeau_path=drapeau_path)
    
    # Slide 1
    gen.slide_1_titre(date_rapport)
    
    # Slide 2
    gen.slide_2_faits_saillants(
        periode=periode_faits,
        total_appels=donnees.get('total_appels', 0),
        renseignements_data=donnees.get('renseignements', {}),
        assistance_data=donnees.get('assistance', {}),
        signaux_data=donnees.get('signaux', {}),
        autres_data=donnees.get('autres', {})
    )
    
    # Slide 3
    if 'df_comparaison' in donnees:
        gen.slide_3_comparaison(
            semaine1=donnees.get('semaine1', ''),
            semaine2=donnees.get('semaine2', ''),
            df_comparaison=donnees['df_comparaison']
        )
    
    # Slide 4
    if 'semaines' in donnees and 'valeurs_evolution' in donnees:
        semaines = donnees['semaines']
        if semaines:
            def extraire_numero(s):
                try:
                    return int(s.split('_')[0][1:])
                except:
                    return 0
            semaines_triees = sorted(semaines, key=extraire_numero)
            titre_periode = donnees.get('titre_evolution', f"{semaines_triees[0]} à {semaines_triees[-1]}")
        else:
            titre_periode = donnees.get('titre_evolution', '')
        
        gen.slide_4_evolution(
            semaines=semaines,
            valeurs=donnees['valeurs_evolution'],
            titre_periode=titre_periode
        )
    
    # Slide 5
    if 'questions' in donnees:
        gen.slide_5_questions_interet(
            periode=donnees.get('periode_questions', periode_faits),
            questions_list=donnees['questions']
        )
    
    # Slide 6
    if 'activites_menees' in donnees and 'activites_planifiees' in donnees:
        gen.slide_6_activites(
            activites_menees=donnees['activites_menees'],
            activites_planifiees=donnees['activites_planifiees']
        )
    
    # Slide 7
    gen.slide_7_merci()
    
    return gen.sauvegarder()


# ==============================================================================
# FONCTION WRAPPER POUR NOUVELLE ARCHITECTURE
# ==============================================================================

def generer_rapport_minsante(df_appels, df_calendrier, semaine, output_path):
    """
    Wrapper pour la NOUVELLE ARCHITECTURE.
    Signature: generer_rapport_minsante(df_appels, df_calendrier, semaine, output_path)
    
    Convertit les nouveaux paramètres vers l'ancien format.
    """
    from utils.data_processor import (
        calculer_totaux_semaine, 
        calculer_regroupements,
        calculer_totaux_hebdomadaires,
        comparer_periodes
    )
    from config import settings
    
    print(f"🎯 Génération rapport MINSANTE pour {semaine}...")
    
    # Calculer les données de la semaine
    totaux = calculer_totaux_semaine(df_appels, semaine)
    df_semaine = df_appels[df_appels['Semaine épidémiologique'] == semaine]
    
    # Préparer les données pour les graphiques camembert
    renseignements_data = {}
    if 'RENSEIGNEMENTS' in settings.REGROUPEMENTS:
        for cat in settings.REGROUPEMENTS['RENSEIGNEMENTS']:
            if cat in df_semaine.columns:
                val = int(df_semaine[cat].sum())
                if val > 0:
                    label = settings.LABELS_CATEGORIES.get(cat, cat)
                    renseignements_data[label] = val
    
    assistance_data = {}
    if 'ASSISTANCES' in settings.REGROUPEMENTS:
        for cat in settings.REGROUPEMENTS['ASSISTANCES']:
            if cat in df_semaine.columns:
                val = int(df_semaine[cat].sum())
                if val > 0:
                    label = settings.LABELS_CATEGORIES.get(cat, cat)
                    assistance_data[label] = val
    
    signaux_data = {}
    if 'SIGNAUX' in settings.REGROUPEMENTS:
        for cat in settings.REGROUPEMENTS['SIGNAUX']:
            if cat in df_semaine.columns:
                val = int(df_semaine[cat].sum())
                if val > 0:
                    label = settings.LABELS_CATEGORIES.get(cat, cat)
                    signaux_data[label] = val
    
    # Préparer le dictionnaire de données (ancien format)
    donnees = {
        'total_appels': totaux['total'],
        'renseignements': renseignements_data,
        'assistance': assistance_data,
        'signaux': signaux_data,
        'autres': {
            'appels_sortants': 0,
            'total': totaux['total']
        }
    }
    
    # Ajouter la comparaison
    try:
        semaines_disponibles = sorted(df_appels['Semaine épidémiologique'].unique())
        idx_actuelle = semaines_disponibles.index(semaine)
        
        if idx_actuelle > 0:
            semaine_precedente = semaines_disponibles[idx_actuelle - 1]
            df_comparaison = comparer_periodes(df_appels, [semaine_precedente, semaine])
            donnees['df_comparaison'] = df_comparaison
            donnees['semaine1'] = semaine_precedente
            donnees['semaine2'] = semaine
    except Exception as e:
        print(f"⚠️ Pas de comparaison disponible: {e}")
    
    # Ajouter l'évolution
    try:
        df_hebdo = calculer_totaux_hebdomadaires(df_appels)
        semaines = df_hebdo['Semaine épidémiologique'].tolist()
        valeurs = df_hebdo['TOTAL_APPELS_SEMAINE'].tolist()
        
        donnees['semaines'] = semaines
        donnees['valeurs_evolution'] = valeurs
    except Exception as e:
        print(f"⚠️ Pas d'évolution disponible: {e}")
    
    # Ajouter les questions d'intérêt
    donnees['questions'] = [
        "Qu'elle est la durée de validité d'une carte CSU ?",
        "Est ce qu'on peut avoir une CSU avant d'accoucher ?",
        "Combien coûte une carte CSU ?",
        "Quel est le délai pour recevoir la carte CSU ?",
        "Puis-je utiliser ma carte CSU dans toutes les structures de santé ?"
    ]
    
    # Ajouter les activités
    donnees['activites_menees'] = [
        "Formation des opérateurs sur la gestion des appels d'urgence",
        "Mise à jour de la base de données des centres de santé",
        "Coordination avec les équipes de surveillance épidémiologique",
        "Analyse des tendances hebdomadaires des appels"
    ]
    
    donnees['activites_planifiees'] = [
        "Extension de la couverture géographique du service 1510",
        "Intégration d'un système de triage automatisé",
        "Formation continue sur les nouvelles pathologies émergentes",
        "Évaluation de la satisfaction des usagers"
    ]
    
    # Préparer les dates
    date_rapport = totaux['date_fin'].strftime("%d %B %Y")
    periode_faits = f"{totaux['date_debut'].strftime('%d')} au {totaux['date_fin'].strftime('%d %B %Y')}"
    
    # Générer le rapport en appelant la fonction ORIGINALE
    pptx_bytes = generer_rapport_minsante_old(donnees, date_rapport, periode_faits)
    
    # Sauvegarder
    with open(output_path, 'wb') as f:
        f.write(pptx_bytes)
    
    print(f"✅ Rapport MINSANTE généré : {output_path}")
    print(f"📊 7 slides complètes")
    
    return output_path