from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import json
import logging

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration (use environment variables in production)
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'email': os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com'),
    'password': os.getenv('EMAIL_PASSWORD', 'your-app-password'),
    'recipient': os.getenv('RECIPIENT_EMAIL', 'hello@zolabecker.com')
}

# Route to serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# API route to handle form submissions
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email format
        import re
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Log the form submission
        logger.info(f"Form submission from {data['name']} ({data['email']})")
        
        # Save to file (backup)
        save_form_data(data)
        
        # Send email notification
        send_email_notification(data)
        
        return jsonify({'message': 'Form submitted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error processing form submission: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def save_form_data(data):
    """Save form data to a JSON file for backup"""
    try:
        # Create submissions directory if it doesn't exist
        if not os.path.exists('submissions'):
            os.makedirs('submissions')
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        # Save to file
        filename = f"submissions/submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Form data saved to {filename}")
        
    except Exception as e:
        logger.error(f"Error saving form data: {str(e)}")

def send_email_notification(data):
    """Send email notification about new form submission"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = EMAIL_CONFIG['recipient']
        msg['Subject'] = f"New Portfolio Contact: {data['subject']}"
        
        # Email body
        body = f"""
        New contact form submission from your portfolio website:
        
        Name: {data['name']}
        Email: {data['email']}
        Subject: {data['subject']}
        
        Message:
        {data['message']}
        
        Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to server and send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], EMAIL_CONFIG['recipient'], text)
        server.quit()
        
        logger.info(f"Email notification sent for submission from {data['name']}")
        
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
        # Don't raise the error - we don't want form submission to fail if email fails

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

# API endpoint to get form submissions (for admin use)
@app.route('/admin/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = []
        submissions_dir = 'submissions'
        
        if os.path.exists(submissions_dir):
            for filename in sorted(os.listdir(submissions_dir)):
                if filename.endswith('.json'):
                    with open(os.path.join(submissions_dir, filename), 'r') as f:
                        submission = json.load(f)
                        submissions.append(submission)
        
        return jsonify(submissions), 200
        
    except Exception as e:
        logger.error(f"Error retrieving submissions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create submissions directory
    if not os.path.exists('submissions'):
        os.makedirs('submissions')
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)