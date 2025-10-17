# Import necessary libraries
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro 1.5 model
model = genai.GenerativeModel('gemini-2.5-flash')


def get_gemini_response(input_text, pdf_content=None, image=None):
    """Get response from Gemini model based on input type"""
    if image:
        response = model.generate_content([input_text, image])
    elif pdf_content:
        combined_input = f"{input_text}\n\nReference Document Content:\n{pdf_content}"
        response = model.generate_content(combined_input)
    else:
        response = model.generate_content(input_text)
    return response.text


def input_image_setup(uploaded_file):
    """Process uploaded image file"""
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    else:
        raise FileNotFoundError("No file uploaded")


def read_pdf_content(uploaded_file):
    """Extract text from PDF file"""
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text


# Custom prompt for chemical research
CHEM_PROMPT = """
You are an expert AI Chemist assistant. Analyze the input and provide detailed chemical solutions considering:

For Experimental Design:
1. Suggest optimal reaction conditions (temperature, pressure, catalysts)
2. Recommend safety precautions
3. Provide alternative synthesis routes

For Material Analysis:
1. Identify key chemical properties
2. Suggest characterization techniques
3. Predict material behavior under different conditions

For Drug Discovery:
1. Analyze target interactions
2. Suggest potential analogs
3. Predict ADMET properties

Format output with clear sections using Markdown. Highlight critical values in **bold**.
"""

# Streamlit App Configuration
st.set_page_config(page_title="AI Chemist", page_icon="⚗️", layout="wide")

# Custom CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f9f9f9;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ecc71;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        font-size: 1.2rem;
        padding: 10px;
        background-color: #e74c3c;
        color: white;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown('<div class="title">⚗️ AI Chemist - Research Assistant By Rashid Patel</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Empowering Chemical Science with AI</div>', unsafe_allow_html=True)
st.markdown("---")

# Input Section
col1, col2 = st.columns([1, 2])

with col1:
    st.image("AIC.png", width=200)

with col2:
    input_type = st.radio("Select Input Type:", ["Text", "Image", "PDF"], horizontal=True)

user_input = ""
pdf_content = ""
image = None

if input_type == "Text":
    user_input = st.text_area("📝 Describe your chemical research problem:", height=150)
elif input_type == "Image":
    uploaded_image = st.file_uploader("📷 Upload a chemical structure/image:", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = input_image_setup(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
elif input_type == "PDF":
    uploaded_pdf = st.file_uploader("📄 Upload research document (PDF):", type="pdf")
    if uploaded_pdf:
        pdf_content = read_pdf_content(uploaded_pdf)
        st.success("✅ PDF content extracted successfully!")

# Additional Parameters
with st.expander("⚙️ Advanced Settings"):
    temp = st.slider("Model Creativity (Temperature):", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Response Length (Tokens):", 100, 2000, 500)

# Process Input
if st.button("🔬 Generate Solution", use_container_width=True):
    with st.spinner("🧪 Analyzing chemical problem..."):
        try:
            full_prompt = f"{CHEM_PROMPT}\n\nUser Input: {user_input}"

            if input_type == "Image":
                response = get_gemini_response(full_prompt, image=image)
            elif input_type == "PDF":
                response = get_gemini_response(full_prompt, pdf_content=pdf_content)
            else:
                response = get_gemini_response(full_prompt)

            st.snow()  # ❄️ Cool snow effect for result display
            st.markdown("<h2 style='color: #e74c3c;'>🧪 AI Chemist's Solution</h2>", unsafe_allow_html=True)
            st.markdown(response)

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Sidebar Information
with st.sidebar:
    st.markdown("<h2 style='color: #3498db;'>🔬 Research Parameters</h2>", unsafe_allow_html=True)
    st.info("""
    ✅ Supported Input Types:
    - Chemical equations
    - Spectral data
    - Material properties
    - Reaction parameters
    - Research abstracts
    """)

    st.markdown("<h2 style='color: #e67e22;'>⚠️ Safety Protocols</h2>", unsafe_allow_html=True)
    st.warning("""
    1. Always verify AI suggestions
    2. Use proper PPE
    3. Double-check chemical compatibility
    4. Follow institutional safety guidelines
    """)

    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>🚀 Powered by Google Gemini AI</h3>", unsafe_allow_html=True)

