import numpy as np
from collections import Counter


# ---------------- BASIC STAT FEATURES ----------------
def entropy(data):
    counts = np.bincount(data, minlength=256)
    probs = counts / len(data)
    probs = probs[probs > 0]
    return -np.sum(probs * np.log2(probs))

def chi_square(data):
    expected = len(data) / 256
    counts = np.bincount(data, minlength=256)
    return np.sum((counts - expected) ** 2 / expected)

# ---------------- CRYPTO-AWARE FEATURES ----------------
def block_alignment_score(data, block=16):
    blocks = len(data) // block
    if blocks < 2:
        return 0.0
    matches = 0
    for i in range(blocks - 1):
        if np.array_equal(
            data[i*block:(i+1)*block],
            data[(i+1)*block:(i+2)*block]
        ):
            matches += 1
    return matches / blocks

def repeated_block_ratio(data, block=16):
    blocks = [bytes(data[i:i+block]) for i in range(0, len(data), block)]
    if len(blocks) == 0:
        return 0.0
    return 1 - (len(set(blocks)) / len(blocks))

def byte_run_length(data):
    runs = []
    run = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1]:
            run += 1
        else:
            runs.append(run)
            run = 1
    runs.append(run)
    return float(np.mean(runs))

def bigram_variance(data):
    if len(data) < 2:
        return 0.0
    bigrams = Counter(zip(data[:-1], data[1:]))
    return float(np.var(list(bigrams.values())))

def hamming_weight(data):
    return float(np.mean([bin(b).count("1") for b in data]))

def nibble_imbalance(data):
    high = sum(b >> 4 for b in data)
    low = sum(b & 0x0F for b in data)
    return abs(high - low) / len(data)

# ---------------- FEATURE EXTRACTION ----------------
def extract_features(byte_data):
    data = np.frombuffer(byte_data, dtype=np.uint8)

    return {
        "length": len(data),
        "entropy": entropy(data),
        "chi_square": chi_square(data),
        "mean": float(np.mean(data)),
        "std": float(np.std(data)),
        "autocorrelation": float(
            np.corrcoef(data[:-1], data[1:])[0, 1]
        ) if len(data) > 1 else 0.0,

        #  CRYPTO-AWARE FEATURES
        "block_alignment": block_alignment_score(data),
        "repeated_block_ratio": repeated_block_ratio(data),
        "byte_run_length": byte_run_length(data),
        "bigram_variance": bigram_variance(data),
        "hamming_weight": hamming_weight(data),
        "nibble_imbalance": nibble_imbalance(data),
    }
