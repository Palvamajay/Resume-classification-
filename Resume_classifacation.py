import streamlit as st
import pickle
import docx2txt
from PyPDF2 import PdfReader

# Load model
with open("resume_domain_classifier.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Resume Domain Classifier", layout="centered")
st.title("📄 Resume Domain Classifier")
st.write("Upload a resume (PDF, DOCX, or TXT) to predict its professional domain.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

# Text extraction
def extract_text(file):
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.name.endswith('.docx'):
        return docx2txt.process(file)
    elif file.name.endswith('.txt'):
        return str(file.read(), "utf-8")
    else:
        return ""

# Handle uploaded resume
if uploaded_file:
    resume_text = extract_text(uploaded_file)

    if resume_text.strip() == "":
        st.error("No text could be extracted. Please upload a valid file.")
    else:
        st.subheader("📑 Extracted Resume Content")
        st.text_area("Resume Text", resume_text[:2000], height=200)

        if st.button("🔍 Predict Domain"):
            prediction = model.predict([resume_text])[0]
            st.success(f"🎯 **Predicted Domain:** {prediction}") 

st.markdown("---")
st.subheader("⭐ Rate This App")

rating = st.slider('How would you rate your experience?', min_value=1, max_value=5, value=3)

if st.button("Submit Rating"):
    if rating >= 3:
        st.success(f"🎉 Thank you for rating us {rating} out of 5!")
        st.write("We appreciate your feedback!")
        st.balloons()
    else:
        st.warning(f"Thank you for rating us {rating} out of 5.")
        st.write("We will work on improving the app. 😞")
    
