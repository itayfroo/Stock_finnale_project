import socket
import struct
import base64
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


def build_packet(ip, port, enc_key, cipher):
    ip_bytes = ip.encode("ascii")

    packet  = b"SSAP"                                     # magic header
    packet += struct.pack("!I", len(ip_bytes))            # ip length
    packet += ip_bytes                                    # ip bytes
    packet += struct.pack("!I", port)                     # port number
    packet += struct.pack("!I", len(enc_key))             # AES key len
    packet += enc_key                                     # encrypted AES key
    packet += struct.pack("!I", len(cipher))              # data len
    packet += cipher                                      # encrypted data

    return packet


def start_client():
    plaintext = input("Enter message: ")

    public_key = fetch_public_key()

    aes_key = get_random_bytes(32)
    cipher = aes_encrypt_ecb(plaintext, aes_key)
    enc_key = rsa_encrypt_aes_key(aes_key, public_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        local_ip, local_port = s.getsockname()

        packet = build_packet(local_ip, local_port, enc_key, cipher)
        print(packet)
        s.sendall(packet)

    print("Binary packet sent!")


if __name__ == "__main__":
    start_client()
