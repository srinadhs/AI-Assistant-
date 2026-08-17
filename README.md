# Storm AI

**Storm AI** is a conversational AI assistant built with Streamlit and LangChain, powered by Google Gemini. It provides a sleek chat interface for asking questions, discussing documents, and getting intelligent responses in real-time.

---

## Features

- **Conversational AI Chat**: Clean, intuitive chat interface powered by Google Gemini (`gemini-2.5-flash`)
- **Document Upload**: Attach PDF, TXT, or MD files to ask questions about their content
- **Chat History**: Maintains conversation context throughout the session
- **Responsive UI**: Built with Streamlit for a modern, cross-platform experience
- **Async-Ready**: Proper event loop handling for smooth Streamlit integration

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend / UI | Streamlit |
| LLM Framework | LangChain |
| Language Model | Google Gemini (`gemini-2.5-flash`) |
| PDF Processing | PyMuPDF (`fitz`) |
| Configuration | Python `dotenv` |
| Language | Python 3.12+ |

---

## Project Structure

```
AI Assistant/
├── app.py                 # Main Streamlit application entry point
├── core/
│   ├── __init__.py        # Package initializer
│   └── engine.py          # ChatEngine: LLM orchestration & file extraction
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Google Cloud project with the [Generative Language API](https://ai.google.dev/) enabled
- A Google API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/storm-ai.git
   cd storm-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

   - **Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and paste your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Usage

1. **Start chatting** — Type a message in the chat input and press Enter.
2. **Attach documents** — Use the sidebar to upload PDF, TXT, or MD files. The assistant will read and reference the content when answering.
3. **Clear conversation** — Click "Clear Conversation" in the sidebar to reset the chat history.

---

## Configuration

You can customize the assistant behavior in `core/engine.py`:

- **Model**: Change `model_name` in `ChatEngine.__init__()` (e.g., `"gemini-1.5-pro"`)
- **Temperature**: Adjust `temperature` (0.0 = deterministic, 1.0 = creative)
- **System Prompt**: Modify `self.system_prompt` to change the assistant's persona or instructions

