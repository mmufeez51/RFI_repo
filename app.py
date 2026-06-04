import streamlit as st
import google.generativeai as genai
from docx import Document
import io
import os
from PIL import Image

# Configure page
st.set_page_config(page_title="AI RFI Assistant", page_icon="🏗️")

# Set up the API key for Google Gemini
# Prioritize Streamlit secrets, fallback to environment variable
API_KEY = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not API_KEY:
    API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.warning("⚠️ Please set your GEMINI_API_KEY as an environment variable or in Streamlit secrets (.streamlit/secrets.toml) to use the AI features.")

st.title("🏗️ AI-Powered RFI Assistant")
st.write("Upload a construction photo and provide some site notes. The AI will generate a formal Request for Information (RFI) document.")

# File uploader for the photo
uploaded_file = st.file_uploader("Upload Construction Photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Construction Photo", use_column_width=True)

# Text area for site notes
site_notes = st.text_area("Site Notes", placeholder="Enter your observations, measurements, or specific queries here...", height=150)

def create_docx(text):
    doc = Document()
    doc.add_heading('Request for Information (RFI)', 0)
    
    # Simple parsing to preserve some formatting
    paragraphs = text.split('\n')
    for para in paragraphs:
        if para.strip() != "":
            # Handle basic bolding and headers for cleaner word doc output
            if para.startswith('**') and para.endswith('**'):
                p = doc.add_paragraph()
                p.add_run(para.replace('**', '')).bold = True
            elif para.startswith('#'):
                doc.add_heading(para.replace('#', '').strip(), level=2)
            else:
                doc.add_paragraph(para)
                
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

if st.button("Generate RFI", type="primary"):
    if not API_KEY:
        st.error("Gemini API Key is missing. Cannot generate RFI. Please set the GEMINI_API_KEY environment variable.")
    elif not uploaded_file and not site_notes:
        st.error("Please upload an image and/or provide site notes to generate an RFI.")
    else:
        with st.spinner("Analyzing image and notes to generate formal RFI..."):
            try:
                # We use the requested 'gemini-3.5-flash' model
                model = genai.GenerativeModel('gemini-3.5-flash')
                
                contents = []
                
                # Instruction prompt
                prompt = """
                You are an expert construction project manager. Based on the provided construction site photo and the site notes, please generate a structured, formal Request for Information (RFI). 
                
                The RFI should be formatted clearly and include the following sections:
                - Subject Line (clear and concise)
                - Background / Context (based on the image and notes provided)
                - The Specific Question or Clarification Needed
                - Potential Impact if not resolved (e.g., schedule delay, cost impact)
                - Suggested Solution (if any can be inferred)
                
                Make the tone professional, objective, and ready to be sent to an architect or engineer. Do not include placeholder brackets like [Insert Date], just provide the core content.
                """
                contents.append(prompt)
                
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    contents.append(image)
                    
                if site_notes:
                    contents.append(f"Site Notes from field personnel:\n{site_notes}")

                # Generate content
                response = model.generate_content(contents)
                
                st.success("RFI Generated Successfully!")
                
                st.markdown("---")
                st.subheader("Generated RFI Draft")
                st.write(response.text)
                st.markdown("---")
                
                # Create docx for download
                docx_buffer = create_docx(response.text)
                
                st.download_button(
                    label="📄 Download RFI as Word Document (.docx)",
                    data=docx_buffer,
                    file_name="Generated_RFI.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
