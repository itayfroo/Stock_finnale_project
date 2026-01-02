import socket
import struct
import json
from Crypto.Random import get_random_bytes
from crypto_utils import aes_encrypt_ecb, rsa_encrypt_aes_key
from Crypto.PublicKey import RSA

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
KEY_PORT    = 5001


def fetch_public_key():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, KEY_PORT))
        pub = s.recv(4096)
    return RSA.import_key(pub)


def build_packet(ip, port, enc_key, cipher_header, cipher_body):
    ip_bytes = ip.encode("ascii")

    packet  = b"SSAP"
    packet += struct.pack("!I", len(ip_bytes))
    packet += ip_bytes
    packet += struct.pack("!I", port)

    packet += struct.pack("!I", len(enc_key))
    packet += enc_key

    packet += struct.pack("!I", len(cipher_header))
    packet += cipher_header

    packet += struct.pack("!I", len(cipher_body))
    packet += cipher_body

    return packet


def start_client(data: dict):
    # dict format example:
    # {"Agam_NVDA": ["NVDA", "text", "⭐⭐⭐⭐⭐", "timestamp"]}

    header = list(data.keys())[0]
    body_json = json.dumps(data[header], ensure_ascii=False)

    public_key = fetch_public_key()
    aes_key = get_random_bytes(32)

    cipher_header = aes_encrypt_ecb(header, aes_key)
    cipher_body = aes_encrypt_ecb(body_json, aes_key)
    enc_key = rsa_encrypt_aes_key(aes_key, public_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        local_ip, local_port = s.getsockname()

        packet = build_packet(local_ip, local_port, enc_key, cipher_header, cipher_body)
        s.sendall(packet)

    print("Packet sent!")


if __name__ == "__main__":
    start_client({"Agam_NVDA": ["NVDA", "this stock os goated!", "\u2b50\u2b50\u2b50\u2b50\u2b50", "2025-11-21 17:37:08.706831"]})

