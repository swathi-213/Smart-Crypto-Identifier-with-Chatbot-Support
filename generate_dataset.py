from pathlib import Path
from Crypto.Cipher import AES, DES, DES3, Blowfish, CAST, ARC4, ChaCha20, Salsa20, PKCS1_OAEP
from Crypto.PublicKey import RSA, DSA, ECC
from Crypto.Signature import DSS
from Crypto.Hash import (
    MD5, SHA1, SHA224, SHA256, SHA384, SHA512,
    SHA3_256, SHA3_384, SHA3_512, RIPEMD160
)
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
# ---------------- CONFIG ----------------
OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLES = 200
DATA_SIZE = 1024  # 1 KB

# ---------------- SYMMETRIC BLOCK (10) ----------------
def aes_cbc(d): return AES.new(get_random_bytes(16), AES.MODE_CBC, get_random_bytes(16)).encrypt(pad(d, 16))
def aes_ctr(d): return AES.new(get_random_bytes(16), AES.MODE_CTR).encrypt(d)
def aes_cfb(d): return AES.new(get_random_bytes(16), AES.MODE_CFB, get_random_bytes(16)).encrypt(d)
def aes_ofb(d): return AES.new(get_random_bytes(16), AES.MODE_OFB, get_random_bytes(16)).encrypt(d)

def des_cbc(d): return DES.new(get_random_bytes(8), DES.MODE_CBC, get_random_bytes(8)).encrypt(pad(d, 8))
def des3_cbc(d): return DES3.new(DES3.adjust_key_parity(get_random_bytes(24)), DES3.MODE_CBC, get_random_bytes(8)).encrypt(pad(d, 8))

def blowfish_cbc(d): return Blowfish.new(get_random_bytes(16), Blowfish.MODE_CBC, get_random_bytes(8)).encrypt(pad(d, 8))
def blowfish_cfb(d): return Blowfish.new(get_random_bytes(16), Blowfish.MODE_CFB, get_random_bytes(8)).encrypt(d)

def cast_cbc(d): return CAST.new(get_random_bytes(16), CAST.MODE_CBC, get_random_bytes(8)).encrypt(pad(d, 8))
def cast_cfb(d): return CAST.new(get_random_bytes(16), CAST.MODE_CFB, get_random_bytes(8)).encrypt(d)

# ---------------- STREAM (10) ----------------
def rc4_128(d): return ARC4.new(get_random_bytes(16)).encrypt(d)
def rc4_256(d): return ARC4.new(get_random_bytes(32)).encrypt(d)

def chacha20_64(d): return ChaCha20.new(key=get_random_bytes(32), nonce=get_random_bytes(8)).encrypt(d)
def chacha20_96(d): return ChaCha20.new(key=get_random_bytes(32), nonce=get_random_bytes(12)).encrypt(d)

def salsa20_64(d): return Salsa20.new(key=get_random_bytes(32), nonce=get_random_bytes(8)).encrypt(d)

def aes_ctr_stream(d): return AES.new(get_random_bytes(16), AES.MODE_CTR).encrypt(d)
def aes_cfb_stream(d): return AES.new(get_random_bytes(16), AES.MODE_CFB, get_random_bytes(16)).encrypt(d)
def aes_ofb_stream(d): return AES.new(get_random_bytes(16), AES.MODE_OFB, get_random_bytes(16)).encrypt(d)
def aes_gcm_stream(d): return AES.new(get_random_bytes(16), AES.MODE_GCM).encrypt(d)
def aes_ccm_stream(d): return AES.new(get_random_bytes(16), AES.MODE_CCM).encrypt(d)

# ---------------- ASYMMETRIC (10) ----------------
def rsa_oaep_2048(d):
    k = RSA.generate(2048)
    return PKCS1_OAEP.new(k.publickey()).encrypt(d[:190])

def rsa_oaep_3072(d):
    k = RSA.generate(3072)
    return PKCS1_OAEP.new(k.publickey()).encrypt(d[:190])

def rsa_oaep_1024(d):
    k = RSA.generate(1024)
    return PKCS1_OAEP.new(k.publickey()).encrypt(d[:86])

def dsa_2048(d):
    k = DSA.generate(2048)
    return DSS.new(k, "fips-186-3").sign(SHA256.new(d))

def dsa_3072(d):
    k = DSA.generate(3072)
    return DSS.new(k, "fips-186-3").sign(SHA256.new(d))

def ecdsa_p256(d):
    k = ECC.generate(curve="P-256")
    return DSS.new(k, "fips-186-3").sign(SHA256.new(d))

def ecdsa_p384(d):
    k = ECC.generate(curve="P-384")
    return DSS.new(k, "fips-186-3").sign(SHA256.new(d))

def ecdsa_p521(d):
    k = ECC.generate(curve="P-521")
    return DSS.new(k, "fips-186-3").sign(SHA256.new(d))

def rsa_pss(d):
    key = RSA.generate(2048)
    h = SHA256.new(d)
    signer = pss.new(key)
    return signer.sign(h)

def rsa_pkcs1v15(d):
    k = RSA.generate(2048)
    return PKCS1_OAEP.new(k.publickey()).encrypt(d[:190])

# ---------------- HASH (10) ----------------
def h_md5(d): return MD5.new(d).digest()
def h_sha1(d): return SHA1.new(d).digest()
def h_sha224(d): return SHA224.new(d).digest()
def h_sha256(d): return SHA256.new(d).digest()
def h_sha384(d): return SHA384.new(d).digest()
def h_sha512(d): return SHA512.new(d).digest()
def h_sha3_256(d): return SHA3_256.new(d).digest()
def h_sha3_384(d): return SHA3_384.new(d).digest()
def h_sha3_512(d): return SHA3_512.new(d).digest()
def h_ripemd160(d): return RIPEMD160.new(d).digest()

# ---------------- ALGORITHMS (40 TOTAL) ----------------
ALGORITHMS = {

    # Symmetric Block
    "AES-CBC": aes_cbc,
    "AES-CTR": aes_ctr,
    "AES-CFB": aes_cfb,
    "AES-OFB": aes_ofb,
    "DES-CBC": des_cbc,
    "3DES-CBC": des3_cbc,
    "Blowfish-CBC": blowfish_cbc,
    "Blowfish-CFB": blowfish_cfb,
    "CAST-CBC": cast_cbc,
    "CAST-CFB": cast_cfb,

    # Stream
    "RC4-128": rc4_128,
    "RC4-256": rc4_256,
    "ChaCha20-64": chacha20_64,
    "ChaCha20-96": chacha20_96,
    "Salsa20-64": salsa20_64,
    "AES-CTR-Stream": aes_ctr_stream,
    "AES-CFB-Stream": aes_cfb_stream,
    "AES-OFB-Stream": aes_ofb_stream,
    "AES-GCM": aes_gcm_stream,
    "AES-CCM": aes_ccm_stream,

    # Asymmetric
    "RSA-OAEP-2048": rsa_oaep_2048,
    "RSA-OAEP-3072": rsa_oaep_3072,
    "RSA-OAEP-1024": rsa_oaep_1024,
    "DSA-2048": dsa_2048,
    "DSA-3072": dsa_3072,
    "ECDSA-P256": ecdsa_p256,
    "ECDSA-P384": ecdsa_p384,
    "ECDSA-P521": ecdsa_p521,

    "RSA-PSS": rsa_pss,
    "RSA-PKCS1v15": rsa_pkcs1v15,

    # Hash
    "MD5": h_md5,
    "SHA1": h_sha1,
    "SHA224": h_sha224,
    "SHA256": h_sha256,
    "SHA384": h_sha384,
    "SHA512": h_sha512,
    "SHA3-256": h_sha3_256,
    "SHA3-384": h_sha3_384,
    "SHA3-512": h_sha3_512,
    "RIPEMD160": h_ripemd160,
}

# ---------------- GENERATE DATA ----------------
for algo, func in ALGORITHMS.items():
    folder = OUT_DIR / algo
    folder.mkdir(parents=True, exist_ok=True)

    print(f"Generating samples for {algo}")
    for i in range(SAMPLES):
        plaintext = get_random_bytes(DATA_SIZE)
        output = func(plaintext)

        # Store as HEX
        with open(folder / f"sample_{i}.hex", "w") as f:
            f.write(output.hex())