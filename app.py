import streamlit as st
from datetime import datetime

from modules.module1_features import extract_features
from modules.module2_detection import detect_algorithm
from modules.module3_usage import DATA_USAGE
from modules.module4_security import analyze_security_by_usage
from modules.module5_reencryption import reencrypt_data


# =====================================================
# PAGE CONFIG (MIN-WIDE)
# =====================================================
st.set_page_config(
    page_title="Cryptographic Security Analyzer",
    layout="wide"
)

# =====================================================
# HIDE SIDEBAR
# =====================================================
st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
button[kind="primary"] {
    border: 2px solid #c084fc;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# THEME + WIDTH CONTROL (UI ONLY)
# =====================================================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1e0b36, #0f0a1a 70%);
}

html, body, [class*="css"] {
    color: #e9d5ff;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-left: 2rem;
    padding-right: 2rem;
}

.card {
    background: linear-gradient(135deg, rgba(88,28,135,0.9), rgba(30,16,60,0.95));
    padding: 1.6rem;
    margin-bottom: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(168,85,247,0.35);
}

.card-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #c084fc;
}
.badge-strong {background:#22c55e;color:black;padding:6px 14px;border-radius:20px;font-weight:700;}
.badge-medium {background:#facc15;color:black;padding:6px 14px;border-radius:20px;font-weight:700;}
.badge-weak {background:#ef4444;color:white;padding:6px 14px;border-radius:20px;font-weight:700;}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE (UNCHANGED LOGIC)
# =====================================================
if "step" not in st.session_state:
    st.session_state.step = 1

for key in ["encrypted_data", "detection", "security_result", "reencrypt_result"]:
    if key not in st.session_state:
        st.session_state[key] = None

st.title("🔐 CipherScope")
st.caption("Unified Cryptographic Security Analysis & Expert Chatbot")

# =====================================================
# TOP NAV (UI ONLY)
# =====================================================
nav1, nav2 = st.columns(2)

with nav1:
    st.button("🔐 Cipher Analysis Engine", use_container_width=True)

with nav2:
    if st.button("🧠 Crypto Chatbot", use_container_width=True):
        st.switch_page("pages/chatbot.py")
# =====================================================
# TITLE
# =====================================================

st.title("🔐 Cipher Analysis Engine")
st.markdown(
    "A step-by-step system for detecting cryptographic algorithms, "
    "evaluating their security based on intended usage, "
    "and performing secure re-encryption."
)


# =====================================================
# STEP 1 — UPLOAD
# =====================================================
st.markdown('<div class="card"><div class="card-title">📥 Upload Encrypted Data</div></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload encrypted file (BIN / DAT / TXT)",
    type=["bin", "dat", "txt"]
)

if uploaded_file:
    st.session_state.encrypted_data = uploaded_file.read()
    st.session_state.step = max(st.session_state.step, 2)


# =====================================================
# STEP 2 — DETECTION
# =====================================================
if st.session_state.step >= 2:
    st.markdown('<div class="card"><div class="card-title">🔍 Algorithm Detection</div></div>', unsafe_allow_html=True)

    if st.button("🚀 Detect Algorithm"):
        features = extract_features(st.session_state.encrypted_data)
        st.session_state.detection = detect_algorithm(features)
        st.session_state.step = 3

    if st.session_state.detection:
        det = st.session_state.detection
        st.write("**Detected Category:**", det["category"])
        st.write("**Detected Algorithm:**", det["algorithm"])


# =====================================================
# STEP 3 — SECURITY ANALYSIS
# =====================================================
if st.session_state.step >= 3:
    st.markdown('<div class="card"><div class="card-title">🛡️ Security Analysis</div></div>', unsafe_allow_html=True)

    selected_usage = st.selectbox("Select intended data usage:", list(DATA_USAGE.keys()))

    if st.button("🔎 Analyze Security"):
        st.session_state.security_result = analyze_security_by_usage(
            detected_algorithm=det["algorithm"],
            data_usage=selected_usage
        )
        st.session_state.step = 4

    if st.session_state.security_result:
        sr = st.session_state.security_result

        badge = {
            "Strong": '<span class="badge-strong">STRONG</span>',
            "Medium": '<span class="badge-medium">MEDIUM</span>',
            "Weak": '<span class="badge-weak">WEAK</span>'
        }[sr["strength_for_usage"]]

        st.markdown(f"**Security Strength:** {badge}", unsafe_allow_html=True)
        st.info(sr["reason"])


# =====================================================
# STEP 4 — RE-ENCRYPTION
# =====================================================
if st.session_state.step >= 4:
    if sr["strength_for_usage"] == "Strong":
        st.success("Detected algorithm is already strong. Re-encryption is not required.")
        st.session_state.step = 5

    elif not sr["reencryption_supported"]:
        st.warning(
            "Re-encryption is not applicable because this use case is intended for "
            "authentication and integrity verification using hash functions and "
            "digital signatures, rather than data encryption."
        )

        st.markdown("**Recommended Algorithms:**")
        st.write(sr["recommended_algorithms"])

        if st.button("➡️ Proceed to Final Report"):
            st.session_state.step = 5

    else:
        st.markdown('<div class="card"><div class="card-title">🔁 Secure Re-Encryption</div></div>', unsafe_allow_html=True)

        selected_algo = st.selectbox(
            "Choose algorithm for secure re-encryption:",
            sr["recommended_algorithms"]
        )

        if st.button("🔐 Re-Encrypt Data"):
            st.session_state.reencrypt_result = reencrypt_data(
                st.session_state.encrypted_data,
                selected_algo
            )
            st.session_state.step = 5


        if st.session_state.reencrypt_result:
            rr = st.session_state.reencrypt_result

            # -------------------------------------------------
            # CREATE HEX REPORT CONTENT
            # -------------------------------------------------
            hex_report = f"""
        Re-Encrypted Data (Hex)
        ----------------------
        {rr["ciphertext_hex"]}
        """

            if "key_hex" in rr:
                hex_report += f"""

        Encryption Key (Hex)
        --------------------
        {rr["key_hex"]}
        """

            hex_report += f"""

        Nonce (Hex)
        -----------
        {rr["nonce_hex"]}
        """

            # -------------------------------------------------
            # DOWNLOAD AS TEXT FILE
            # -------------------------------------------------
            st.download_button(
                label="⬇️ Download Re-Encrypted Hex Report",
                data=hex_report,
                file_name="reencrypted_output_hex.txt",
                mime="text/plain"
            )

# =====================================================
# STEP 5 — REPORT
# =====================================================
if st.session_state.step >= 5:
    st.markdown('<div class="card"><div class="card-title">📄 Final Analysis Report</div></div>', unsafe_allow_html=True)

    report = f"""
Cryptographic Security Analysis Report
-------------------------------------
Timestamp: {datetime.now()}

Detected Algorithm: {det["algorithm"]}
Detected Category: {det["category"]}
Selected Data Usage: {selected_usage}
Security Strength: {sr["strength_for_usage"]}

Explanation:
{sr["reason"]}
"""

    st.download_button("📥 Download Analysis Report", report)