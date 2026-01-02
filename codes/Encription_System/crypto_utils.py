from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# -------------------------
# PKCS7 padding
# -------------------------
def pad(data: bytes) -> bytes:
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len]) * pad_len

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

# -------------------------
# AES ECB
# -------------------------
def aes_encrypt_ecb(plaintext: str, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(plaintext.encode("utf-8"))
    return cipher.encrypt(padded)

def aes_decrypt_ecb(ciphertext: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)

    try:
        unpadded = unpad(decrypted)
        return unpadded.decode("utf-8")
    except:
        return decrypted  # fallback raw bytes

# -------------------------
# RSA OAEP
# -------------------------
def load_rsa_public_key(path: str):
    with open(path, "rb") as f:
        return RSA.import_key(f.read())

def load_rsa_private_key(path: str):
    with open(path, "rb") as f:
        return RSA.import_key(f.read())

def rsa_encrypt_aes_key(aes_key: bytes, public_key: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(aes_key)

def rsa_decrypt_aes_key(enc_key: bytes, private_key: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(enc_key)
