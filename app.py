import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import qrcode
import time
from PIL import Image

# ------------------------
# Title
# ------------------------
st.set_page_config(page_title="Mentor AI", layout="wide")
st.title("🎓 Mentor AI App")

# ------------------------
# 1. Dashboard
# ------------------------
st.header("📊 Student Dashboard")

data = {
    "Semester": [1, 2, 3, 4],
    "CGPA": [7.5, 8.2, 7.9, 8.5],
    "Attendance": [82, 85, 79, 88]
}
df = pd.DataFrame(data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("CGPA Progress")
    st.line_chart(df.set_index("Semester")["CGPA"])

with col2:
    st.subheader("Attendance Scatter Plot")
    fig, ax = plt.subplots()
    ax.scatter(df["Semester"], df["Attendance"], color="blue")
    ax.set_xlabel("Semester")
    ax.set_ylabel("Attendance %")
    st.pyplot(fig)

# ------------------------
# 2. Student Report
# ------------------------
st.header("📑 Student Report")

message = st.text_area("Enter message to parents")
subject = st.selectbox("Select Subject", ["Math", "Science", "English", "History"])
semester = st.selectbox("Select Semester", [1,2,3,4,5,6,7,8])
progress = st.slider("Progress Score", 0, 100)

if st.button("Save Report"):
    st.success(f"Report saved for {subject}, Semester {semester}")
    st.info(f"Message sent to parents: {message}")

# ------------------------
# 3. QR Attendance
# ------------------------
st.header("📷 QR Attendance")

if st.button("Generate QR Code"):
    expiry = int(time.time()) + 30  # expires in 30 seconds
    qr_data = f"ATTEND-{expiry}"
    img = qrcode.make(qr_data)
    st.image(img, caption="Scan within 30s")
    st.warning("QR Code will expire in 30 seconds ⏳")

# ------------------------
# 4. Career Prediction
# ------------------------
st.header("💼 Career Prediction")

cgpa = st.slider("Enter CGPA", 0.0, 10.0, 7.5)
attendance = st.slider("Enter Attendance %", 0, 100, 80)

if st.button("Predict Career"):
    if cgpa > 8 and attendance > 85:
        st.success("Suggested Career: Data Scientist / Engineer 🚀")
    elif cgpa > 7:
        st.success("Suggested Career: Business Analyst / Software Developer 📈")
    else:
        st.success("Suggested Career: Creative Fields (Design, Arts, etc.) 🎨")

# ------------------------
# 5. Personality Quiz
# ------------------------
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
        st.success("You might excel in Engineering / Data Science 🚀")
    elif score >= 2:
        st.success("You might enjoy Management / Business 📊")
    else:
        st.success("You might be suited for Creative Careers 🎨")
