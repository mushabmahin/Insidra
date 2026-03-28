import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

# =============================
# CONFIG (CHANGE THESE)
# =============================
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "receiver_email@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

ALERT_LOG_PATH = "data/suspicious_logs.csv"


# =============================
# MAIN ALERT FUNCTION
# =============================
def trigger_alert(event, risk_score, risk_level):
    """
    Generate alert, log it, and send email
    """
    alert_message = (
        f"[ALERT] {datetime.now()}\n"
        f"User: {event.get('user_id')}\n"
        f"Event: {event.get('event_type')}\n"
        f"Risk Score: {risk_score:.2f}\n"
        f"Risk Level: {risk_level}"
    )

    print(alert_message)

    # Save alert locally
    save_alert(event, risk_score, risk_level)

    # Send email alert
    send_email(alert_message)


# =============================
# SAVE ALERT TO CSV
# =============================
def save_alert(event, risk_score, risk_level):
    alert_data = {
        "timestamp": datetime.now(),
        "user_id": event.get("user_id"),
        "event_type": event.get("event_type"),
        "risk_score": risk_score,
        "risk_level": risk_level
    }

    df = pd.DataFrame([alert_data])

    if os.path.exists(ALERT_LOG_PATH):
        df.to_csv(ALERT_LOG_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(ALERT_LOG_PATH, index=False)


# =============================
# EMAIL FUNCTION
# =============================
def send_email(message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "🚨 High Risk Alert Detected"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.send_message(msg)
        server.quit()

        print("📧 Email alert sent successfully!")

    except Exception as e:
        print(f"❌ Email failed: {e}")