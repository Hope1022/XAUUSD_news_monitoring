import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from scraper import get_current_gold_price
import os
from dotenv import load_dotenv

load_dotenv()

def send_alert(article, analysis):
    sender    = os.getenv("EMAIL_ADDRESS")
    password  = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL")
    #.get() is like get the urgency value from a dictionary ("urgency":"high")
    #which is high, but if some how failed use medium rather than empty
    urgency   = analysis.get("urgency", "medium").upper()
    #same for reason get "reason" value if not just return an empty for the reason value makes sense
    reason    = analysis.get("reason", "")
    gold_price = get_current_gold_price()   # ← live price in every alert

    message = MIMEMultipart()
    message["Subject"] = f"🟡 GOLD [{urgency}] — {article['title'][:60]}"
    message["From"]    = sender
    message["To"]      = recipient

    body = f"""
GOLD MARKET ALERT
─────────────────────────────────
Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Gold Price:  {gold_price}
Urgency:     {urgency}
Source:      {article['source']}
─────────────────────────────────

HEADLINE:
{article['title']}

WHY THIS MATTERS:
{reason}

CONTENT:
{article['content'][:500]}

READ MORE:
{article['url']}
─────────────────────────────────
    """

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message.as_string())
        print(f"Alert sent ✅ Gold at {gold_price}")
    except Exception as e:
        print(f"Email failed: {e}")