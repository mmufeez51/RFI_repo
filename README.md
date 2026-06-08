# AI-Powered RFI Assistant 🏗️

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rfirepo-lnu2bnhvebta9whgrgiohc.streamlit.app/)

A Streamlit web application that leverages Google's Gemini AI to automatically generate formal Requests for Information (RFIs) for construction projects. By simply uploading a site photo and providing some notes, the assistant analyzes the context and produces a structured, professional RFI document ready to be sent to architects or engineers.

## Features

- **Image Analysis**: Upload construction site photos for AI-powered context analysis.
- **Automated RFI Generation**: Generates a formal RFI with subject line, background, specific questions, potential impacts, and suggested solutions.
- **Export to Word**: Download the generated RFI directly as a formatted Microsoft Word document (`.docx`).
- **Streamlit Interface**: Clean, easy-to-use web interface for quick data entry and review.

## Prerequisites

- Python 3.8+
- A Google Gemini API Key

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd RFI_repo
   ```

2. **Install the dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API Key:**
   You can set the Gemini API key as an environment variable or use Streamlit secrets.
   
   *Option A: Environment Variable*
   ```bash
   # On Windows (Command Prompt)
   set GEMINI_API_KEY=your_api_key_here
   
   # On Windows (PowerShell)
   $env:GEMINI_API_KEY="your_api_key_here"
   
   # On macOS/Linux
   export GEMINI_API_KEY="your_api_key_here"
   ```

   *Option B: Streamlit Secrets*
   Create a `.streamlit/secrets.toml` file in the project root:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. **Generate an RFI:**
   - Upload a construction photo (JPG, JPEG, PNG).
   - Enter your site notes, observations, or specific queries in the text area.
   - Click "Generate RFI" to let the AI process the information.
   - Review the generated draft on the screen.
   - Click the download button to save the RFI as a `.docx` file.

## Technologies Used

- [Streamlit](https://streamlit.io/) - The web framework used
- [Google Generative AI (Gemini)](https://ai.google.dev/) - For image and text analysis
- [python-docx](https://python-docx.readthedocs.io/) - For generating Word documents
- [Pillow](https://python-pillow.org/) - For image processing
