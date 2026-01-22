import imaplib
import email
import smtplib
import threading
import time
import os
from email.message import EmailMessage
from email.utils import parseaddr
from dotenv import load_dotenv

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")
COMMAND_SENDER = os.getenv("COMMAND_SENDER")

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"

CHECK_INTERVAL = 20

TRIGGERS = [
    "give me reports",
    "send reports",
    "reports now"
]

REPORT_FILES = [
    "report1.pdf",
    "report2.pdf",
    "report3.pdf"
]

# -------------------------------------------------
# SEND SINGLE REPORT
# -------------------------------------------------
def send_report(file_path):
    try:
        print(f"📤 Sending {file_path}")

        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = TARGET_EMAIL
        msg["Subject"] = "Requested Report"
        msg.set_content("Here is one of your requested reports.")

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(file_path)
            )

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print(f"✅ Sent {file_path}")

    except Exception as e:
        print(f"❌ Failed sending {file_path}: {e}")

# -------------------------------------------------
# MULTI THREAD SEND
# -------------------------------------------------
def send_reports_multithread():
    print("🚀 Starting report threads")

    threads = []

    for file in REPORT_FILES:
        if not os.path.exists(file):
            print(f"❌ Missing file: {file}")
            continue

        t = threading.Thread(target=send_report, args=(file,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("📦 All reports sent")

# -------------------------------------------------
# CHECK MAIL
# -------------------------------------------------
def check_mail():
    print("\n🔍 Checking inbox...")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    if not messages or messages == [b""]:
        mail.logout()
        return

    for msg_id in messages[0].split():
        status, data = mail.fetch(msg_id, "(RFC822)")
        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject = msg.get("Subject", "")
        name, sender_email = parseaddr(msg.get("From", ""))

        sender_email = sender_email.lower()

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        print("\n--- EMAIL FOUND ---")
        print("From:", sender_email)
        print("Subject:", subject)

        # Sender validation (NOW CORRECT)
        allowed = [EMAIL.lower()]
        if COMMAND_SENDER:
            allowed.append(COMMAND_SENDER.lower())

        if sender_email not in allowed:
            print("⛔ Ignored sender")
            continue

        content = (subject + " " + body).lower()

        if any(trigger in content for trigger in TRIGGERS):
            print("🔥 COMMAND TRIGGERED")
            send_reports_multithread()
            mail.store(msg_id, "+FLAGS", "\\Seen")
        else:
            print("❌ Trigger not found")

    mail.logout()

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
def listener_loop():
    print("📡 Mail listener started")
    print("Listening as:", EMAIL)
    print("Accepting commands from:", COMMAND_SENDER)

    while True:
        try:
            check_mail()
        except Exception as e:
            print("💥 MAIL ERROR:", e)

        time.sleep(CHECK_INTERVAL)

# -------------------------------------------------
# START
# -------------------------------------------------
if __name__ == "__main__":
    listener_loop()
