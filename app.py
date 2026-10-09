
import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(
    page_title="Custom Clothing System",
    page_icon="👗",
    layout="centered"
)

st.title("👗 AI-Assisted Custom Clothing System")
st.write(
    "Personalized clothing recommendations using your "
    "body measurements and design preferences."
)

st.info(
    "Prototype version: recommendations use predefined rules. "
    "Pattern calculations are preliminary estimates."
)

st.header("1. Body Measurements")

with st.form("clothing_form"):
    col1, col2 = st.columns(2)

    with col1:
        bust = st.number_input(
            "Bust circumference (cm)", min_value=1.0, value=90.0
        )
        waist = st.number_input(
            "Waist circumference (cm)", min_value=1.0, value=75.0
        )
        hip = st.number_input(
            "Hip circumference (cm)", min_value=1.0, value=98.0
        )
        shoulder = st.number_input(
            "Shoulder width (cm)", min_value=1.0, value=38.0
        )
        armhole = st.number_input(
            "Armhole circumference (cm)", min_value=1.0, value=42.0
        )

    with col2:
        length = st.number_input(
            "Garment length (cm)", min_value=1.0, value=75.0
        )
        sleeve = st.number_input(
            "Sleeve length (cm)", min_value=0.0, value=20.0
        )
        ease = st.number_input(
            "Ease allowance (cm)", min_value=0.0, value=4.0
        )
        seam = st.number_input(
            "Seam allowance (cm)", min_value=0.0, value=1.5
        )

    st.header("2. Design Preferences")

    garment = st.selectbox(
        "Garment type",
        ["Straight Kurti", "A-Line Kurti", "Sleeveless Top"]
    )

    fit = st.selectbox(
        "Preferred fit",
        ["Regular", "Relaxed", "Fitted"]
    )

    occasion = st.selectbox(
        "Occasion",
        ["Everyday", "College", "Workwear", "Festive", "Party"]
    )

    fabric = st.selectbox(
        "Preferred fabric",
        ["Cotton", "Linen", "Rayon", "Silk", "Denim"]
    )

    budget = st.selectbox(
        "Budget",
        ["Under ₹500", "₹500–₹1,000", "₹1,000–₹2,000", "Above ₹2,000"]
    )

    submitted = st.form_submit_button("Generate Recommendation")

if submitted:
    effective_ease = ease

    if fit == "Relaxed":
        effective_ease += 4
    elif fit == "Fitted":
        effective_ease = max(0, ease - 2)

    quarter_bust = bust / 4
    quarter_waist = waist / 4
    quarter_hip = hip / 4

    if occasion == "Workwear":
        recommendation = (
            "Choose a comfortable, structured design. "
            "Cotton or linen may be suitable."
        )
    elif occasion == "Festive":
        recommendation = (
            "Consider decorative details and a fabric "
            "with a suitable drape, such as rayon or silk."
        )
    elif occasion == "Party":
        recommendation = (
            "Consider a stylish silhouette with suitable "
            "fabric drape and finishing."
        )
    elif occasion == "College":
        recommendation = (
            "Choose an easy-care design that allows "
            "comfortable movement."
        )
    else:
        recommendation = (
            "Consider a comfortable everyday design "
            "in a breathable fabric."
        )

    if fabric == "Denim":
        fabric_note = "Check fabric weight and flexibility before drafting."
    elif fabric == "Silk":
        fabric_note = "Consider the fabric's drape and handling requirements."
    else:
        fabric_note = f"{fabric} is your selected fabric preference."

    # Preliminary calculations only; not a complete pattern.
    body_width = max(quarter_bust, quarter_hip)
    estimated_width = body_width + effective_ease / 4
    estimated_cut_width = estimated_width + 2 * seam
    estimated_cut_length = length + 2 * seam

    st.header("3. Your Recommendation")

    st.write(f"**Garment:** {garment}")
    st.write(f"**Fit:** {fit}")
    st.write(f"**Occasion:** {occasion}")
    st.write(f"**Fabric:** {fabric}")
    st.write(f"**Budget:** {budget}")
    st.write(f"**Design suggestion:** {recommendation}")
    st.write(f"**Fabric note:** {fabric_note}")

    st.header("4. Preliminary Measurements")

    col1, col2, col3 = st.columns(3)
    col1.metric("Quarter bust", f"{quarter_bust:.1f} cm")
    col2.metric("Quarter waist", f"{quarter_waist:.1f} cm")
    col3.metric("Quarter hip", f"{quarter_hip:.1f} cm")

    st.write(f"Estimated width: {estimated_width:.2f} cm")
    st.write(f"Estimated cut width: {estimated_cut_width:.2f} cm")
    st.write(f"Estimated cut length: {estimated_cut_length:.2f} cm")

    st.warning(
        "These estimates are not a ready-to-cut pattern. "
        "Real pattern drafting needs garment-specific shaping, "
        "additional measurements, construction details, and fitting tests. "
        "Do not use these estimates alone to cut fabric."
    )

    report = {
        "Garment": garment,
        "Fit": fit,
        "Occasion": occasion,
        "Fabric": fabric,
        "Budget": budget,
        "Recommendation": recommendation,
        "Bust (cm)": bust,
        "Waist (cm)": waist,
        "Hip (cm)": hip,
        "Shoulder (cm)": shoulder,
        "Armhole (cm)": armhole,
        "Garment length (cm)": length,
        "Sleeve length (cm)": sleeve,
        "Ease allowance (cm)": effective_ease,
        "Seam allowance (cm)": seam,
        "Quarter bust (cm)": round(quarter_bust, 2),
        "Quarter waist (cm)": round(quarter_waist, 2),
        "Quarter hip (cm)": round(quarter_hip, 2),
        "Estimated cut width (cm)": round(estimated_cut_width, 2),
        "Estimated cut length (cm)": round(estimated_cut_length, 2)
    }

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4

    y = page_height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(45, y, "Custom Clothing Report")

    y -= 30
    pdf.setFont("Helvetica", 10)

    for key, value in report.items():
        if y < 50:
            pdf.showPage()
            y = page_height - 50
            pdf.setFont("Helvetica", 10)

        line = f"{key}: {value}"
        pdf.drawString(45, y, line[:100])
        y -= 20

    pdf.save()
    buffer.seek(0)

    st.download_button(
        "Download Your PDF Report",
        data=buffer.getvalue(),
        file_name="custom_clothing_report.pdf",
        mime="application/pdf"
    )
