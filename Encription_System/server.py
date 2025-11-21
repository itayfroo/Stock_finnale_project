import socket
import threading
import struct
import os
from Crypto.PublicKey import RSA
from crypto_utils import (
    aes_decrypt_ecb,
    rsa_decrypt_aes_key,
    load_rsa_private_key
)

HOST = "127.0.0.1"
PORT_DATA = 5000
PORT_KEY  = 5001

PRIVATE_KEY_PATH = "Encription_System/server_private.pem"
PUBLIC_KEY_PATH  = "Encription_System/server_public.pem"


# --------------------------
# GENERATE KEYS IF MISSING
# --------------------------
def generate_keys_if_missing():
    # Create folder if missing
    key_dir = os.path.dirname(PRIVATE_KEY_PATH)
    os.makedirs(key_dir, exist_ok=True)

    # If keys exist → done
    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        print("[KEYS] Existing RSA keys found.")
        return

    print("[KEYS] No RSA keys found. Generating new RSA keypair...")

    key = RSA.generate(2048)

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(key.export_key())

    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(key.publickey().export_key())

    print("[KEYS] RSA keypair generated and saved.")



# --------------------------
# PUBLIC KEY SERVER
# --------------------------
def public_key_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_KEY))
        s.listen()
        print(f"[KEY SERVER] Waiting for key requests on {PORT_KEY}")

        while True:
            conn, addr = s.accept()
            print(f"[KEY SERVER] Client connected for public key: {addr}")

            with conn:
                with open(PUBLIC_KEY_PATH, "rb") as f:
                    pubkey = f.read()
                conn.sendall(pubkey)


# --------------------------
# PACKET PARSING
# --------------------------
def parse_packet(data):
    if data[:4] != b"SSAP":
        print("Invalid packet header")
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

    data_len = struct.unpack("!I", data[offset:offset+4])[0]
    offset += 4
    cipher = data[offset:offset+data_len]

    return ip, port, enc_key, cipher


# --------------------------
# PACKET SERVER
# --------------------------
def packet_server():
    private_key = load_rsa_private_key(PRIVATE_KEY_PATH)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT_DATA))
        server.listen()
        print(f"[PACKET SERVER] Listening on {HOST}:{PORT_DATA}")

        while True:
            conn, addr = server.accept()
            print(f"\n[PACKET SERVER] Client connected: {addr}")

            with conn:
                packet = conn.recv(65535)
                if not packet:
                    print("[WARN] Empty packet ignored")
                    continue

                parsed = parse_packet(packet)
                if parsed is None:
                    continue

                ip, port, enc_key, cipher = parsed

                aes_key = rsa_decrypt_aes_key(enc_key, private_key)
                plaintext = aes_decrypt_ecb(cipher, aes_key)

                print("\n=== PACKET RECEIVED ===")
                print(f"FROM: {ip}:{port}")
                print(f"PLAINTEXT: {plaintext}")
                print("=======================\n")


# --------------------------
# MAIN THREAD STARTER
# --------------------------
if __name__ == "__main__":
    # STEP 1: Create RSA keys if missing
    generate_keys_if_missing()

    # STEP 2: Start public key server
    threading.Thread(target=public_key_server, daemon=True).start()

    # STEP 3: Start packet server
    packet_server()
