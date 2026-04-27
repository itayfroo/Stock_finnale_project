import os
import time
from Crypto.PublicKey import RSA

KEY_FOLDER = "keys"
PRIVATE_KEY_PATH = os.path.join(KEY_FOLDER, "private.pem")
PUBLIC_KEY_PATH = os.path.join(KEY_FOLDER, "public.pem")

def rotate_keys():
    if not os.path.exists(KEY_FOLDER):
        os.makedirs(KEY_FOLDER)

    while True:
        print("\n[KEY MANAGER] Generating new RSA keys...")

        key = RSA.generate(2048)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key)

        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_key)

        print("[KEY MANAGER] New keys activated.")
        print("Private key saved at:", os.path.abspath(PRIVATE_KEY_PATH))
        print("Public key saved at:", os.path.abspath(PUBLIC_KEY_PATH))

        time.sleep(180)

if __name__ == "__main__":
    rotate_keys()