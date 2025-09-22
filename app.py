import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import docx2txt
import PyPDF2

st.header("📄 Resume Parser")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
if resume_file:
    if resume_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(resume_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    else:
        text = docx2txt.process(resume_file)

    st.subheader("Extracted Text")
    st.write(text[:1000])  # Show first 1000 characters

    # Simple keyword extraction
    keywords = ["Python", "Excel", "Leadership", "Recruitment", "Analytics"]
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    st.success(f"Skills detected: {', '.join(found)}")


st.set_page_config(page_title="Talent Management AI Demo", layout="wide")

st.title("🤖 Talent Management Dashboard")
st.markdown("Simulated AI-powered HR tool for screening, performance, and development")

# --- Candidate Screening ---
st.header("📋 Candidate Screening")

uploaded_file = st.file_uploader("Upload candidate data (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Raw Data", df)

    # Simulate AI scoring
    scaler = MinMaxScaler()
    df["AI_Score"] = scaler.fit_transform(df.select_dtypes(include=np.number)).mean(axis=1) * 100
    df_sorted = df.sort_values("AI_Score", ascending=False)

    st.write("🔍 Top Candidates by AI Score")
    st.dataframe(df_sorted[["Name", "AI_Score"]])

# --- Performance Dashboard ---
st.header("📊 Performance Dashboard")

performance_data = pd.DataFrame({
    "Employee": ["Amit", "Sara", "John", "Priya", "Ali"],
    "Performance": [88, 76, 92, 69, 85],
    "Potential": [90, 80, 95, 70, 88]
})

fig, ax = plt.subplots()
ax.scatter(performance_data["Performance"], performance_data["Potential"], color='blue')
for i, txt in enumerate(performance_data["Employee"]):
    ax.annotate(txt, (performance_data["Performance"][i], performance_data["Potential"][i]))
ax.set_xlabel("Performance")
ax.set_ylabel("Potential")
ax.set_title("9-Box Grid Simulation")
st.pyplot(fig)

# --- Learning Recommendations ---
st.header("📚 AI Learning Recommendations")

skills = st.multiselect("Select skill gaps", ["Leadership", "Python", "Communication", "Data Analysis", "Project Management"])
if skills:
    st.write("Recommended Courses:")
    for skill in skills:
        st.markdown(f"- [Learn {skill} on Coursera](https://www.coursera.org/search?query={skill})")

# --- Succession Planning ---
st.header("🧬 Succession Planning")

role = st.selectbox("Select a key role", ["Team Lead", "HR Manager", "Data Analyst"])
if role:
    st.write(f"Suggested successors for {role}:")
    st.write(performance_data.sort_values("Potential", ascending=False).head(3)[["Employee", "Potential"]])

st.markdown("---")
st.caption("Demo app for educational purposes. Created with ❤️ using Streamlit.")

# --- Authentication ---
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "hradmin" and password == "demo123":
            st.session_state["logged_in"] = True
        else:
            st.sidebar.error("Invalid credentials")

if "logged_in" not in st.session_state:
    login()
    st.stop()


# --- HR Chatbot ---
st.header("💬 HR Chatbot Assistant")

query = st.text_input("Ask me anything about HR policies, leave, or training:")
if query:
    if "leave" in query.lower():
        st.success("You are entitled to 24 paid leaves annually. Apply via the HR portal.")
    elif "training" in query.lower():
        st.success("Recommended training: Leadership 101, Python for HR, and Emotional Intelligence.")
    elif "policy" in query.lower():
        st.success("Company policies are available in the HR handbook. Let me know what you need.")
    else:
        st.info("I'm still learning! Please ask about leave, training, or policies.")
