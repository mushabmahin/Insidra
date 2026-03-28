import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_alert_email(emp_id, risk_score, reasons):
    """
    Sends an email alert when a high-risk anomaly is detected.
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        print("⚠️ Email credentials are not fully configured in .env. Skipping email alert.")
        return False

    try:
        msg = EmailMessage()
        msg['Subject'] = f"🚨 INSIDRA ALERT: Critical Threat Detected - Risk Score {risk_score}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        
        # Format reasons properly
        reasons_text = ", ".join(reasons) if isinstance(reasons, list) else reasons

        body = f"""
        🚨 CRITICAL INSIDER THREAT DETECTED 🚨

        A user has triggered a high-risk alert in the Insidra Threat Detection System.

        Details:
        - Employee ID: {emp_id}
        - Risk Score: {risk_score}
        - Identified Reasons: {reasons_text}
        
        Please check the live dashboard for more details.
        
        -- Insidra Monitor
        """
        
        msg.set_content(body)

        # Connect to server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email alert successfully sent for User {emp_id}!")
        return True

    except Exception as e:
        print(f"❌ Failed to send email alert. Error: {e}")
        return False

if __name__ == "__main__":
    # Test execution
    send_alert_email("EMP-TEST", 95, ["Multiple failed logins", "Accessing restricted files"])
