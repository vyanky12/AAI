from textblob import TextBlob
import datetime

class IncidentAnalyzer:
    def __init__(self):
        self.danger_words = {
            'weapon': 5, 'knife': 5, 'gun': 5, 'armed': 5, 'violence': 4,
            'threat': 4, 'force': 3, 'break': 3, 'damage': 2, 'suspicious': 2,
            'steal': 3, 'stolen': 3, 'assault': 5, 'attack': 4, 'robbery': 4,
            'blood': 4, 'injured': 4, 'wound': 4, 'death': 5, 'dead': 5,
            'emergency': 4, 'immediate': 3, 'urgent': 3
        }

    def analyze_threat(self, description):
        """
        Analyze incident description for threat level and severity.
        
        Parameters:
        description (str): The incident description text.
        
        Returns:
        dict: A dictionary containing the threat analysis results.
        """
        blob = TextBlob(description)
        
        # Calculate base severity score from keywords
        severity_score = 0
        found_indicators = []
        words = description.lower().split()
        
        for word in words:
            if word in self.danger_words:
                severity_score += self.danger_words[word]
                found_indicators.append(word)
        
        # Adjust score based on sentiment
        sentiment = blob.sentiment.polarity
        if sentiment < -0.5:
            severity_score += 3
        elif sentiment < -0.3:
            severity_score += 2
        
        # Determine threat level
        if severity_score >= 10:
            threat_level = "HIGH RISK"
            priority = "IMMEDIATE RESPONSE REQUIRED"
        elif severity_score >= 5:
            threat_level = "MEDIUM RISK"
            priority = "URGENT ATTENTION NEEDED"
        else:
            threat_level = "LOW RISK"
            priority = "STANDARD PROTOCOL"
        
        return {
            "threat_level": threat_level,
            "severity_score": severity_score,
            "key_indicators": list(set(found_indicators)),
            "sentiment_score": sentiment,
            "priority": priority,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def generate_report_preview(self, report_data, summary_data, analysis_result):
        """
        Generate a structured preview for officers dashboard.
        
        Parameters:
        report_data (dict): The incident report data.
        summary_data (dict): The text summarization data.
        analysis_result (dict): The threat analysis results.
        
        Returns:
        dict: A dictionary containing the report preview.
        """
        return {
            "report_id": f"INC-{datetime.datetime.now().strftime('%Y%m%d%H%M')}",
            "timestamp": datetime.datetime.now().isoformat(),
            "incident_details": {
                "type": report_data['incidentType'],
                "location": report_data['location'],
                "reporter": {
                    "name": report_data['fullname'],
                    "contact": report_data['phone']
                }
            },
            "risk_assessment": {
                "threat_level": analysis_result['threat_level'],
                "severity_score": analysis_result['severity_score'],
                "key_indicators": analysis_result['key_indicators'],
                "priority": analysis_result['priority']
            },
            "incident_summary": summary_data['summary'],
            "original_description": report_data['description'],
            "response_priority": report_data['urgency'],
            "witnesses_present": report_data.get('witnesses', False)
        }