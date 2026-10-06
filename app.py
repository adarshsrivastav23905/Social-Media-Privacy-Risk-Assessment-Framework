import io

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit


st.set_page_config(
    page_title="Social Media Privacy Risk Assessment Framework",
    page_icon="🔒",
    layout="wide",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(99, 102, 241, 0.22), transparent 35%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.18), transparent 30%),
                linear-gradient(135deg, #07111f 0%, #0f172a 28%, #111827 100%);
            color: #e5eefc;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        .hero-panel {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.35);
            backdrop-filter: blur(8px);
            margin-bottom: 1.5rem;
        }

        .brand-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 0.8rem;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            gap: 0.8rem;
            font-weight: 800;
            color: #f8fbff;
            letter-spacing: -0.03em;
        }

        .brand-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(79,70,229,0.2), rgba(14,165,233,0.18));
            border: 1px solid rgba(96,165,250,0.32);
            font-size: 1.35rem;
        }

        .brand-meta {
            font-size: 0.76rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #9fb0cd;
            font-weight: 700;
        }

        .summary-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(120px, 1fr));
            gap: 0.85rem;
            margin-top: 1.2rem;
        }

        .summary-pill {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 0.8rem 0.9rem;
        }

        .summary-pill .label {
            display: block;
            color: #9fb0cd;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }

        .summary-pill .value {
            color: #f8fbff;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .eyebrow {
            display: inline-block;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            background: rgba(99, 102, 241, 0.16);
            border: 1px solid rgba(129, 140, 248, 0.38);
            color: #c7d2fe;
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 0.85rem;
        }

        .hero-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .hero-title h1 {
            margin: 0;
            font-size: clamp(2rem, 3vw, 3rem);
            line-height: 1.1;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: #f8fbff;
        }

        .hero-note {
            color: #afbdd8;
            font-size: 0.97rem;
            margin-top: 0.45rem;
        }

        .premium-chip {
            padding: 0.72rem 1rem;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(16,185,129,0.15));
            border: 1px solid rgba(96, 165, 250, 0.35);
            color: #dbeafe;
            font-weight: 600;
            min-width: 150px;
            text-align: center;
        }

        .panel {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 22px;
            padding: 1.2rem 1.1rem;
            box-shadow: 0 10px 30px rgba(2, 6, 23, 0.25);
            margin-bottom: 1.2rem;
        }

        .panel h3,
        .panel h4,
        .panel h5 {
            color: #f8fbff;
            margin-top: 0;
        }

        .stForm {
            background: rgba(15, 23, 42, 0.35);
            border-radius: 20px;
            padding: 0.4rem 0.1rem 0.2rem;
        }

        div[data-testid="stHorizontalBlock"] > div {
            padding: 0.1rem 0.2rem;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.9), rgba(17, 24, 39, 0.9));
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 1rem 1rem 0.7rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
            animation: fadeInUp 0.6s ease-out;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(8px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        div[data-testid="stMetricLabel"] {
            color: #9fb0cd !important;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: #f8fbff !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em;
        }

        .status-box {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-weight: 700;
            font-size: 0.95rem;
            padding: 0.7rem 1rem;
            border-radius: 14px;
            margin-top: 0.7rem;
            border: 1px solid transparent;
        }

        .status-low { background: rgba(34, 197, 94, 0.12); color: #a7f3d0; border-color: rgba(34, 197, 94, 0.36); }
        .status-moderate { background: rgba(250, 204, 21, 0.12); color: #fde68a; border-color: rgba(250, 204, 21, 0.36); }
        .status-high { background: rgba(249, 115, 22, 0.12); color: #fed7aa; border-color: rgba(249, 115, 22, 0.36); }
        .status-critical { background: rgba(239, 68, 68, 0.12); color: #fecaca; border-color: rgba(239, 68, 68, 0.36); }

        .risk-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.5rem 0.8rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            border: 1px solid rgba(255,255,255,0.15);
        }

        .risk-badge.low { background: rgba(34,197,94,0.12); color: #a7f3d0; border-color: rgba(34,197,94,0.32); }
        .risk-badge.moderate { background: rgba(250,204,21,0.12); color: #fde68a; border-color: rgba(250,204,21,0.32); }
        .risk-badge.high { background: rgba(249,115,22,0.12); color: #fed7aa; border-color: rgba(249,115,22,0.32); }
        .risk-badge.critical { background: rgba(239,68,68,0.12); color: #fecaca; border-color: rgba(239,68,68,0.32); }

        .score-shell {
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 1rem;
            align-items: start;
            margin-top: 1rem;
        }

        .score-value {
            font-size: clamp(2.4rem, 6vw, 4.6rem);
            font-weight: 900;
            letter-spacing: -0.07em;
            line-height: 0.9;
            color: #f8fbff;
            animation: fadeInUp 0.7s ease-out;
        }

        .score-value span {
            font-size: 1.1rem;
            letter-spacing: 0;
            color: #9fb0cd;
            margin-left: 0.35rem;
        }

        .summary-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 18px;
            padding: 1rem 1.2rem;
        }

        .summary-card p {
            margin: 0;
            color: #dfeaf9;
            line-height: 1.7;
        }

        .risk-list li {
            margin-bottom: 0.55rem;
            color: #e6ecf8;
        }

        .stSidebar {
            background: rgba(2, 6, 23, 0.88);
        }

        .stSidebar > div {
            padding-top: 1.2rem;
        }

        .stSidebar .css-17lntkn {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 18px;
            padding: 1rem;
        }

        .st-bb {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 14px;
        }

        .stButton > button {
            background: linear-gradient(135deg, #4f46e5, #0284c7);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.72rem 1.15rem;
            font-weight: 700;
            box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
        }

        .stButton > button:hover {
            filter: brightness(1.08);
        }

        @media (max-width: 800px) {
            .summary-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .score-shell {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 1200px) {
            .summary-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.55rem;
                margin-top: 0.9rem;
            }

            .hero-panel {
                padding: 0.95rem 1rem;
                margin-bottom: 0.9rem;
            }

            .hero-title h1 {
                font-size: 1.55rem;
            }

            .hero-note {
                font-size: 0.88rem;
            }

            .brand-row {
                gap: 0.6rem;
                margin-bottom: 0.6rem;
            }

            .premium-chip {
                min-width: 0;
                padding: 0.6rem 0.75rem;
            }

            .summary-pill {
                padding: 0.55rem 0.65rem;
            }

            .summary-pill .value {
                font-size: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def calculate_risk(data):
    score = 0
    drivers = []

    risk_map = {
        "Private": 10,
        "Restricted": 28,
        "Public": 52,
    }
    score += risk_map.get(data["profile_visibility"], 0)
    drivers.append(("Profile visibility", risk_map.get(data["profile_visibility"], 0)))

    score += data["personal_data_exposure"] * 0.35
    drivers.append(("Personal data exposure", round(data["personal_data_exposure"] * 0.35, 1)))

    score += data["connected_apps"] * 6
    drivers.append(("Third-party app links", data["connected_apps"] * 6))

    score += data["posting_frequency"] * 2.5
    drivers.append(("Posting frequency", round(data["posting_frequency"] * 2.5, 1)))

    score += data["followers"] / 200
    drivers.append(("Audience size", round(data["followers"] / 200, 1)))

    if data["location_sharing"] == "Always on":
        score += 25
    elif data["location_sharing"] == "Only when posting":
        score += 12
    drivers.append(("Location sharing", 25 if data["location_sharing"] == "Always on" else 12 if data["location_sharing"] == "Only when posting" else 0))

    if not data["mfa"]:
        score += 18
        drivers.append(("MFA coverage", 18))
    else:
        score -= 8
        drivers.append(("MFA coverage", -8))

    device_map = {"Strong": -10, "Average": 8, "Weak": 20}
    score += device_map.get(data["device_security"], 0)
    drivers.append(("Device security", device_map.get(data["device_security"], 0)))

    password_map = {"Strong": -12, "Moderate": 8, "Weak": 22}
    score += password_map.get(data["password_hygiene"], 0)
    drivers.append(("Password hygiene", password_map.get(data["password_hygiene"], 0)))

    privacy_map = {"Locked down": -10, "Balanced": 8, "Open": 18}
    score += privacy_map.get(data["privacy_controls"], 0)
    drivers.append(("Privacy controls", privacy_map.get(data["privacy_controls"], 0)))

    age_score = 0
    if data["account_age_months"] > 60:
        age_score = 10
    elif data["account_age_months"] > 24:
        age_score = 6
    score += age_score
    drivers.append(("Account age footprint", age_score))

    score = max(0, min(100, round(score)))

    if score < 30:
        level = "Low risk"
        summary = "Your current privacy posture is relatively strong. Continue reducing exposure and review stale permissions regularly."
    elif score < 60:
        level = "Moderate risk"
        summary = "Your profile has some exposure that could be exploited. Tighten controls and reduce unnecessary data sharing."
    elif score < 80:
        level = "High risk"
        summary = "The platform profile is carrying considerable exposure. A targeted security reset is recommended soon."
    else:
        level = "Critical risk"
        summary = "Your current settings present a material privacy and social engineering risk. Immediate remediation is advised."

    recommendations = []
    if data["profile_visibility"] in {"Restricted", "Public"}:
        recommendations.append("Restrict profile visibility to friends or trusted users only.")
    if data["personal_data_exposure"] >= 60:
        recommendations.append("Reduce the amount of personal information visible on your profile.")
    if data["connected_apps"] >= 3:
        recommendations.append("Review and revoke third-party app access that is no longer needed.")
    if not data["mfa"]:
        recommendations.append("Enable multi-factor authentication for account recovery and logins.")
    if data["location_sharing"] != "Never":
        recommendations.append("Disable geotagging and location sharing in posts and account settings.")
    if data["password_hygiene"] != "Strong":
        recommendations.append("Use a unique, strong password and rotate it regularly.")
    if data["device_security"] == "Weak":
        recommendations.append("Strengthen device protection with antivirus, screen lock, and device encryption.")
    if data["privacy_controls"] == "Open":
        recommendations.append("Set stricter privacy controls for tags, comments, follower requests, and message filtering.")
    if not recommendations:
        recommendations.append("Keep monitoring your account and review privacy settings quarterly.")

    chart_data = pd.DataFrame(drivers, columns=["Factor", "Weight"]).sort_values("Weight", ascending=False)
    return score, level, summary, recommendations, chart_data


def get_risk_band(score):
    if score < 30:
        return "low"
    if score < 60:
        return "moderate"
    if score < 80:
        return "high"
    return "critical"


def build_radar_values(data):
    visibility = {"Private": 15, "Restricted": 45, "Public": 80}
    risk_vectors = {
        "profile_visibility": visibility.get(data["profile_visibility"], 30),
        "personal_data_exposure": min(100, data["personal_data_exposure"]),
        "connected_apps": min(100, data["connected_apps"] * 8),
        "location_sharing": 0 if data["location_sharing"] == "Never" else 50 if data["location_sharing"] == "Only when posting" else 95,
        "mfa": 0 if data["mfa"] else 80,
        "device_security": {"Strong": 20, "Average": 55, "Weak": 90}.get(data["device_security"], 50),
    }
    labels = ["Visibility", "Data", "Apps", "Location", "MFA", "Device"]
    values = [
        risk_vectors["profile_visibility"],
        risk_vectors["personal_data_exposure"],
        risk_vectors["connected_apps"],
        risk_vectors["location_sharing"],
        risk_vectors["mfa"],
        risk_vectors["device_security"],
    ]
    return labels, values


def build_risk_history(score):
    history = [max(8, score - 22), max(10, score - 16), max(14, score - 10), max(18, score - 6), score]
    stages = ["Earlier", "Stage 2", "Stage 3", "Recent", "Current"]
    return stages, history


def build_report(data, score, level, summary, recommendations):
    lines = [
        "Social Media Privacy Risk Assessment Report",
        "=" * 42,
        f"Platform: {data['platform']}",
        f"Risk score: {score}/100",
        f"Risk level: {level}",
        f"Summary: {summary}",
        "",
        "Priority recommendations:",
    ]
    lines.extend(f"- {item}" for item in recommendations)
    return "\n".join(lines)


def build_pdf_report(data, score, level, summary, recommendations):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4
    margin = 48
    content_width = page_width - 2 * margin

    pdf.setTitle("Social Media Privacy Risk Assessment Report")
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.roundRect(margin, page_height - 148, content_width, 100, 14, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#a5b4fc"))
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(margin + 20, page_height - 72, "NEXAGUARD  /  PRIVACY INTELLIGENCE")
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawString(margin + 20, page_height - 101, "Social Media Privacy Risk Report")
    pdf.setFillColor(HexColor("#cbd5e1"))
    pdf.setFont("Helvetica", 9)
    pdf.drawRightString(page_width - margin - 20, page_height - 72, "EXECUTIVE ASSESSMENT")

    card_y = page_height - 244
    pdf.setFillColor(HexColor("#f1f5f9"))
    pdf.roundRect(margin, card_y, content_width, 76, 12, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(margin + 18, card_y + 37, f"{score}/100")
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(margin + 18, card_y + 18, level)
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(page_width - margin - 18, card_y + 43, f"Platform: {data['platform']}")
    pdf.drawRightString(page_width - margin - 18, card_y + 25, "Assessment type: Privacy exposure review")

    y = card_y - 32
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin, y, "Executive summary")
    y -= 18
    pdf.setFillColor(HexColor("#334155"))
    pdf.setFont("Helvetica", 10)
    for line in simpleSplit(summary, "Helvetica", 10, content_width):
        pdf.drawString(margin, y, line)
        y -= 14

    y -= 12
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin, y, "Assessment profile")
    y -= 14
    profile_items = [
        ("Profile visibility", data["profile_visibility"]),
        ("Personal data exposed", f"{data['personal_data_exposure']}%"),
        ("Connected apps", str(data["connected_apps"])),
        ("Location sharing", data["location_sharing"]),
        ("Multi-factor authentication", "Enabled" if data["mfa"] else "Not enabled"),
        ("Password hygiene", data["password_hygiene"]),
        ("Device security", data["device_security"]),
        ("Privacy controls", data["privacy_controls"]),
    ]
    column_gap = 12
    cell_width = (content_width - column_gap) / 2
    for row in range(4):
        row_y = y - 34
        for column in range(2):
            label, value = profile_items[row * 2 + column]
            cell_x = margin + column * (cell_width + column_gap)
            pdf.setFillColor(HexColor("#f1f5f9"))
            pdf.roundRect(cell_x, row_y, cell_width, 30, 6, fill=1, stroke=0)
            pdf.setFillColor(HexColor("#64748b"))
            pdf.setFont("Helvetica-Bold", 7)
            pdf.drawString(cell_x + 9, row_y + 18, label.upper())
            pdf.setFillColor(HexColor("#0f172a"))
            pdf.setFont("Helvetica", 9)
            pdf.drawString(cell_x + 9, row_y + 7, value[:55])
        y = row_y - 8

    y -= 2
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margin, y, "Recommended actions")
    y -= 20

    pdf.setFont("Helvetica", 10)
    for item in recommendations:
        wrapped_lines = simpleSplit(item, "Helvetica", 10, content_width - 20)
        needed_height = len(wrapped_lines) * 14 + 7
        if y - needed_height < 72:
            pdf.showPage()
            y = page_height - 60
            pdf.setFillColor(HexColor("#0f172a"))
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(margin, y, "Recommended actions (continued)")
            y -= 24
            pdf.setFont("Helvetica", 10)

        pdf.setFillColor(HexColor("#4f46e5"))
        pdf.circle(margin + 3, y + 3, 2, fill=1, stroke=0)
        pdf.setFillColor(HexColor("#334155"))
        for line in wrapped_lines:
            pdf.drawString(margin + 14, y, line)
            y -= 14
        y -= 7

    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.line(margin, 54, page_width - margin, 54)
    pdf.setFillColor(HexColor("#64748b"))
    pdf.setFont("Helvetica", 8)
    pdf.drawString(margin, 40, "Screening aid only; not a legal, compliance, or platform security audit.")
    pdf.drawRightString(page_width - margin, 40, "NexaGuard")
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


def build_heatmap_data(data):
    labels = [
        "Visibility",
        "Personal data",
        "Connected apps",
        "Posting",
        "Audience",
        "Location",
        "MFA",
        "Device",
        "Password",
        "Privacy controls",
        "Account age",
    ]
    values = [
        {"Private": 15, "Restricted": 45, "Public": 80}[data["profile_visibility"]],
        data["personal_data_exposure"],
        min(100, data["connected_apps"] * 10),
        min(100, data["posting_frequency"] * 5),
        min(100, round(data["followers"] / 200)),
        {"Never": 0, "Only when posting": 50, "Always on": 95}[data["location_sharing"]],
        0 if data["mfa"] else 80,
        {"Strong": 20, "Average": 55, "Weak": 90}[data["device_security"]],
        {"Strong": 15, "Moderate": 55, "Weak": 90}[data["password_hygiene"]],
        {"Locked down": 15, "Balanced": 50, "Open": 90}[data["privacy_controls"]],
        20 if data["account_age_months"] <= 24 else 40 if data["account_age_months"] <= 60 else 65,
    ]
    return labels, [values]


st.markdown(
    """
    <div class="hero-panel">
        <div class="brand-row">
            <div class="brand-mark">
                <span class="brand-icon">🔒</span>
                <div>
                    <div style="font-size:0.8rem; color:#9fb0cd; letter-spacing:0.12em; text-transform:uppercase; font-weight:700;">Privacy intelligence</div>
                    <div style="font-size:1.1rem;">NexaGuard</div>
                </div>
            </div>
            <div class="premium-chip">Live advisory</div>
        </div>
        <div class="hero-title">
            <div>
                <h1>Social Media Privacy Risk Assessment Framework</h1>
                <div class="hero-note">Evaluate exposure, security posture, and behavioral risk in one premium-grade assessment.</div>
            </div>
        </div>
        <div class="summary-strip">
            <div class="summary-pill"><span class="label">Scoring scale</span><span class="value">0–100</span></div>
            <div class="summary-pill"><span class="label">Platforms</span><span class="value">6 supported</span></div>
            <div class="summary-pill"><span class="label">Risk factors</span><span class="value">11 assessed</span></div>
            <div class="summary-pill"><span class="label">Report export</span><span class="value">PDF ready</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

assessment_summary_slot = st.container()

with st.form("risk_form"):
    st.markdown('<div class="panel"><h3>Account and privacy settings</h3></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        platform = st.selectbox("Primary platform", ["Instagram", "Facebook", "X", "LinkedIn", "TikTok", "Snapchat"])
        account_age_months = st.slider("Account age (months)", 1, 120, 24)
        profile_visibility = st.radio("Profile visibility", ["Private", "Restricted", "Public"], index=1, horizontal=True)
        personal_data_exposure = st.slider("Personal data visible on profile (%)", 0, 100, 35)

    with col2:
        connected_apps = st.slider("Connected third-party apps", 0, 15, 1)
        posting_frequency = st.slider("Posts per day", 0, 20, 1)
        followers = st.slider("Followers or connections", 0, 20000, 500)
        location_sharing = st.selectbox("Location sharing", ["Never", "Only when posting", "Always on"])

    with col3:
        mfa = st.toggle("Multi-factor authentication enabled", value=True)
        password_hygiene = st.selectbox("Password hygiene", ["Strong", "Moderate", "Weak"], index=1)
        device_security = st.selectbox("Device security", ["Strong", "Average", "Weak"], index=1)
        privacy_controls = st.selectbox("Privacy controls", ["Locked down", "Balanced", "Open"])

    submitted = st.form_submit_button("Assess risk")

if "show_assessment" not in st.session_state:
    st.session_state.show_assessment = True
if "is_example_assessment" not in st.session_state:
    st.session_state.is_example_assessment = True
if submitted:
    st.session_state.show_assessment = True
    st.session_state.is_example_assessment = False

if st.session_state.show_assessment:
    data = {
        "platform": platform,
        "account_age_months": account_age_months,
        "profile_visibility": profile_visibility,
        "personal_data_exposure": personal_data_exposure,
        "connected_apps": connected_apps,
        "posting_frequency": posting_frequency,
        "followers": followers,
        "location_sharing": location_sharing,
        "mfa": mfa,
        "password_hygiene": password_hygiene,
        "device_security": device_security,
        "privacy_controls": privacy_controls,
    }

    score, level, summary, recommendations, chart_data = calculate_risk(data)
    risk_band = get_risk_band(score)
    radar_labels, radar_values = build_radar_values(data)
    trend_months, trend_scores = build_risk_history(score)
    heatmap_labels, heatmap_matrix = build_heatmap_data(data)
    report_text = build_report(data, score, level, summary, recommendations)
    pdf_report = build_pdf_report(data, score, level, summary, recommendations)
    with assessment_summary_slot:
        st.caption(
            "Illustrative sample assessment — adjust the inputs and select Assess risk to evaluate a specific account."
            if st.session_state.is_example_assessment
            else "Assessment generated from the submitted account settings."
        )
        st.markdown(
            """
            <div class="panel">
                <div class="eyebrow">Executive summary</div>
                <div class="score-shell">
                    <div>
                        <div class="score-value">{score}<span>/100</span></div>
                        <div class="risk-badge {risk_band}">{level}</div>
                    </div>
                    <div class="summary-card">
                        <p>{summary}</p>
                    </div>
                </div>
            </div>
            """.format(score=score, risk_band=risk_band, level=level, summary=summary),
            unsafe_allow_html=True,
        )

        score_cards = st.columns(2)
        with score_cards[0]:
            st.metric("Risk score", f"{score}/100")
        with score_cards[1]:
            st.metric("Risk level", level)

        detail_cards = st.columns(2)
        with detail_cards[0]:
            st.metric("Platform", platform)
        with detail_cards[1]:
            st.metric("Exposure", f"{personal_data_exposure}%")

        st.markdown(
            """
            <div class="panel">
                <h3>Severity legend</h3>
                <div style="display:flex; flex-wrap:wrap; gap:10px; margin-top:10px;">
                    <span style="display:inline-flex; align-items:center; gap:8px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.36); color:#a7f3d0; padding:6px 10px; border-radius:999px;">● Low</span>
                    <span style="display:inline-flex; align-items:center; gap:8px; background:rgba(250,204,21,0.12); border:1px solid rgba(250,204,21,0.36); color:#fde68a; padding:6px 10px; border-radius:999px;">● Moderate</span>
                    <span style="display:inline-flex; align-items:center; gap:8px; background:rgba(249,115,22,0.12); border:1px solid rgba(249,115,22,0.36); color:#fed7aa; padding:6px 10px; border-radius:999px;">● High</span>
                    <span style="display:inline-flex; align-items:center; gap:8px; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.36); color:#fecaca; padding:6px 10px; border-radius:999px;">● Critical</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(score / 100)

    chart_col, rec_col = st.columns([1.5, 1])
    with chart_col:
        st.markdown('<div class="panel"><h3>Risk drivers</h3></div>', unsafe_allow_html=True)
        risk_driver_data = chart_data.sort_values("Weight", ascending=True)
        risk_driver_fig = go.Figure(
            go.Bar(
                x=risk_driver_data["Weight"],
                y=risk_driver_data["Factor"],
                orientation="h",
                marker_color=[
                    "#22c55e" if weight < 0 else "#7c3aed"
                    for weight in risk_driver_data["Weight"]
                ],
                text=risk_driver_data["Weight"],
                textposition="outside",
                hovertemplate="%{y}: %{x} points<extra></extra>",
            )
        )
        risk_driver_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            margin=dict(l=10, r=30, t=10, b=35),
            height=460,
            xaxis=dict(title="Contribution to score", zeroline=True, zerolinecolor="#64748b"),
            yaxis=dict(title=None, automargin=True),
            showlegend=False,
        )
        st.plotly_chart(risk_driver_fig, width="stretch")

        heatmap_fig = go.Figure(data=go.Heatmap(
            z=heatmap_matrix,
            x=heatmap_labels,
            y=['Current profile'],
            colorscale=[[0, '#0ea5e9'], [0.5, '#8b5cf6'], [1, '#f43f5e']],
            zmin=0,
            zmax=100,
            hovertemplate='Factor: %{x}<br>Exposure: %{z}%<extra></extra>'
        ))
        heatmap_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=20, r=20, t=10, b=20),
            showlegend=False,
        )
        st.markdown('<div class="panel"><h3>Risk heatmap</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(heatmap_fig, width="stretch")

        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=radar_values,
                theta=radar_labels,
                fill='toself',
                line=dict(color='#7c3aed', width=3),
                marker=dict(color='#60a5fa', size=8),
                name='Exposure profile',
            )
        )
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(15, 23, 42, 0.78)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(148, 163, 184, 0.35)",
                    linecolor="rgba(148, 163, 184, 0.35)",
                    tickfont=dict(color="#9fb0cd"),
                ),
                angularaxis=dict(
                    gridcolor="rgba(148, 163, 184, 0.3)",
                    linecolor="rgba(148, 163, 184, 0.35)",
                    tickfont=dict(color="#e2e8f0"),
                ),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=30, r=30, t=30, b=30),
            showlegend=False,
        )
        st.markdown('<div class="panel"><h3>Exposure radar</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(fig, width="stretch")

        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(x=trend_months, y=trend_scores, mode='lines+markers', line=dict(color='#22c55e', width=3), marker=dict(size=8, color='#a7f3d0')))
        trend_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=20, r=20, t=10, b=10),
            xaxis_title='Period',
            yaxis_title='Risk score',
            yaxis=dict(range=[0, 100]),
            showlegend=False,
        )
        st.markdown('<div class="panel"><h3>Illustrative risk trajectory</h3></div>', unsafe_allow_html=True)
        st.caption("Simulated demo trajectory only; historical account scores are not stored.")
        st.plotly_chart(trend_fig, width="stretch")

    with rec_col:
        st.markdown('<div class="panel"><h3>Recommended actions</h3></div>', unsafe_allow_html=True)
        st.markdown("<ul class='risk-list'>" + "".join(f"<li>{item}</li>" for item in recommendations) + "</ul>", unsafe_allow_html=True)
        st.download_button(
            label="Download PDF report",
            data=pdf_report,
            file_name=f"{platform.lower()}_privacy_risk_report.pdf",
            mime="application/pdf",
            width="stretch",
        )

    st.markdown(
        """
        <div class="panel">
            <h3>Framework interpretation</h3>
            <p>This framework combines visibility, account hygiene, third-party integrations, and device behavior into a single risk indicator. Use it as a practical screening tool rather than a legal or compliance calculation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="panel">
            <h3>Privacy profile snapshot</h3>
            <p>Complete the assessment form to generate a privacy risk profile.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    """
    <div class="panel">
        <h3>Framework summary</h3>
        <p>The model highlights the balance between exposed personal data, public profile footprint, and security controls such as MFA and strong device hygiene.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
