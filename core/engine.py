import os
import tempfile
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class ChatEngine:
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature
        )
        self.system_prompt = (
            "your name is storm created by sarikondu sreenadh"
            "You are a helpful, intelligent, and accurate AI assistant. "
            "Respond clearly and concisely to user queries."
        )

    def extract_file_content(self, uploaded_files) -> str:
        """Extracts raw text from uploaded PDF or TXT files on the fly without indexing."""
        extracted_text = ""
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in [".pdf", ".txt", ".md"]:
                continue

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                temp_file.write(file.getvalue())
                temp_path = temp_file.name

            try:
                # Upgraded to PyMuPDFLoader for better PDF extraction
                if file_extension == ".pdf":
                    loader = PyMuPDFLoader(temp_path)
                else:
                    loader = TextLoader(temp_path)
                
                docs = loader.load()
                file_text = "\n".join([doc.page_content for doc in docs if doc.page_content.strip()])
                if file_text:
                    extracted_text += f"\n\n--- Content from {file.name} ---\n{file_text}"
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return extracted_text

    def generate_response(self, user_query: str, chat_history: List, file_context: str = "") -> str:
        """Sends chat history and optional direct file text to Gemini."""
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add prior conversation history
        messages.extend(chat_history)
        
        # Prepare the current prompt with attached text if present
        if file_context:
            current_content = f"Reference Context:\n{file_context}\n\nUser Question:\n{user_query}"
        else:
            current_content = user_query
            
        messages.append(HumanMessage(content=current_content))
        
        response = self.llm.invoke(messages)
        return response.content