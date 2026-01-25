import imaplib
import email
import smtplib
import threading
import time
import os
import subprocess
import sys
from email.message import EmailMessage
from email.utils import parseaddr

# -------------------------------------------------
# MANUAL ENV LOADER
# -------------------------------------------------
def load_env_manual(path):
    if not os.path.exists(path):
        raise RuntimeError(".env file not found")

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

BASE_DIR = os.path.dirname(__file__)
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_env_manual(ENV_PATH)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")
COMMAND_SENDER = os.getenv("COMMAND_SENDER")

if not EMAIL or not PASSWORD:
    raise RuntimeError("EMAIL or PASSWORD missing")

# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
CHECK_INTERVAL = 20

TRIGGERS = ["give me reports", "send reports", "reports now"]

REPORT_DIR = os.path.join(BASE_DIR, "reports")

REPORT_FILES = [
    os.path.join(REPORT_DIR, "new_users_weekly.csv"),
    os.path.join(REPORT_DIR, "stock_recommendation_stats.csv"),
    os.path.join(REPORT_DIR, "weekly_recommendations.csv")
]

# -------------------------------------------------
# GENERATE REPORTS
# -------------------------------------------------
def generate_reports_on_start():
    print("🛠 Generating reports at startup")

    scripts = [
        "generate_new_users_report.py",
        "generate_stock_stats_report.py",
        "generate_weekly_recommendations.py"
    ]

    for script in scripts:
        path = os.path.join(BASE_DIR, script)
        try:
            subprocess.run([sys.executable, path], check=True)
            print("✅ Generated:", script)
        except Exception as e:
            print("❌ Failed:", script, e)

# -------------------------------------------------
# SEND SINGLE REPORT
# -------------------------------------------------
def send_report(file_path):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = TARGET_EMAIL
        msg["Subject"] = "Requested Report"
        msg.set_content("Here is one of your requested reports.")

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="csv",
                filename=os.path.basename(file_path)
            )

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("✅ Sent:", file_path)
    except Exception as e:
        print("❌ Send failed:", e)

# -------------------------------------------------
# MULTI THREAD SEND
# -------------------------------------------------
def send_reports_multithread():
    threads = []
    for file in REPORT_FILES:
        if os.path.exists(file):
            t = threading.Thread(target=send_report, args=(file,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

# -------------------------------------------------
# CHECK MAIL
# -------------------------------------------------
def check_mail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        return

    for msg_id in messages[0].split():
        _, data = mail.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        subject = msg.get("Subject", "")
        _, sender = parseaddr(msg.get("From", ""))
        sender = sender.lower()

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        allowed = [EMAIL.lower()]
        if COMMAND_SENDER:
            allowed.append(COMMAND_SENDER.lower())

        if sender in allowed:
            content = (subject + body).lower()
            if any(t in content for t in TRIGGERS):
                generate_reports_on_start()
                send_reports_multithread()

        mail.store(msg_id, "+FLAGS", "\\Seen")

    mail.logout()

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
def listener_loop():
    print("📡 Mail listener started as", EMAIL)
    while True:
        check_mail()
        time.sleep(CHECK_INTERVAL)

# -------------------------------------------------
# START
# -------------------------------------------------
if __name__ == "__main__":
    generate_reports_on_start()
    listener_loop()
