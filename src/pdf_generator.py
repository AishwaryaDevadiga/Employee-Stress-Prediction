"""
PDF Report Generator Module
Creates professional PDF reports for employee stress predictions
"""

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from datetime import datetime
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

import pandas as pd
from io import BytesIO


class PDFReportGenerator:
    """Generate professional PDF reports for employee stress analysis."""
    
    def __init__(self):
        """Initialize PDF report generator."""
        self.available = REPORTLAB_AVAILABLE
    
    def generate_prediction_report(self, employee_data, prediction, probabilities, stress_score):
        """
        Generate a PDF report for a single employee prediction.
        
        Parameters:
        -----------
        employee_data : dict
            Employee information
        prediction : int
            Predicted stress level (0, 1, or 2)
        probabilities : array
            Probability distribution
        stress_score : float
            Calculated stress score
        
        Returns:
        --------
        BytesIO or None
            PDF document as bytes, or None if reportlab not available
        """
        if not REPORTLAB_AVAILABLE:
            return None
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Define custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("🏢 HR Analytics Platform", title_style))
        story.append(Paragraph("Employee Stress Prediction Report", styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Report Date
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Employee Information
        story.append(Paragraph("Employee Information", header_style))
        emp_data = [
            ["Field", "Value"],
            ["Employee ID", str(employee_data.get('id', 'N/A'))],
            ["Age", str(employee_data.get('age', 'N/A'))],
            ["Gender", str(employee_data.get('gender', 'N/A'))],
            ["Department", str(employee_data.get('department', 'N/A'))],
            ["Salary", f"${employee_data.get('salary', 0):,.2f}"],
            ["Heart Rate (BPM)", str(employee_data.get('heart_rate', 'N/A'))]
        ]
        
        emp_table = Table(emp_data, colWidths=[2*inch, 2*inch])
        emp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(emp_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Prediction Results
        story.append(Paragraph("Prediction Results", header_style))
        
        stress_levels = ['Low Stress', 'Medium Stress', 'High Stress']
        predicted_level = stress_levels[int(prediction)]
        
        results_data = [
            ["Metric", "Value"],
            ["Predicted Stress Level", f"🔴 {predicted_level}" if prediction == 2 else f"🟡 {predicted_level}" if prediction == 1 else f"🟢 {predicted_level}"],
            ["Stress Score", f"{stress_score:.2f}/10"],
            ["Confidence", f"{max(probabilities)*100:.1f}%"],
            ["Low Stress Probability", f"{probabilities[0]*100:.2f}%"],
            ["Medium Stress Probability", f"{probabilities[1]*100:.2f}%"],
            ["High Stress Probability", f"{probabilities[2]*100:.2f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 1.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(results_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("HR Recommendations", header_style))
        
        if predicted_level == 'Low Stress':
            recommendation = """
            <b>✅ Employee is performing well</b><br/>
            - Continue current work arrangement<br/>
            - Recognize and reward good performance<br/>
            - Maintain regular check-ins<br/>
            - Support career development opportunities
            """
        elif predicted_level == 'Medium Stress':
            recommendation = """
            <b>⚠️ Monitor employee workload</b><br/>
            - Reduce workload where possible<br/>
            - Recommend wellness activities and programs<br/>
            - Schedule one-on-one meetings with manager<br/>
            - Consider flexible work arrangements<br/>
            - Check for work-life balance issues
            """
        else:
            recommendation = """
            <b>🚨 Immediate intervention required</b><br/>
            - Schedule urgent meeting with HR<br/>
            - Offer mental health counseling services<br/>
            - Consider temporary workload reduction<br/>
            - Explore mentoring opportunities<br/>
            - Review role and responsibilities<br/>
            - Consider transfer or role change
            """
        
        story.append(Paragraph(recommendation, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(Paragraph("---", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("<i>This report is generated by the HR Analytics Platform. "
                              "For confidentiality, please handle with care.</i>", 
                              styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
    
    def generate_summary_report(self, df):
        """
        Generate a PDF summary report for the entire organization.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Employee dataset with predictions
        
        Returns:
        --------
        BytesIO or None
            PDF document as bytes
        """
        if not REPORTLAB_AVAILABLE:
            return None
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph("Employee Stress Analysis Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary Statistics
        total_emp = len(df)
        low_stress = len(df[df['Stress_Level'] == 0])
        med_stress = len(df[df['Stress_Level'] == 1])
        high_stress = len(df[df['Stress_Level'] == 2])
        
        summary_data = [
            ["Metric", "Count", "Percentage"],
            ["Total Employees", str(total_emp), "100%"],
            ["Low Stress", str(low_stress), f"{low_stress/total_emp*100:.1f}%"],
            ["Medium Stress", str(med_stress), f"{med_stress/total_emp*100:.1f}%"],
            ["High Stress", str(high_stress), f"{high_stress/total_emp*100:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer


# Initialize generator
pdf_generator = PDFReportGenerator()
