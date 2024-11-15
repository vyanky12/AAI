document.addEventListener('DOMContentLoaded', function() {
    let reports = [];
    const reportsContainer = document.getElementById('reports-container');
    const reportTemplate = document.getElementById('report-template');
    const riskFilter = document.getElementById('riskFilter');
    const timeFilter = document.getElementById('timeFilter');

    // Fetch reports from server
    function fetchReports() {
        fetch('/get_reports')
            .then(response => response.json())
            .then(data => {
                reports = data;
                updateDashboard();
            })
            .catch(error => console.error('Error fetching reports:', error));
    }

    // Update dashboard with filtered reports
    function updateDashboard() {
        const filteredReports = filterReports();
        reportsContainer.innerHTML = '';
        
        updateStats(reports);
        
        filteredReports.forEach(report => {
            const reportCard = createReportCard(report);
            reportsContainer.appendChild(reportCard);
        });
    }

    // Create a report card from template
    function createReportCard(report) {
        const template = reportTemplate.content.cloneNode(true);
        
        template.querySelector('.report-id').textContent = report.report_id;
        template.querySelector('.timestamp').textContent = new Date(report.timestamp).toLocaleString();
        
        const riskLevel = template.querySelector('.risk-level');
        riskLevel.textContent = report.risk_assessment.threat_level;
        riskLevel.classList.add(getRiskClass(report.risk_assessment.threat_level));
        
        template.querySelector('.incident-type').textContent = report.incident_details.type;
        template.querySelector('.location').textContent = report.incident_details.location;
        template.querySelector('.summary').textContent = report.incident_summary;
        
        const indicators = template.querySelector('.key-indicators');
        report.risk_assessment.key_indicators.forEach(indicator => {
            const span = document.createElement('span');
            span.textContent = indicator;
            indicators.appendChild(span);
        });
        
        return template;
    }

    // Update statistics
    function updateStats(reports) {
        const stats = {
            'HIGH RISK': 0,
            'MEDIUM RISK': 0,
            'LOW RISK': 0
        };
        
        reports.forEach(report => {
            stats[report.risk_assessment.threat_level]++;
        });
        
        document.getElementById('highRiskCount').textContent = stats['HIGH RISK'];
        document.getElementById('mediumRiskCount').textContent = stats['MEDIUM RISK'];
        document.getElementById('lowRiskCount').textContent = stats['LOW RISK'];
    }

    // Filter reports based on selected filters
    function filterReports() {
        return reports.filter(report => {
            const riskMatch = riskFilter.value === 'all' || report.risk_assessment.threat_level === riskFilter.value;
            const timeMatch = checkTimeFilter(report.timestamp);
            return riskMatch && timeMatch;
        });
    }

    // Check if report matches time filter
    function checkTimeFilter(timestamp) {
        const reportDate = new Date(timestamp);
        const now = new Date();
        
        switch(timeFilter.value) {
            case 'today':
                return reportDate.toDateString() === now.toDateString();
            case 'week':
                const weekAgo = new Date(now.setDate(now.getDate() - 7));
                return reportDate >= weekAgo;
            case 'month':
                const monthAgo = new Date(now.setMonth(now.getMonth() - 1));
                return reportDate >= monthAgo;
            default:
                return true;
        }
    }

    fetchReports();
});