import os
import joblib
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, StandardScaler, label_binarize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

# =====================================================
# DIRECTORIES
# =====================================================
BASE_MODEL_DIR = "models"
STAGE1_DIR = os.path.join(BASE_MODEL_DIR, "stage1")
STAGE2_DIR = os.path.join(BASE_MODEL_DIR, "stage2")
OUTPUT_DIR = "output"

os.makedirs(STAGE1_DIR, exist_ok=True)
os.makedirs(STAGE2_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================
df = pd.read_csv("features_enhanced.csv")

# =====================================================
# ALGORITHM → CATEGORY MAP
# =====================================================
HASH = {
    "MD5","SHA1","SHA224","SHA256","SHA384","SHA512",
    "SHA3-256","SHA3-384","SHA3-512","RIPEMD160"
}
ASYMMETRIC = {
    "RSA-OAEP-2048","RSA-OAEP-3072","RSA-OAEP-1024",
    "RSA-PSS","RSA-PKCS1v15",
    "DSA-2048","DSA-3072",
    "ECDSA-P256","ECDSA-P384","ECDSA-P521"
}
STREAM = {
    "RC4-128","RC4-256","ChaCha20-64","ChaCha20-96","Salsa20-64",
    "AES-CTR-Stream","AES-CFB-Stream","AES-OFB-Stream",
    "AES-GCM","AES-CCM"
}


SYMMETRIC = {
    "AES-CBC","AES-CTR","AES-CFB","AES-OFB",
    "DES-CBC","3DES-CBC",
    "Blowfish-CBC","Blowfish-CFB",
    "CAST-CBC","CAST-CFB"
}

def map_category(algo: str) -> str:
    if algo in HASH:
        return "Hash"
    elif algo in ASYMMETRIC:
        return "Asymmetric"
    elif algo in STREAM:
        return "Stream"
    elif algo in SYMMETRIC:
        return "Symmetric"
    else:
        raise ValueError(f"Unknown algorithm: {algo}")

df["category"] = df["algorithm"].apply(map_category)

# =====================================================
# STAGE-1 : CATEGORY CLASSIFICATION (ENSEMBLE)
# =====================================================
stage1_features = [
    "entropy","chi_square","block_alignment",
    "repeated_block_ratio","byte_run_length",
    "hamming_weight","nibble_imbalance"
]

X1 = df[stage1_features]
le_cat = LabelEncoder()
y1 = le_cat.fit_transform(df["category"])

X1_tr, X1_te, y1_tr, y1_te = train_test_split(
    X1, y1, test_size=0.2, stratify=y1, random_state=42
)

# ---- Models ----
rf1 = RandomForestClassifier(
    n_estimators=800, class_weight="balanced", random_state=42
)

xgb1 = XGBClassifier(
    n_estimators=600, max_depth=6, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.9,
    objective="multi:softprob", eval_metric="mlogloss",
    random_state=42
)

scaler1 = StandardScaler()
X1_tr_s = scaler1.fit_transform(X1_tr)
X1_te_s = scaler1.transform(X1_te)

svm1 = SVC(
    kernel="rbf", C=10,
    probability=True, class_weight="balanced"
)

rf1.fit(X1_tr, y1_tr)
xgb1.fit(X1_tr, y1_tr)
svm1.fit(X1_tr_s, y1_tr)

# ---- Ensemble prediction ----
proba1 = (
    0.40 * xgb1.predict_proba(X1_te) +
    0.35 * rf1.predict_proba(X1_te) +
    0.25 * svm1.predict_proba(X1_te_s)
)
y1_pred = np.argmax(proba1, axis=1)

# =====================================================
# SAVE STAGE-1 MODELS
# =====================================================
joblib.dump(rf1, f"{STAGE1_DIR}/rf.pkl")
joblib.dump(xgb1, f"{STAGE1_DIR}/xgb.pkl")
joblib.dump(svm1, f"{STAGE1_DIR}/svm.pkl")
joblib.dump(scaler1, f"{STAGE1_DIR}/scaler.pkl")
joblib.dump(le_cat, f"{STAGE1_DIR}/label_encoder.pkl")

print("✅ Stage-1 ensemble models saved")

# =====================================================
# STAGE-2 : ALGORITHM CLASSIFICATION (TRAIN + SAVE ONLY)
# =====================================================
stage2_features = [
    c for c in df.columns if c not in ["algorithm","category"]
]

for category in df["category"].unique():
    print(f"\nTraining Stage-2 ensemble for category: {category}")

    cat_dir = os.path.join(STAGE2_DIR, category)
    os.makedirs(cat_dir, exist_ok=True)

    sub = df[df["category"] == category]

    X2 = sub[stage2_features]
    le_algo = LabelEncoder()
    y2 = le_algo.fit_transform(sub["algorithm"])

    X2_tr, _, y2_tr, _ = train_test_split(
        X2, y2, test_size=0.2, stratify=y2, random_state=42
    )

    rf2 = RandomForestClassifier(
        n_estimators=800, class_weight="balanced", random_state=42
    )

    xgb2 = XGBClassifier(
        n_estimators=600, max_depth=6, learning_rate=0.05,
        subsample=0.9, colsample_bytree=0.9,
        objective="multi:softprob", eval_metric="mlogloss",
        random_state=42
    )

    scaler2 = StandardScaler()
    X2_tr_s = scaler2.fit_transform(X2_tr)

    svm2 = SVC(
        kernel="rbf", C=10,
        probability=True, class_weight="balanced"
    )

    rf2.fit(X2_tr, y2_tr)
    xgb2.fit(X2_tr, y2_tr)
    svm2.fit(X2_tr_s, y2_tr)

    joblib.dump(rf2, f"{cat_dir}/rf.pkl")
    joblib.dump(xgb2, f"{cat_dir}/xgb.pkl")
    joblib.dump(svm2, f"{cat_dir}/svm.pkl")
    joblib.dump(scaler2, f"{cat_dir}/scaler.pkl")
    joblib.dump(le_algo, f"{cat_dir}/label_encoder.pkl")

    print(f"✅ Stage-2 ensemble saved for {category}")


# =====================================================
# CONFUSION MATRIX
# =====================================================
cm = confusion_matrix(y1_te, y1_pred)

plt.figure(figsize=(6,5))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=le_cat.classes_,
    yticklabels=le_cat.classes_
)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Stage-1 Category Confusion Matrix")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/stage1_confusion_matrix.png")
plt.close()

# =====================================================
# CLASSIFICATION REPORT
# =====================================================
report = classification_report(
    y1_te, y1_pred, target_names=le_cat.classes_
)

with open(f"{OUTPUT_DIR}/stage1_classification_report.txt", "w") as f:
    f.write(report)

print("\n=== STAGE-1 CLASSIFICATION REPORT ===")
print(report)

# =====================================================
# ROC CURVE (MULTI-CLASS)
# =====================================================
y_bin = label_binarize(y1_te, classes=range(len(le_cat.classes_)))

plt.figure(figsize=(6,5))
for i, cls in enumerate(le_cat.classes_):
    fpr, tpr, _ = roc_curve(y_bin[:, i], proba1[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{cls} (AUC={roc_auc:.2f})")

plt.plot([0,1], [0,1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Stage-1 ROC Curve")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/stage1_roc_curve.png")
plt.close()

print("\n🎉 TRAINING COMPLETE — MODELS + EVALUATION SAVED")