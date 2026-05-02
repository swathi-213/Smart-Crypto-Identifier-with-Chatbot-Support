import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


# -------------------------------------------------
# Helper: bytes → hex (DISPLAY ONLY)
# -------------------------------------------------
def to_hex(data: bytes) -> str:
    return data.hex()


def reencrypt_data(data: bytes, algorithm: str):

    # ---------- SYMMETRIC ----------
    if algorithm.startswith(("AES", "ChaCha20")):
        return encrypt_aes_gcm(data)

    # ---------- ASYMMETRIC (HYBRID) ----------
    if algorithm.startswith("RSA"):
        return hybrid_rsa_aes(data)

    raise ValueError("Unsupported re-encryption algorithm")


def encrypt_aes_gcm(data: bytes):
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)

    return {
        "method": "AES-GCM",

        # ✅ ORIGINAL (unchanged)
        "ciphertext": ciphertext,
        "key": key,
        "nonce": nonce,

        # ✅ ADDED (hex for UI / report)
        "ciphertext_hex": to_hex(ciphertext),
        "key_hex": to_hex(key),
        "nonce_hex": to_hex(nonce)
    }


def hybrid_rsa_aes(data: bytes):
    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aes = AESGCM(aes_key)
    ciphertext = aes.encrypt(nonce, data, None)

    rsa_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    enc_key = rsa_key.public_key().encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return {
        "method": "Hybrid RSA + AES-GCM",

        # ✅ ORIGINAL (unchanged)
        "ciphertext": ciphertext,
        "encrypted_key": enc_key,
        "nonce": nonce,

        # ✅ ADDED (hex for UI / report)
        "ciphertext_hex": to_hex(ciphertext),
        "encrypted_key_hex": to_hex(enc_key),
        "nonce_hex": to_hex(nonce)
    }