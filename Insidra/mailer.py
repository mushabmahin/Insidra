import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

def send_soc_email(user_id, risk_score, reasons):
    # Force load environment variables dynamically when the function runs
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path, override=True)

    # Retrieve credentials from environment variables for security
    sender_email = os.environ.get("SMTP_EMAIL", "yoursystem@gmail.com")
    sender_password = os.environ.get("SMTP_PASSWORD", "your_app_password")
    receiver_email = os.environ.get("ADMIN_EMAIL", "admin@company.com")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"🚨 URGENT: High Risk Insider Threat Detected - User {user_id}"

    # Format the reasons neatly
    if isinstance(reasons, list):
        reasons_text = "\n".join([f"- {r}" for r in reasons])
    else:
        reasons_text = f"- {reasons}"

    body = f"""
SECURITY ALERT:

A critical insider threat has been detected by the Insidra System.

Target Subject: {user_id}
Final Risk Score: {risk_score} / 100

Triggered Behavioral Anomalies:
{reasons_text}

Automated Remediation: Manual review recommended immediately. Check the Insidra Dashboard for full forensic details.

- Insidra Autonomous Risk Engine
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Prevent runtime crash if user hasn't setup actual passwords yet
        if sender_password == "your_app_password":
            return True, f"Mock Email generated to {receiver_email}. Setup SMTP_EMAIL and SMTP_PASSWORD environment variables to send real emails."

        # Establish SMTP connection (Configured for Gmail by default)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        server.login(sender_email, sender_password)
        
        # Send
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        
        # Cleanup
        server.quit()
        return True, f"Alert successfully dispatched to {receiver_email}"
        
    except Exception as e:
        return False, f"Mailer Error: {str(e)}"
