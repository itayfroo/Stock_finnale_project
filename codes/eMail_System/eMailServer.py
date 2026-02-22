import imaplib
import email
import smtplib
import threading
import time
import os
import subprocess
import sys
import json
from email.message import EmailMessage
from email.utils import parseaddr

from codes.removeUser import RemoveUser

# MANUAL ENV LOADER
def load_env_manual(path: str) -> None:
    if not os.path.exists(path):
        raise RuntimeError(".env file not found")

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if (not line) or line.startswith("#") or ("=" not in line):
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

# Make relative paths (like texts/users.json) work from anywhere
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
os.chdir(PROJECT_ROOT)

USERS_JSON_PATH = os.path.join(PROJECT_ROOT, "texts", "users.json")

# CONSTANTS
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
CHECK_INTERVAL = 5

TRIGGERS = ["give me reports", "send reports", "reports now","reports"]

REPORT_DIR = os.path.join(PROJECT_ROOT, "codes", "eMail_System", "reports")

REPORT_FILES = [
    os.path.join(REPORT_DIR, "new_users_weekly.csv"),
    os.path.join(REPORT_DIR, "stock_recommendation_stats.csv"),
    os.path.join(REPORT_DIR, "weekly_recommendations.csv"),
]

# GENERATE REPORTS
def generate_reports_on_start() -> None:
    print("🛠 Generating reports at startup")

    scripts = [
        "generate_new_users_report.py",
        "generate_stock_stats_report.py",
        "generate_weekly_recommendations.py",
    ]

    scripts_dir = os.path.join(PROJECT_ROOT, "codes", "eMail_System")

    for script in scripts:
        path = os.path.join(scripts_dir, script)
        try:
            subprocess.run([sys.executable, path], check=True)
            print("✅ Generated:", script)
        except Exception as e:
            print("❌ Failed:", script, e)

# SEND SINGLE REPORT
def send_report(file_path: str) -> None:
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = TARGET_EMAIL
        report_name = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ")
        msg["Subject"] = report_name
        msg.set_content("Here is one of your requested reports.")

        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="csv",
                filename=os.path.basename(file_path),
            )

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("✅ Sent:", file_path)
    except Exception as e:
        print("❌ Send failed:", e)

# MULTI THREAD SEND
def send_reports_multithread() -> None:
    threads = []
    for file_path in REPORT_FILES:
        if os.path.exists(file_path):
            t = threading.Thread(target=send_report, args=(file_path,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

# REMOVE USERS PROTOCOL
def parse_usernames(body: str) -> list[str]:

    if not body:
        return []

    body = body.replace(",", "\n")
    names = []
    for line in body.splitlines():
        u = line.strip()
        if not u:
            continue
        u = u.strip('"').strip("'")
        if u:
            names.append(u)

    seen = set()
    out = []
    for u in names:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def load_users_db() -> dict:
    if not os.path.exists(USERS_JSON_PATH):
        return {}
    with open(USERS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def user_exists_in_db(data: dict, username: str) -> bool:
    return (username in data) or (f"{username}_info" in data)

def handle_remove_users(body: str) -> list[str]:
    usernames = parse_usernames(body)
    if not usernames:
        return []

    data = load_users_db()
    removed = []

    for username in usernames:
        if user_exists_in_db(data, username):
            try:
                RemoveUser(username)
                removed.append(username)
                print("✅ Removed:", username)
            except Exception as e:
                print("❌ Failed removing", username, "error:", e)
        else:
            print("⚠ Not found (no removal):", username)

    return removed

def send_admin_remove_response(admin_email: str, removed: list[str]) -> None:
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = admin_email

    if removed:
        msg["Subject"] = "users removed"
        msg.set_content("Removed users:\n" + "\n".join(removed))
    else:
        msg["Subject"] = "Users not found."
        msg.set_content("No users were removed!")

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

# CHECK MAIL
def check_mail() -> None:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        mail.logout()
        return

    allowed = [EMAIL.lower()]
    if COMMAND_SENDER:
        allowed.append(COMMAND_SENDER.lower())

    for msg_id in messages[0].split():
        status, data = mail.fetch(msg_id, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(data[0][1])

        subject = msg.get("Subject", "")
        _, sender = parseaddr(msg.get("From", ""))
        sender = sender.lower().strip()

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True) or b""
                    body += payload.decode(errors="ignore")
        else:
            payload = msg.get_payload(decode=True) or b""
            body = payload.decode(errors="ignore")

        if sender in allowed:
            normalized_subject = subject.strip().lower()

            if normalized_subject in ("remove users", "remove user"):
                removed_users = handle_remove_users(body)
                send_admin_remove_response(sender, removed_users)
            else:
                content = (subject + body).lower()
                if any(t in content for t in TRIGGERS):
                    generate_reports_on_start()
                    time.sleep(1.5)
                    send_reports_multithread()

        mail.store(msg_id, "+FLAGS", "\\Seen")

    mail.logout()

# MAIN LOOP
def listener_loop() -> None:
    print("📡 Mail listener started as", EMAIL)
    while True:
        check_mail()
        time.sleep(CHECK_INTERVAL)

# START
if __name__ == "__main__":
    listener_loop()