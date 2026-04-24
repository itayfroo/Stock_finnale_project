import imaplib
import email
import smtplib
import threading
import time
import os
import subprocess
import sys
import json
import random
import requests
import yfinance as yf
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

            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()


BASE_DIR = os.path.dirname(__file__)
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_env_manual(ENV_PATH)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")
COMMAND_SENDER = os.getenv("COMMAND_SENDER")

if not EMAIL or not PASSWORD:
    raise RuntimeError("EMAIL or PASSWORD missing")

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
os.chdir(PROJECT_ROOT)

USERS_JSON_PATH = os.path.join(PROJECT_ROOT, "texts", "users.json")
STOCKS_JSON_PATH = os.path.join(PROJECT_ROOT, "texts", "stocks.json")

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
CHECK_INTERVAL = 5

TRIGGERS = [
    "give me reports",
    "send reports",
    "reports now",
    "reports",
]

ADD_STOCK_SUBJECTS = [
    "add stock",
    "add stocks",
    "new stock",
    "new stocks",
]

API_KEYS = [
    "MNI5T6CU7KLSFJA8",
    "QJFF49AEUN6NX884",
    "9ZZWS60Q2CZ6JYUK",
    "ZX5XTAKCAXGAYNBG",
    "XUKT2LY2NIC35B83",
    "9XZBYP0RSJFMOT4L",
    "L485NGI7NK2M6VFT",
    "PS74H4D0OXVW2M22",
    "X7RFFB0EHKNTH25O",
    "EEINBBF6PX2GAO02",
    "FLTAY1Z6W73ZVRQB",
    "JDZLDTK95XWAYVEP",
    "QOHMIEDH92482YHC",
    "ZL7O0XZCYX1QQAIB",
]

REPORT_DIR = os.path.join(PROJECT_ROOT, "codes", "eMail_System", "reports")

REPORT_FILES = [
    os.path.join(REPORT_DIR, "new_users_weekly.csv"),
    os.path.join(REPORT_DIR, "stock_recommendation_stats.csv"),
    os.path.join(REPORT_DIR, "weekly_recommendations.csv"),
]


# GENERATE REPORTS
def generate_reports_on_start() -> None:
    print("Generating reports...")

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
            print("Generated:", script)

        except Exception as e:
            print("Failed generating:", script, "Error:", e)


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

        print("Sent:", file_path)

    except Exception as e:
        print("Send failed:", e)


# MULTI THREAD SEND
def send_reports_multithread() -> None:
    threads = []

    for file_path in REPORT_FILES:
        if os.path.exists(file_path):
            thread = threading.Thread(target=send_report, args=(file_path,))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()


# REMOVE USERS PROTOCOL
def parse_usernames(body: str) -> list[str]:
    if not body:
        return []

    body = body.replace(",", "\n")
    names = []

    for line in body.splitlines():
        username = line.strip()

        if not username:
            continue

        username = username.strip('"').strip("'")

        if username:
            names.append(username)

    seen = set()
    output = []

    for username in names:
        if username not in seen:
            seen.add(username)
            output.append(username)

    return output


def load_users_db() -> dict:
    if not os.path.exists(USERS_JSON_PATH):
        return {}

    with open(USERS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def user_exists_in_db(data: dict, username: str) -> bool:
    return username in data or f"{username}_info" in data


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
                print("Removed:", username)

            except Exception as e:
                print("Failed removing:", username, "Error:", e)

        else:
            print("User not found:", username)

    return removed


def send_admin_remove_response(admin_email: str, removed: list[str]) -> None:
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = admin_email

    if removed:
        msg["Subject"] = "users removed"
        msg.set_content("Removed users:\n" + "\n".join(removed))
    else:
        msg["Subject"] = "Users not found"
        msg.set_content("No users were removed.")

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


# ADD STOCKS PROTOCOL
def parse_company_names(body: str) -> list[str]:
    if not body:
        return []

    body = body.replace(",", "\n")
    companies = []

    for line in body.splitlines():
        company_name = line.strip().strip('"').strip("'")

        if company_name:
            companies.append(company_name)

    seen = set()
    output = []

    for company_name in companies:
        normalized = company_name.upper()

        if normalized not in seen:
            seen.add(normalized)
            output.append(company_name)

    return output


def load_stocks_db() -> dict:
    if not os.path.exists(STOCKS_JSON_PATH):
        return {}

    with open(STOCKS_JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_stocks_db(data: dict) -> None:
    with open(STOCKS_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def stock_already_exists(data: dict, company_name: str, symbol: str | None = None) -> bool:
    company_key = company_name.upper()

    if company_key in data:
        return True

    if symbol:
        symbol = symbol.upper()

        for existing_symbol in data.values():
            if str(existing_symbol).upper() == symbol:
                return True

    return False


def get_stock_symbol(company_name: str) -> tuple[str | None, bool]:
    all_api_keys_failed = True

    for api_key in API_KEYS:
        try:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "SYMBOL_SEARCH",
                    "keywords": company_name,
                    "apikey": api_key,
                },
                timeout=10,
            )

            data = response.json()

            if "bestMatches" in data and data["bestMatches"]:
                symbol = data["bestMatches"][0]["1. symbol"].upper()
                return symbol, False

            if "Note" in data or "Information" in data:
                print("API key limit/problem:", api_key)
                continue

            all_api_keys_failed = False

        except Exception as e:
            print("API key failed:", api_key, "Error:", e)
            continue

    return None, all_api_keys_failed


def symbol_has_yfinance_data(symbol: str) -> bool:
    try:
        data = yf.download(
            symbol,
            period="5d",
            interval="1d",
            progress=False,
            auto_adjust=True,
        )

        return data is not None and not data.empty

    except Exception as e:
        print("YFinance validation failed for:", symbol, "Error:", e)
        return False


def add_stocks_from_body(body: str) -> dict:
    company_names = parse_company_names(body)

    results = {
        "added": [],
        "already_exists": [],
        "not_found": [],
        "api_failed": [],
        "invalid_symbol": [],
    }

    if not company_names:
        return results

    stocks_data = load_stocks_db()

    for company_name in company_names:
        if stock_already_exists(stocks_data, company_name):
            results["already_exists"].append(company_name.upper())
            continue

        symbol, api_failed = get_stock_symbol(company_name)

        if api_failed:
            results["api_failed"].append(company_name)
            continue

        if not symbol:
            results["not_found"].append(company_name)
            continue

        if not symbol_has_yfinance_data(symbol):
            results["invalid_symbol"].append(f"{company_name} ({symbol})")
            continue

        stocks_data = load_stocks_db()

        if stock_already_exists(stocks_data, company_name, symbol):
            results["already_exists"].append(f"{company_name.upper()}: {symbol}")
            continue

        stocks_data[company_name.upper()] = symbol
        save_stocks_db(stocks_data)

        results["added"].append((company_name.upper(), symbol))
        print("Added stock:", company_name.upper(), symbol)

    return results


def build_add_stocks_response_body(results: dict) -> str:
    lines = []

    if results["added"]:
        lines.append("Stocks added successfully:")
        for company_name, symbol in results["added"]:
            lines.append(f"{company_name}: {symbol}")
        lines.append("")

    if results["already_exists"]:
        lines.append("Stocks already inside the system:")
        for item in results["already_exists"]:
            lines.append(str(item))
        lines.append("")

    if results["not_found"]:
        lines.append("No stock symbol was found for:")
        for company_name in results["not_found"]:
            lines.append(company_name)
        lines.append("")

    if results["invalid_symbol"]:
        lines.append("Invalid symbol, no yfinance data was found:")
        for item in results["invalid_symbol"]:
            lines.append(str(item))
        lines.append("")

    if results["api_failed"]:
        lines.append("Could not check these stocks because all API keys failed or reached their limit:")
        for company_name in results["api_failed"]:
            lines.append(company_name)
        lines.append("")

    if not lines:
        lines.append("No company names were found in the email body.")

    return "\n".join(lines).strip()


def send_add_stocks_response(admin_email: str, results: dict) -> None:
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = admin_email
    msg["Subject"] = "stocks update result"
    msg.set_content(build_add_stocks_response_body(results))

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


# READ EMAIL BODY
def get_email_body(msg) -> str:
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True) or b""
                body += payload.decode(errors="ignore")

    else:
        payload = msg.get_payload(decode=True) or b""
        body = payload.decode(errors="ignore")

    return body


# CHECK MAIL
def check_mail() -> None:
    mail = None

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            return

        allowed = [EMAIL.lower()]

        if COMMAND_SENDER:
            allowed.append(COMMAND_SENDER.lower())

        for msg_id in messages[0].split():
            try:
                status, data = mail.fetch(msg_id, "(RFC822)")

                if status != "OK" or not data or not data[0]:
                    continue

                msg = email.message_from_bytes(data[0][1])

                subject = msg.get("Subject", "")
                normalized_subject = subject.strip().lower()

                _, sender = parseaddr(msg.get("From", ""))
                sender = sender.lower().strip()

                body = get_email_body(msg)

                if sender in allowed:
                    if normalized_subject in ("remove users", "remove user"):
                        removed_users = handle_remove_users(body)
                        send_admin_remove_response(sender, removed_users)

                    elif normalized_subject in ADD_STOCK_SUBJECTS:
                        results = add_stocks_from_body(body)
                        send_add_stocks_response(sender, results)

                    else:
                        content = (subject + body).lower()

                        if any(trigger in content for trigger in TRIGGERS):
                            generate_reports_on_start()
                            time.sleep(1.5)
                            send_reports_multithread()

                mail.store(msg_id, "+FLAGS", "\\Seen")

            except imaplib.IMAP4.abort:
                raise

            except Exception as e:
                print("Failed processing email:", e)

    finally:
        if mail:
            try:
                mail.logout()
            except Exception:
                pass


# MAIN LOOP
def listener_loop() -> None:
    print("Mail listener started as", EMAIL)

    while True:
        try:
            check_mail()

        except imaplib.IMAP4.abort as e:
            print("IMAP connection aborted:", e)
            print("Reconnecting on next cycle...")

        except imaplib.IMAP4.error as e:
            print("IMAP error:", e)

        except Exception as e:
            print("Listener error:", e)

        time.sleep(CHECK_INTERVAL)


# START
if __name__ == "__main__":
    listener_loop()