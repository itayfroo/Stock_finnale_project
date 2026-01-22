from Crypto.Random import get_random_bytes
from Encription_System.crypto_utils import aes_encrypt_ecb, rsa_encrypt_aes_key
from Crypto.PublicKey import RSA
import socket
import struct
import json


class EncriptRecoms:


    def __init__(self):
        self.SERVER_HOST = "127.0.0.1"
        self.SERVER_PORT = 5000
        self.KEY_PORT = 5001
        self._aesKey = get_random_bytes(32)

    def fetch_public_key(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.SERVER_HOST, self.KEY_PORT))
            pub = s.recv(4096)
        return RSA.import_key(pub)


    def build_packet(self, ip, port, enc_key, cipher_header, cipher_body):
        ip_bytes = ip.encode("ascii")
        packet = b"SSAP"
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


    def start_client(self, data: dict):
        # dict format example:
        # {"Agam_NVDA": ["NVDA", "text", "⭐⭐⭐⭐⭐", "timestamp"]}

        header = list(data.keys())[0]
        body_json = json.dumps(data[header], ensure_ascii=False)

        public_key = self.fetch_public_key()
        aes_key = self._aesKey

        cipher_header = aes_encrypt_ecb(header, aes_key)
        cipher_body = aes_encrypt_ecb(body_json, aes_key)
        enc_key = rsa_encrypt_aes_key(aes_key, public_key)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.SERVER_HOST, self.SERVER_PORT))
            local_ip, local_port = s.getsockname()

            packet = self.build_packet(local_ip, local_port, enc_key, cipher_header, cipher_body)
            s.sendall(packet)