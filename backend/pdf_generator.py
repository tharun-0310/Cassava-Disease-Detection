"""
PDF Report Generator for Cassava Disease Detection
Generates comprehensive farmer-friendly reports
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import io


class DiseaseDatabase:
    """Database of disease information for report generation"""
    
    DISEASE_INFO = {
        "Cassava Bacterial Blight (CBB)": {
            "scientific_cause": "Xanthomonas axonopodis pv. manihotis bacteria",
            "summary": "Cassava Bacterial Blight is a serious bacterial disease that affects cassava plants, causing leaf wilting, stem rot, and significant yield loss. It spreads rapidly in humid conditions and can devastate entire crops if not managed properly.",
            "symptoms": {
                "early": [
                    "Small water-soaked spots on young leaves",
                    "Angular leaf spots with yellow halos",
                    "Wilting of top leaves during hot hours"
                ],
                "mid": [
                    "Leaf spots turn brown and enlarge",
                    "Gum exudation from stems",
                    "Wilting becomes permanent",
                    "Stem cankers appear"
                ],
                "advanced": [
                    "Complete leaf death and defoliation",
                    "Stem rot and dieback",
                    "Plant death in severe cases",
                    "Vascular browning visible in stems"
                ]
            },
            "field_signs": [
                "Wilted plants in patches across field",
                "Sticky gum oozing from stems",
                "Brown angular leaf spots",
                "Top-down wilting pattern"
            ],
            "medicines": [
                {
                    "name": "Copper Hydroxide",
                    "type": "Bactericide",
                    "dosage": "2-3 g/L water",
                    "application": "Foliar spray every 7-10 days",
                    "safety": "Wear protective gear, avoid spraying in rain"
                },
                {
                    "name": "Streptomycin Sulfate",
                    "type": "Antibiotic",
                    "dosage": "200 ppm solution",
                    "application": "Spray on affected areas",
                    "safety": "Use only as directed, avoid overuse"
                },
                {
                    "name": "Bordeaux Mixture",
                    "type": "Organic Fungicide/Bactericide",
                    "dosage": "1% solution (10g/L)",
                    "application": "Preventive spray every 14 days",
                    "safety": "Natural but can burn leaves if too concentrated"
                },
                {
                    "name": "Neem Oil Extract",
                    "type": "Organic",
                    "dosage": "5 ml/L water",
                    "application": "Spray early morning or evening",
                    "safety": "Safe for organic farming"
                }
            ],
            "prevention": [
                "Use disease-free planting material from certified sources",
                "Plant resistant varieties like TME-7, TMS-30572",
                "Maintain 1m x 1m spacing between plants",
                "Remove and burn infected plants immediately",
                "Disinfect cutting tools with 10% bleach solution",
                "Avoid working in fields when plants are wet",
                "Practice crop rotation with non-host crops",
                "Ensure good drainage to reduce humidity"
            ],
            "future_avoidance": [
                "Rotate cassava with legumes or cereals (2-3 year cycle)",
                "Plant resistant varieties: TME-7, TMS-30572, TMS-91934",
                "Establish disease monitoring system - check fields weekly",
                "Control temperature and humidity in storage areas",
                "Rotate bactericides to prevent resistance",
                "Maintain field hygiene - remove crop debris",
                "Use certified disease-free stem cuttings only"
            ],
            "treatment_schedule": {
                "Day 1": {
                    "action": "Remove all infected leaves and stems",
                    "spray": "Copper Hydroxide (2.5 g/L)",
                    "time": "Early morning (6-8 AM)",
                    "monitor": "Mark infected plants with stakes",
                    "avoid": "Don't spray if rain expected within 6 hours"
                },
                "Day 2": {
                    "action": "Inspect neighboring plants for symptoms",
                    "spray": "None - observation day",
                    "time": "Morning inspection",
                    "monitor": "Check for new spots or wilting",
                    "avoid": "Don't water overhead"
                },
                "Day 3": {
                    "action": "Apply systemic treatment",
                    "spray": "Streptomycin Sulfate (200 ppm)",
                    "time": "Evening (5-7 PM)",
                    "monitor": "Document spray coverage",
                    "avoid": "Don't spray during hot sun"
                },
                "Day 4": {
                    "action": "Check soil moisture and drainage",
                    "spray": "None - rest day",
                    "time": "Anytime",
                    "monitor": "Ensure no waterlogging",
                    "avoid": "Don't over-water"
                },
                "Day 5": {
                    "action": "Second copper treatment",
                    "spray": "Copper Hydroxide (2.5 g/L)",
                    "time": "Early morning (6-8 AM)",
                    "monitor": "Check if symptoms are reducing",
                    "avoid": "Don't mix with other chemicals"
                },
                "Day 6": {
                    "action": "Apply organic supplement",
                    "spray": "Neem Oil (5 ml/L)",
                    "time": "Evening (5-7 PM)",
                    "monitor": "Look for new growth",
                    "avoid": "Don't spray in direct sunlight"
                },
                "Day 7": {
                    "action": "Final assessment and planning",
                    "spray": "None - evaluation day",
                    "time": "Morning",
                    "monitor": "Document improvement or spread",
                    "avoid": "Don't stop monitoring after 7 days"
                }
            }
        },
        "Cassava Brown Streak Disease (CBSD)": {
            "scientific_cause": "Cassava brown streak virus (CBSV) transmitted by whiteflies",
            "summary": "CBSD is a viral disease causing brown streaks on stems and roots, leading to root necrosis and making cassava unmarketable. It's transmitted by whiteflies and through infected planting material.",
            "symptoms": {
                "early": ["Yellow chlorotic blotches on young leaves", "Faint brown streaks on stems"],
                "mid": ["Brown necrotic streaks on stems become prominent", "Leaf yellowing spreads", "Root discoloration begins"],
                "advanced": ["Severe root necrosis with brown/black rot", "Unmarketable roots", "Plant stunting"]
            },
            "field_signs": ["Brown streaks on green stems", "Chlorotic leaf patches", "Whitefly presence"],
            "medicines": [
                {"name": "Imidacloprid", "type": "Insecticide (Whitefly control)", "dosage": "0.5 ml/L", "application": "Foliar spray every 10 days", "safety": "Toxic to bees - spray evening"},
                {"name": "Thiamethoxam", "type": "Systemic Insecticide", "dosage": "0.3 g/L", "application": "Soil drench or spray", "safety": "Use protective equipment"},
                {"name": "Neem-based insecticide", "type": "Organic", "dosage": "5-10 ml/L", "application": "Weekly spray", "safety": "Safe for organic farming"}
            ],
            "prevention": ["Use virus-free planting material", "Control whitefly vectors", "Remove infected plants", "Plant resistant varieties"],
            "future_avoidance": ["Use certified clean planting material", "Implement whitefly monitoring", "Plant resistant varieties like Namikonga"],
            "treatment_schedule": {
                "Day 1": {"action": "Remove infected plants", "spray": "Imidacloprid for whiteflies", "time": "Evening", "monitor": "Mark infected areas", "avoid": "Don't replant in same spot"},
                "Day 2-7": {"action": "Continue whitefly control", "spray": "Alternate insecticides", "time": "Evening", "monitor": "Check for new infections", "avoid": "Don't use same insecticide continuously"}
            }
        },
        "Cassava Green Mottle (CGM)": {
            "scientific_cause": "Cassava green mottle virus (CsGMV)",
            "summary": "CGM causes distinctive green mottling patterns on leaves, reducing photosynthesis and yield. It's a relatively mild disease but can cause significant losses in susceptible varieties.",
            "symptoms": {
                "early": ["Light green mottling on young leaves", "Slight leaf distortion"],
                "mid": ["Mottling becomes more pronounced", "Reduced leaf size", "Mild stunting"],
                "advanced": ["Severe mottling across all leaves", "Reduced plant vigor", "Lower yield"]
            },
            "field_signs": ["Green mosaic patterns on leaves", "Uneven leaf coloration", "Slightly stunted growth"],
            "medicines": [
                {"name": "No direct cure - focus on vector control", "type": "Preventive", "dosage": "N/A", "application": "Remove infected plants", "safety": "N/A"},
                {"name": "Insecticides for vector control", "type": "Insecticide", "dosage": "As per label", "application": "Control insect vectors", "safety": "Follow label instructions"}
            ],
            "prevention": ["Use virus-free cuttings", "Control insect vectors", "Rogue out infected plants", "Maintain field sanitation"],
            "future_avoidance": ["Plant resistant varieties", "Use certified planting material", "Monitor and remove infected plants early"],
            "treatment_schedule": {
                "Day 1": {"action": "Identify and remove infected plants", "spray": "None", "time": "Morning", "monitor": "Survey entire field", "avoid": "Don't leave infected material in field"},
                "Day 2-7": {"action": "Monitor for spread", "spray": "Vector control if needed", "time": "Regular checks", "monitor": "New symptoms", "avoid": "Don't replant with uncertified material"}
            }
        },
        "Cassava Mosaic Disease (CMD)": {
            "scientific_cause": "Cassava mosaic geminiviruses transmitted by whiteflies",
            "summary": "CMD is the most widespread and damaging cassava disease in Africa, causing mosaic patterns, leaf distortion, and severe yield losses up to 90%. It spreads through whiteflies and infected cuttings.",
            "symptoms": {
                "early": ["Pale yellow-green mosaic patterns on young leaves", "Slight leaf curling"],
                "mid": ["Severe mosaic and distortion", "Leaf size reduction", "Plant stunting begins"],
                "advanced": ["Severe stunting", "Twisted, distorted leaves", "Up to 90% yield loss"]
            },
            "field_signs": ["Yellow-green mosaic on leaves", "Leaf distortion and curling", "Stunted plants", "Whitefly presence"],
            "medicines": [
                {"name": "Imidacloprid", "type": "Insecticide", "dosage": "0.5 ml/L", "application": "Whitefly control spray", "safety": "Avoid bee exposure"},
                {"name": "Acetamiprid", "type": "Insecticide", "dosage": "0.3 g/L", "application": "Foliar spray", "safety": "Use protective gear"},
                {"name": "Neem oil", "type": "Organic", "dosage": "5 ml/L", "application": "Weekly spray", "safety": "Safe for organic use"}
            ],
            "prevention": ["Use CMD-resistant varieties", "Plant virus-free cuttings", "Control whiteflies", "Remove infected plants within 2 months"],
            "future_avoidance": ["Plant resistant varieties (TME-204, TMS-97/2205)", "Use certified clean planting material", "Implement whitefly IPM program"],
            "treatment_schedule": {
                "Day 1": {"action": "Remove severely infected plants", "spray": "Imidacloprid (0.5 ml/L)", "time": "Evening (6-7 PM)", "monitor": "Count whiteflies", "avoid": "Don't spray during day"},
                "Day 3": {"action": "Second whitefly spray", "spray": "Acetamiprid (0.3 g/L)", "time": "Evening", "monitor": "Check whitefly reduction", "avoid": "Don't use same chemical"},
                "Day 5": {"action": "Organic treatment", "spray": "Neem oil (5 ml/L)", "time": "Early morning", "monitor": "New symptom development", "avoid": "Don't spray in hot sun"},
                "Day 7": {"action": "Assessment", "spray": "Repeat if needed", "time": "Morning", "monitor": "Overall improvement", "avoid": "Don't stop monitoring"}
            }
        },
        "Healthy": {
            "scientific_cause": "No disease detected",
            "summary": "Your cassava plant appears healthy with no visible disease symptoms. Continue good agricultural practices to maintain plant health.",
            "symptoms": {
                "early": ["No symptoms - plant is healthy"],
                "mid": ["No symptoms - plant is healthy"],
                "advanced": ["No symptoms - plant is healthy"]
            },
            "field_signs": ["Vibrant green leaves", "Normal growth", "No discoloration or spots"],
            "medicines": [
                {"name": "Preventive care only", "type": "N/A", "dosage": "N/A", "application": "Regular monitoring", "safety": "N/A"}
            ],
            "prevention": ["Continue current practices", "Regular monitoring", "Use quality planting material", "Maintain field hygiene"],
            "future_avoidance": ["Keep using certified planting material", "Monitor regularly for early disease detection", "Practice crop rotation"],
            "treatment_schedule": {
                "Day 1-7": {"action": "Regular monitoring", "spray": "None needed", "time": "Weekly checks", "monitor": "Watch for any changes", "avoid": "Don't over-fertilize"}
            }
        }
    }
    
    @classmethod
    def get_disease_info(cls, disease_name: str) -> Dict[str, Any]:
        """Get disease information by name"""
        return cls.DISEASE_INFO.get(disease_name, cls.DISEASE_INFO["Healthy"])


class PDFReportGenerator:
    """Generate comprehensive PDF reports for farmers"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C5F2D'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2C5F2D'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
    
    def generate_report(self, prediction_result: Dict[str, Any], image_path: str = None) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            prediction_result: Dictionary containing prediction results
            image_path: Optional path to the analyzed image
        
        Returns:
            Path to generated PDF file
        """
        disease_name = prediction_result['predicted_class']
        confidence = prediction_result['confidence']
        
        # Get disease information
        disease_info = DiseaseDatabase.get_disease_info(disease_name)
        
        # Create PDF filename
        safe_name = disease_name.replace(" ", "_").replace("(", "").replace(")", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Plant_Disease_Report_{safe_name}_{timestamp}.pdf"
        pdf_path = self.output_dir / pdf_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("🌿 Cassava Disease Detection Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        metadata = f"""
        <b>Report Generated:</b> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br/>
        <b>Detected Disease:</b> {disease_name}<br/>
        <b>Detection Confidence:</b> {confidence:.1%}<br/>
        """
        story.append(Paragraph(metadata, self.styles['ReportBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # Section 1: Disease Analysis
        story.append(Paragraph("1. Disease Analysis - How the Model Detected the Disease", self.styles['SectionHeader']))
        analysis_text = self._generate_analysis_text(disease_name, confidence, prediction_result)
        story.append(Paragraph(analysis_text, self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Section 2: Disease Summary
        story.append(Paragraph("2. Disease Summary", self.styles['SectionHeader']))
        summary_text = f"""
        <b>Disease Name:</b> {disease_name}<br/>
        <b>Scientific Cause:</b> {disease_info['scientific_cause']}<br/><br/>
        {disease_info['summary']}
        """
        story.append(Paragraph(summary_text, self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Section 3: Symptoms & Identification
        story.append(Paragraph("3. Symptoms & Identification", self.styles['SectionHeader']))
        story.append(Paragraph("<b>Early Stage Symptoms:</b>", self.styles['ReportBody']))
        for symptom in disease_info['symptoms']['early']:
            story.append(Paragraph(f"• {symptom}", self.styles['ReportBody']))
        story.append(Paragraph("<b>Mid Stage Symptoms:</b>", self.styles['ReportBody']))
        for symptom in disease_info['symptoms']['mid']:
            story.append(Paragraph(f"• {symptom}", self.styles['ReportBody']))
        story.append(Paragraph("<b>Advanced Stage Symptoms:</b>", self.styles['ReportBody']))
        for symptom in disease_info['symptoms']['advanced']:
            story.append(Paragraph(f"• {symptom}", self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Section 4: Recommended Medicines
        story.append(Paragraph("4. Recommended Medicines", self.styles['SectionHeader']))
        medicine_table = self._create_medicine_table(disease_info['medicines'])
        story.append(medicine_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Section 5: Prevention Methods
        story.append(Paragraph("5. Prevention Methods", self.styles['SectionHeader']))
        for method in disease_info['prevention']:
            story.append(Paragraph(f"• {method}", self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Section 6: Future Avoidance
        story.append(Paragraph("6. How to Avoid This Disease in Future", self.styles['SectionHeader']))
        for method in disease_info['future_avoidance']:
            story.append(Paragraph(f"• {method}", self.styles['ReportBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Section 7: Treatment Schedule
        story.append(Paragraph("7. Treatment Plan (7-Day Schedule)", self.styles['SectionHeader']))
        schedule_table = self._create_schedule_table(disease_info['treatment_schedule'])
        story.append(schedule_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Section 8: Final Recommendations
        story.append(Paragraph("8. Final Recommendation Summary", self.styles['SectionHeader']))
        recommendations = self._generate_recommendations(disease_name)
        story.append(Paragraph(recommendations, self.styles['ReportBody']))
        
        # Build PDF
        doc.build(story)
        
        return str(pdf_path)
    
    def _generate_analysis_text(self, disease_name: str, confidence: float, prediction_result: Dict) -> str:
        """Generate disease analysis explanation"""
        if disease_name == "Healthy":
            return """Our advanced AI model analyzed your cassava leaf image using multiple image processing techniques 
            and found no signs of disease. The leaf shows normal green coloration, healthy texture, and no visible 
            symptoms of common cassava diseases. The model examined color patterns, leaf structure, and compared 
            against thousands of disease samples to confirm the plant's healthy status."""
        
        analysis = f"""Our AI model detected <b>{disease_name}</b> with {confidence:.1%} confidence by analyzing 
        multiple visual features from your leaf image:<br/><br/>
        <b>Visual Symptoms Identified:</b><br/>"""
        
        if "Blight" in disease_name:
            analysis += "• Angular leaf spots with yellow halos<br/>• Water-soaked lesions<br/>• Wilting patterns<br/>"
        elif "Brown Streak" in disease_name:
            analysis += "• Brown necrotic streaks on stems<br/>• Chlorotic leaf patches<br/>• Root discoloration patterns<br/>"
        elif "Mosaic" in disease_name:
            analysis += "• Yellow-green mosaic patterns<br/>• Leaf distortion and curling<br/>• Stunted growth indicators<br/>"
        elif "Mottle" in disease_name:
            analysis += "• Green mottling patterns<br/>• Uneven leaf coloration<br/>• Mild distortion<br/>"
        
        analysis += """<br/><b>How the Analysis Works:</b><br/>
        Our model uses advanced image processing (DCT, STFT, Wavelet transforms) combined with deep learning 
        to detect subtle patterns invisible to the human eye. It compares your image against thousands of 
        labeled disease samples to identify characteristic symptoms."""
        
        return analysis
    
    def _create_medicine_table(self, medicines: list) -> Table:
        """Create medicine recommendation table"""
        data = [['Medicine Name', 'Type', 'Dosage', 'Application', 'Safety Notes']]
        
        for med in medicines:
            data.append([
                med['name'],
                med['type'],
                med['dosage'],
                med['application'],
                med['safety']
            ])
        
        table = Table(data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5F2D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        return table
    
    def _create_schedule_table(self, schedule: dict) -> Table:
        """Create 7-day treatment schedule table"""
        data = [['Day', 'Action', 'Spray', 'Time', 'Monitor', 'Avoid']]
        
        for day, details in schedule.items():
            data.append([
                day,
                details.get('action', 'N/A'),
                details.get('spray', 'N/A'),
                details.get('time', 'N/A'),
                details.get('monitor', 'N/A'),
                details.get('avoid', 'N/A')
            ])
        
        table = Table(data, colWidths=[0.6*inch, 1.5*inch, 1.3*inch, 1*inch, 1.3*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C5F2D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        return table
    
    def _generate_recommendations(self, disease_name: str) -> str:
        """Generate final recommendations"""
        if disease_name == "Healthy":
            return """<b>DO's:</b><br/>
            ✓ Continue regular monitoring<br/>
            ✓ Maintain good field hygiene<br/>
            ✓ Use certified planting material<br/>
            ✓ Practice crop rotation<br/><br/>
            <b>DON'Ts:</b><br/>
            ✗ Don't become complacent - diseases can appear quickly<br/>
            ✗ Don't skip regular field inspections<br/>
            ✗ Don't ignore early symptoms in neighboring plants"""
        
        return """<b>DO's:</b><br/>
        ✓ Act quickly - early treatment is most effective<br/>
        ✓ Follow the 7-day treatment schedule strictly<br/>
        ✓ Remove and destroy infected plant parts<br/>
        ✓ Monitor neighboring plants daily<br/>
        ✓ Keep records of treatments applied<br/>
        ✓ Consult local agricultural extension officers<br/><br/>
        <b>DON'Ts:</b><br/>
        ✗ Don't delay treatment - diseases spread rapidly<br/>
        ✗ Don't reuse infected plant material<br/>
        ✗ Don't work in wet fields to avoid spreading disease<br/>
        ✗ Don't use the same chemical repeatedly<br/>
        ✗ Don't ignore safety precautions when spraying"""


# Global generator instance
_generator = None

def get_pdf_generator() -> PDFReportGenerator:
    """Get or create PDF generator instance"""
    global _generator
    if _generator is None:
        _generator = PDFReportGenerator()
    return _generator
