import os
import joblib
import numpy as np
import pandas as pd

# ---------------- PATHS ----------------
BASE_MODEL_DIR = "models"
STAGE1_DIR = os.path.join(BASE_MODEL_DIR, "stage1")
STAGE2_DIR = os.path.join(BASE_MODEL_DIR, "stage2")

# ---------------- LOAD STAGE-1 ----------------
rf1 = joblib.load(f"{STAGE1_DIR}/rf.pkl")
xgb1 = joblib.load(f"{STAGE1_DIR}/xgb.pkl")
svm1 = joblib.load(f"{STAGE1_DIR}/svm.pkl")
scaler1 = joblib.load(f"{STAGE1_DIR}/scaler.pkl")
le_cat = joblib.load(f"{STAGE1_DIR}/label_encoder.pkl")

STAGE1_FEATURES = [
    "entropy","chi_square","block_alignment",
    "repeated_block_ratio","byte_run_length",
    "hamming_weight","nibble_imbalance"
]

# ---------------- MAIN DETECTION ----------------
def detect_algorithm(features: dict):

    df = pd.DataFrame([features])

    # ===== Stage-1 =====
    X1 = df[STAGE1_FEATURES]
    X1_s = scaler1.transform(X1)

    p1 = (
        0.40 * xgb1.predict_proba(X1) +
        0.35 * rf1.predict_proba(X1) +
        0.25 * svm1.predict_proba(X1_s)
    )

    cat_idx = np.argmax(p1)
    category = le_cat.inverse_transform([cat_idx])[0]
    cat_conf = float(np.max(p1))

    # ===== Stage-2 =====
    cat_dir = os.path.join(STAGE2_DIR, category)

    rf2 = joblib.load(f"{cat_dir}/rf.pkl")
    xgb2 = joblib.load(f"{cat_dir}/xgb.pkl")
    svm2 = joblib.load(f"{cat_dir}/svm.pkl")
    scaler2 = joblib.load(f"{cat_dir}/scaler.pkl")
    le_algo = joblib.load(f"{cat_dir}/label_encoder.pkl")

    X2 = df[scaler2.feature_names_in_]
    X2_s = scaler2.transform(X2)

    p2 = (
        0.40 * xgb2.predict_proba(X2) +
        0.35 * rf2.predict_proba(X2) +
        0.25 * svm2.predict_proba(X2_s)
    )

    algo_idx = np.argmax(p2)
    algorithm = le_algo.inverse_transform([algo_idx])[0]
    algo_conf = float(np.max(p2))

    return {
        "category": category,
        "category_confidence": round(cat_conf, 3),
        "algorithm": algorithm,
        "algorithm_confidence": round(algo_conf, 3),
        "algorithm_probabilities": dict(
            zip(le_algo.classes_, p2[0].round(4))
        )
    }