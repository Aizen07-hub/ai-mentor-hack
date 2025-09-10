import streamlit as st
import pandas as pd
import numpy as np
import qrcode
from io import BytesIO
import streamlit_authenticator as stauth   # ✅ Correct import


st.set_page_config(page_title="AI Mentor", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
names = ["Aziz", "Fasih", "Fazil"]
usernames = ["aziz", "fasih", "fazil"]
passwords = ["1234", "1234", "1234"]  # demo-only passwords

credentials = {
    "usernames": {
        usernames[i]: {"name": names[i], "password": passwords[i]}
        for i in range(len(usernames))
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "ai_mentor_dashboard",    # cookie name
    "abcdef",                 # signature key
    cookie_expiry_days=0      # expires when browser closes
)

name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status == False:
    st.error("❌ Invalid ID or password")
elif authentication_status == None:
    st.warning("Please enter your ID and password")
elif authentication_status:
    authenticator.logout("Logout", location="sidebar")
    st.sidebar.success(f"Welcome {name} 👋")
    
    st.title("🎓 AI Mentor - University Dashboard")
    st.write("Now you can see the full dashboard.")
    # 👉 dashboard code goes here
# -------- Sample Data --------
def create_sample_df():
    data = {
        "name": ["Aman Kumar", "Neha Sharma", "Ravi Singh", "Priya Patel"],
        "roll": ["CS21U001", "CS21U002", "CS21U003", "CS21U004"],
        "parent_name": ["Mr. Kumar", "Ms. Sharma", "Mr. Singh", "Mr. Patel"],
        "parent_contact": ["+911234567890", "+919876543210", "+919112233445", "+918887766554"],
        "sgpa_sem1": [6.8, 8.2, 5.0, 7.4],
        "sgpa_sem2": [7.1, 8.5, 5.5, 7.8],
        "sgpa_sem3": [6.5, 8.0, 4.8, 7.2],
        "attendance_count": [220, 270, 180, 285],
        "total_days": [300, 300, 300, 300]
    }
    return pd.DataFrame(data)

# -------- Logic --------
def analyze_student(row):
    sgpas = [row["sgpa_sem1"], row["sgpa_sem2"], row["sgpa_sem3"]]
    cgpa = sum(sgpas) / len(sgpas)
    attendance_percent = (row["attendance_count"] / row["total_days"]) * 100
    alerts = []
    if cgpa < 6.0:
        alerts.append("Low CGPA")
    if attendance_percent < 75:
        alerts.append("Low Attendance")
    summary = f"{row['name']} has a CGPA of {cgpa:.2f}. Attendance is {attendance_percent:.1f}%. Alerts: {', '.join(alerts) if alerts else 'None.'}"
    parent_msg = f"Hello {row['parent_name']}, this is an update about {row['name']}. CGPA: {cgpa:.2f}, Attendance: {attendance_percent:.1f}%. Concerns: {', '.join(alerts) if alerts else 'All good!'}"
    return cgpa, attendance_percent, alerts, summary, parent_msg

# -------- UI --------
st.title("🎓 AI Mentor - University Dashboard")
st.write("Prototype that automates mentor tasks: progress tracking, attendance, parent communication, and career guidance.")

# Sidebar
uploaded_file = st.sidebar.file_uploader("Upload Students CSV", type=["csv"])
if st.sidebar.button("Load Demo Data"):
    df = create_sample_df()
else:
    df = None
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

# Tabs for features
tabs = st.tabs(["📊 Dashboard", "📘 Student Reports", "📝 Teacher Feedback", "📷 QR Attendance", "🔮 Career Prediction", "🧩 Personality Quiz"])

# --- Dashboard Tab ---
with tabs[0]:
    if df is not None:
        reports = []
        for _, row in df.iterrows():
            cgpa, att, alerts, summary, msg = analyze_student(row)
            reports.append({
                "name": row["name"],
                "cgpa": cgpa,
                "attendance": att,
                "alerts": ", ".join(alerts) if alerts else "None",
                "summary": summary,
                "parent_msg": msg
            })
        report_df = pd.DataFrame(reports)

        st.subheader("📊 Class Summary")
        st.write(f"**Average CGPA:** {report_df['cgpa'].mean():.2f}")
        st.write(f"**Average Attendance:** {report_df['attendance'].mean():.1f}%")
        st.write(f"**Flagged Students:** {(report_df['alerts'] != 'None').sum()}")

        st.bar_chart(report_df.set_index("name")[["cgpa", "attendance"]])
    else:
        st.info("Upload a CSV or click 'Load Demo Data' to view the dashboard.")

# --- Student Reports Tab ---
with tabs[1]:
    if df is not None:
        st.subheader("👩‍🎓 Student Reports")
        for _, row in report_df.iterrows():
            st.markdown(f"### {row['name']}")
            st.write("📘 **Progress Summary:**", row["summary"])
            st.write("📩 **Parent Message:**", row["parent_msg"])
            st.markdown("---")
    else:
        st.info("No data available yet.")

# --- Teacher Feedback Tab ---
with tabs[2]:
    st.subheader("📝 Teacher Feedback (Prototype)")
    st.write("Here, teachers can correct/edit AI reports. In the future, AI will learn from this feedback.")
    feedback = st.text_area("Write feedback about a student report:")
    if st.button("Submit Feedback"):
        st.success("Feedback saved (demo only).")

# --- QR Attendance Tab ---
with tabs[3]:
    st.subheader("📷 QR Attendance (Prototype)")
    st.write("Students will scan a unique QR code to mark attendance (prevents proxy).")
    qr = qrcode.make("Attendance QR - Valid for 5 min")
    buf = BytesIO()
    qr.save(buf)
    st.image(buf.getvalue(), caption="Scan to mark attendance (demo QR)")

# --- Career Prediction Tab ---
with tabs[4]:
    st.subheader("🔮 Career Prediction (Prototype)")
    st.write("This AI will predict where the student will be after 4 years based on academic & extracurricular progress.")
    st.info("Example: 'Neha Sharma is likely to pursue a Masters in Data Science based on her CGPA and extracurriculars.'")

# --- Personality Quiz Tab ---
with tabs[5]:
    st.subheader("🧩 Personality Quiz (Prototype)")
    st.write("Students answer a short quiz → AI suggests suitable career fields.")
    q1 = st.radio("Do you prefer working with data or people?", ["Data", "People"])
    q2 = st.radio("Would you rather solve problems logically or creatively?", ["Logical", "Creative"])
    if st.button("Submit Quiz"):
        if q1 == "Data" and q2 == "Logical":
            st.success("Suggested Field: Data Analyst / Software Engineer")
        elif q1 == "People" and q2 == "Creative":
            st.success("Suggested Field: Marketing / Management")
        else:
            st.success("Suggested Field: Research / Product Design")
