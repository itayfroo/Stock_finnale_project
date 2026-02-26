import socket
import threading
import struct
import os
import json
from Crypto.PublicKey import RSA

from Encription_System.crypto_utils import (
    aes_decrypt_ecb,
    rsa_decrypt_aes_key,
    load_rsa_private_key
)

HOST = "127.0.0.1"
PORT_DATA = 5000
PORT_KEY  = 5001

PRIVATE_KEY_PATH = "Encription_System/Encription_System/server_private.pem"
PUBLIC_KEY_PATH  = "Encription_System/Encription_System/server_public.pem"
path = r"texts\recommendations.json"


def push_recommendation(key, value_list):
    data = {}

    # load existing dict
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    # add new entry
    data[key] = value_list

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=True,
                separators=(',', ':')
            )
    except:
        print("No such file or directory: 'texts\\recommendations.json'")

def generate_keys_if_missing():
    key_dir = os.path.dirname(PRIVATE_KEY_PATH)
    os.makedirs(key_dir, exist_ok=True)

    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        print("[KEYS] Existing RSA keys found.")
        return

    print("[KEYS] No RSA keys found. Generating...")

    key = RSA.generate(2048)

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(key.export_key())

    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(key.publickey().export_key())

    print("[KEYS] RSA keypair generated.")



def public_key_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_KEY))
        s.listen()
        print(f"[KEY SERVER] Waiting on {PORT_KEY}...")

        while True:
            conn, addr = s.accept()
            print(f"[KEY SERVER] Client connected: {addr}")
            with conn:
                with open(PUBLIC_KEY_PATH, "rb") as f:
                    conn.sendall(f.read())



def parse_packet(data):
    if data[:4] != b"SSAP":
        print("Invalid header")
        return None

    offset = 4

    ip_len = struct.unpack("!I", data[offset:offset+4])[0]
    offset += 4

    ip = data[offset:offset+ip_len].decode("ascii")
    offset += ip_len

    port = struct.unpack("!I", data[offset:offset+4])[0]
    offset += 4

    key_len = struct.unpack("!I", data[offset:offset+4])[0]
    offset += 4

    enc_key = data[offset:offset+key_len]
    offset += key_len

    header_len = struct.unpack("!I", data[offset:offset+4])[0]
    offset += 4

    cipher_header = data[offset:offset+header_len]
    offset += header_len

    body_len = struct.unpack("!I", data[offset:offset+4])[0]
    offset += 4

    cipher_body = data[offset:offset+body_len]

    return ip, port, enc_key, cipher_header, cipher_body



def handle_client(conn, addr, private_key):
    print(f"\n[PACKET] Client: {addr}")

    with conn:
        packet = conn.recv(65535)
        if not packet:
            return

        parsed = parse_packet(packet)
        if not parsed:
            return

        ip, port, enc_key, cipher_header, cipher_body = parsed

        aes_key = rsa_decrypt_aes_key(enc_key, private_key)
        header = aes_decrypt_ecb(cipher_header, aes_key)
        body = aes_decrypt_ecb(cipher_body, aes_key)

        try:
            body = json.loads(body)
        except:
            pass
        recomand = {header: body}
        print("\n=== PACKET RECEIVED ===")
        print(f"FROM: {ip}:{port}")
        print(f"recommendation: {recomand}")
        print("=======================\n")
        push_recommendation(header, body)



def packet_server():
    private_key = load_rsa_private_key(PRIVATE_KEY_PATH)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT_DATA))
        server.listen()
        print(f"[PACKET SERVER] Listening on {HOST}:{PORT_DATA}")

        while True:
            conn, addr = server.accept()

            threading.Thread(
                target=handle_client,
                args=(conn, addr, private_key),
                daemon=True
            ).start()


def main():
    generate_keys_if_missing()
    threading.Thread(target=public_key_server, daemon=True).start()
    packet_server()

if __name__ == "__main__":
    main()