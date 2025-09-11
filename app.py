import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import qrcode
import time
from PIL import Image

# ------------------------
# App Config
# ------------------------
st.set_page_config(page_title="Mentor AI", layout="wide")
st.title("🎓 Mentor AI App")

# ------------------------
# Custom CSS for Sidebar Hover Effect
# ------------------------
st.markdown("""
    <style>
    /* Sidebar hover effect */
    section[data-testid="stSidebar"] .css-1d391kg a {
        display: block;
        padding: 0.6em 1em;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
        font-size: 16px;
        color: #444;
        text-decoration: none;
    }
    section[data-testid="stSidebar"] .css-1d391kg a:hover {
        background-color: #4e8cff;
        color: white;
        font-size: 17px;
        transform: scale(1.01);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------
# Sidebar Navigation
# ------------------------
menu = st.sidebar.radio(
    "📂 Navigate",
    ["Dashboard", "Student Report", "QR Attendance", "Career Prediction", "Personality Quiz"]
)

# ------------------------
# 1. Dashboard
# ------------------------
if menu == "Dashboard":
    st.header("📊 Student Dashboard")

    # Example data
    data = {
        "Semester": [1, 2, 3, 4],
        "CGPA": [7.5, 8.2, 7.9, 8.5],
        "Attendance": [82, 85, 79, 88]  # percentage
    }
    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)

    # CGPA line graph
    with col1:
        st.subheader("📈 CGPA Progress (Line Chart)")
        fig, ax = plt.subplots()
        ax.plot(df["Semester"], df["CGPA"], marker="o", linestyle="-", color="green")
        ax.set_xlabel("Semester")
        ax.set_ylabel("CGPA")
        ax.set_title("CGPA Over Semesters")
        st.pyplot(fig)

    # Attendance pie chart
    with col2:
        st.subheader("📊 Attendance (Pie Chart)")
        latest_attendance = df["Attendance"].iloc[-1]  # last semester attendance
        attended = latest_attendance
        missed = 100 - latest_attendance

        fig2, ax2 = plt.subplots()
        ax2.pie(
            [attended, missed],
            labels=["Attended (%)", "Missed (%)"],
            autopct="%1.1f%%",
            colors=["#4CAF50", "#FF5252"],
            startangle=90
        )
        ax2.axis("equal")  # Equal aspect ratio makes pie chart circular
        st.pyplot(fig2)

    st.info("CGPA shows trend over semesters, Attendance shows latest record.")

# ------------------------
# 2. Student Report
# ------------------------
elif menu == "Student Report":
    st.header("📑 Student Report")

    message = st.text_area("Enter message to parents")
    subject = st.selectbox("Select Subject", ["Math", "Science", "English", "History"])
    semester = st.selectbox("Select Semester", [1,2,3,4,5,6,7,8])
    progress = st.slider("Progress Score", 0, 100)

    if st.button("Save Report"):
        st.success(f"✅ Report saved for {subject}, Semester {semester}")
        st.info(f"📩 Message sent to parents: {message}")

# ------------------------
# 3. QR Attendance
# ------------------------
elif menu == "QR Attendance":
    st.header("📷 QR Attendance")

    if st.button("Generate QR Code"):
        expiry = int(time.time()) + 30  # expires in 30 seconds
        qr_data = f"ATTEND-{expiry}"
        img = qrcode.make(qr_data)
        st.image(img, caption="Scan within 30s", use_column_width=True)
        st.warning("⚠️ QR Code will expire in 30 seconds ⏳")

# ------------------------
# 4. Career Prediction
# ------------------------
elif menu == "Career Prediction":
    st.header("💼 Career Prediction")

    cgpa = st.slider("Enter CGPA", 0.0, 10.0, 7.5)
    attendance = st.slider("Enter Attendance %", 0, 100, 80)

    if st.button("Predict Career"):
        if cgpa > 8 and attendance > 85:
            st.success("🚀 Suggested Career: Data Scientist / Engineer")
        elif cgpa > 7:
            st.success("📈 Suggested Career: Business Analyst / Software Developer")
        else:
            st.success("🎨 Suggested Career: Creative Fields (Design, Arts, etc.)")

# ------------------------
# 5. Personality Quiz
# ------------------------
elif menu == "Personality Quiz":
    st.header("🧠 Personality Quiz")

    questions = [
        "Do you enjoy solving logical problems?",
        "Do you like working with people?",
        "Do you prefer creative tasks over analytical ones?",
        "Do you enjoy technology & coding?",
        "Do you like planning & organizing events?"
    ]

    answers = []
    for q in questions:
        ans = st.radio(q, ["Yes", "No"], key=q)
        answers.append(ans)

    if st.button("Get Career Suggestion"):
        score = answers.count("Yes")
        if score >= 4:
            st.success("🚀 You might excel in Engineering / Data Science")
        elif score >= 2:
            st.success("📊 You might enjoy Management / Business")
        else:
            st.success("🎨 You might be suited for Creative Careers")
