import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Mentor", layout="wide")

st.title("🎓 AI Mentor Agent")
st.write("Automating mentor tasks: Attendance, Progress Reports, Parent Communication, and FAQs.")

# --- Load CSV Helper ---
def load_csv(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📋 Attendance", "📈 Progress Reports", "📨 Parent Communication", "❓ Ask Mentor"])

# ---------------- Attendance Tab ----------------
with tab1:
    st.header("Attendance Overview")
    att_file = st.file_uploader("Upload Attendance CSV", type="csv", key="att")
    att_df = load_csv(att_file)

    if att_df is not None:
        att_df["Attendance%"] = round((att_df["Attended"] / att_df["Total_Classes"]) * 100, 2)
        att_df["Status"] = att_df["Attendance%"].apply(lambda x: "At Risk ❌" if x < 75 else "Good ✅")
        st.dataframe(att_df)

        st.subheader("At Risk Students (<75%)")
        st.write(att_df[att_df["Attendance%"] < 75][["Name", "Attendance%"]])

# ---------------- Progress Reports Tab ----------------
with tab2:
    st.header("Progress Across Semesters")
    gpa_file = st.file_uploader("Upload GPA CSV", type="csv", key="gpa")
    gpa_df = load_csv(gpa_file)

    if gpa_df is not None:
        st.dataframe(gpa_df)

        student = st.selectbox("Select a student", gpa_df["Name"])
        row = gpa_df[gpa_df["Name"] == student].iloc[0]

        sems = [col for col in gpa_df.columns if col.startswith("Sem")]
        scores = [row[col] for col in sems]

        fig, ax = plt.subplots()
        ax.plot(sems, scores, marker="o")
        ax.set_title(f"GPA Trend: {student}")
        ax.set_ylabel("GPA")
        st.pyplot(fig)

        trend = "Improving 📈" if scores[-1] > scores[-2] else "Declining 📉"
        st.write(f"Performance Trend: **{trend}**")

# ---------------- Parent Communication Tab ----------------
with tab3:
    st.header("Auto-Generate Parent Messages")
    if 'att_df' in locals() and att_df is not None and 'gpa_df' in locals() and gpa_df is not None:
        student = st.selectbox("Select student for parent message", att_df["Name"], key="msg")
        att_row = att_df[att_df["Name"] == student].iloc[0]
        gpa_row = gpa_df[gpa_df["Name"] == student].iloc[0]

        attendance = att_row["Attendance%"]
        sems = [col for col in gpa_df.columns if col.startswith("Sem")]
        prev, now = gpa_row[sems[-2]], gpa_row[sems[-1]]

        if attendance < 75 and now < prev:
            msg = f"Dear Parent of {student},\n\nYour ward’s attendance is {attendance}% and GPA has declined from {prev} to {now}. Please meet the mentor to discuss steps.\n\nRegards,\nAI Mentor"
        elif attendance < 75:
            msg = f"Dear Parent of {student},\n\nThis is to inform you that attendance is {attendance}%, below the 75% requirement. Kindly ensure regular attendance.\n\nRegards,\nAI Mentor"
        elif now < prev:
            msg = f"Dear Parent of {student},\n\nWe have observed GPA declined from {prev} to {now}. Please support your ward’s academics.\n\nRegards,\nAI Mentor"
        else:
            msg = f"Dear Parent of {student},\n\nYour ward is performing well with {attendance}% attendance and stable GPA.\n\nRegards,\nAI Mentor"

        st.text_area("Generated Message", msg, height=200)

# ---------------- Ask Mentor Tab ----------------
with tab4:
    st.header("Ask Mentor (FAQs)")
    faq_file = st.file_uploader("Upload FAQ CSV", type="csv", key="faq")
    faq_df = load_csv(faq_file)

    if faq_df is not None:
        question = st.text_input("Ask a question:")
        if st.button("Get Answer"):
            found = None
            for i, row in faq_df.iterrows():
                if row["question"].lower() in question.lower():
                    found = row["answer"]
                    break
            if found:
                st.success(found)
            else:
                st.warning("Sorry, I don’t know the answer. Ask your mentor.")
