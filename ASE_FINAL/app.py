import streamlit as st
import os
import tempfile
from main4 import run_split
from new_handwritten_ocr import run_ocr
from grade_extracted_text import grade_extracted_text_whole
from pdf2image import convert_from_path

# ---------------- User Registration System ----------------
def register():
    st.title("📚 Automated Answer Sheet Grader - Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if username and password and confirm_password:
            if password == confirm_password:
                # Save the new user's credentials (for simplicity, we'll just save them in the session here)
                # You can extend this to save in a database or a file.
                st.session_state.users[username] = password
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Passwords do not match.")
        else:
            st.warning("Please fill in all fields.")

# ---------------- Login System ----------------
def login():
    st.title("📚 Automated Answer Sheet Grader - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

# ---------------- Grading Certificate ----------------
def display_certificate(result):
    st.subheader("📜 Grade Certificate")
    st.markdown("**📘 Subject:** Advanced Machine Learning")
    st.markdown("**🎓 Credits:** 4")
    st.markdown(f"**✅ Score:** {result['score']} / {result['max_marks']}")
    st.markdown(f"**📊 Grade:** {get_grade(result['score'], result['max_marks'])}")
    st.markdown(f"**📝 Matched Keywords:** {', '.join(result['matched_keywords'])}")

def get_grade(score, max_marks):
    percent = (score / max_marks) * 100
    if percent < 40:
        return "Fail"
    elif percent < 60:
        return "Pass"
    elif percent < 80:
        return "Good"
    else:
        return "Outstanding"

# ---------------- Upload & Processing ----------------
def upload_files():
    st.title("📤 Upload Answer Sheet & Schema")

    answer_sheet = st.file_uploader("Upload Answer Sheet (PDF/Image)", type=["pdf", "png", "jpeg"])
    schema_file = st.file_uploader("Upload Answer Schema (Text File)", type=["txt"])
    max_marks = st.number_input("Enter Maximum Marks", min_value=1, max_value=100, value=10)

    if st.button("🧠 Grade Answer Sheet"):
        if not answer_sheet or not schema_file:
            st.warning("Please upload both the answer sheet and the schema file.")
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            # Save uploaded files
            answer_path = os.path.join(tmpdir, answer_sheet.name)
            schema_path = os.path.join(tmpdir, "answer_schema.txt")

            with open(answer_path, "wb") as f:
                f.write(answer_sheet.read())
            with open(schema_path, "wb") as f:
                f.write(schema_file.read())

            # Convert PDF to image if needed
            if answer_path.lower().endswith(".pdf"):
                st.info("📄 Converting PDF to image...")
                images = convert_from_path(answer_path)
                image_path = os.path.join(tmpdir, "converted_page.jpg")
                images[0].save(image_path, "JPEG")
            else:
                image_path = answer_path

            # Split image into segments
            st.info("✂️ Splitting image by lines...")
            #results_folder = os.path.join(tmpdir, "results")
            results_folder = "C:/Users/harsh/Desktop/ASE_FINAL/results"
            run_split(image_path, results_folder)

            # Run OCR
            st.info("🔍 Running Handwritten Text Recognition...")
            #extracted_file = os.path.join(tmpdir, "extracted_texts.txt")
            extracted_file = "C:/Users/harsh/Desktop/ASE_FINAL/extracted_texts.txt"
            run_ocr(results_folder, extracted_file)

            # Grade the extracted text
            st.info("🧮 Grading...")
            result = grade_extracted_text_whole(
                extracted_file=extracted_file,
                schema_file=schema_path,
                max_marks=max_marks
            )

            st.success("✅ Grading Completed!")
            display_certificate(result)

# ---------------- Streamlit App Logic ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize the users dictionary if not present
if "users" not in st.session_state:
    st.session_state.users = {}

# Display login or registration based on the logged-in state
if not st.session_state.logged_in:
    choice = st.radio("Choose an option", ("Login", "Register"))
    
    if choice == "Login":
        login()
    else:
        register()
else:
    upload_files()
