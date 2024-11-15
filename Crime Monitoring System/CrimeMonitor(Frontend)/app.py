from flask import Flask, render_template, request, jsonify
from text_summary import summarizer
from sentiment_analysis import IncidentAnalyzer
import json
from datetime import datetime

app = Flask(__name__)
incident_analyzer = IncidentAnalyzer()

# Store reports in memory (replace with database in production)
officer_reports = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/officer-dashboard')
def officer_dashboard():
    return render_template('officer_dashboard.html')

@app.route('/submit_incident', methods=['POST'])
def submit_incident():
    if request.method == 'POST':
        report_data = request.get_json()
        
        # Generate summary
        summary, doc, original_length, summary_length = summarizer(report_data['description'])
        summary_data = {
            'summary': summary,
            'original_length': original_length,
            'summary_length': summary_length
        }
        
        # Analyze incident
        analysis_result = incident_analyzer.analyze_threat(report_data['description'])
        
        # Generate officer preview
        preview = incident_analyzer.generate_report_preview(
            report_data, summary_data, analysis_result
        )
        
        # Store report (replace with database in production)
        officer_reports.append(preview)
        
        return jsonify({
            "status": "success",
            "message": "Incident report processed",
            "report_id": preview["report_id"]
        })

@app.route('/get_reports', methods=['GET'])
def get_reports():
    return jsonify(officer_reports)

if __name__ == "__main__":
    app.run(debug=True)