import streamlit as st
from typing import Optional
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.assistant import Assistant
import os
from dotenv import load_dotenv
import time

load_dotenv()

def format_console_output(message: str, response: str, response_time: float) -> str:
    # Colors for syntax highlighting
    YELLOW = "#FFFF00"
    GREEN = "#00FF00"
    CYAN = "#00FFFF"
    WHITE = "#FFFFFF"
    
    html = f"""
    <div style="background-color: #1E1E1E; color: {WHITE}; font-family: 'Courier New', monospace; padding: 10px;">
        <div style="border: 1px solid #444; margin-bottom: 10px;">
            <div style="padding: 5px; border-bottom: 1px solid #444;">
                <span style="color: {WHITE}">Message</span>
                <span style="color: {WHITE}; margin-left: 10px;">{message}</span>
            </div>
            <div style="padding: 5px;">
                <span style="color: {WHITE}">Response</span>
                <span style="color: #888;">({response_time:.1f}s)</span><br>
                <span style="color: {GREEN}">• Running: search_knowledge_base(query={message})</span><br><br>
    """
    
    lines = response.split('\n')
    count = 1
    for line in lines:
        if line.strip():
            if ':' in line:
                title, content = line.split(':', 1)
                html += f'<span style="color: {YELLOW}">{count}</span> '
                html += f'<span style="color: {CYAN}">{title}:</span>'
                html += f'<span style="color: {WHITE}">{content}</span><br>'
                count += 1
            elif line.strip().startswith('•'):
                html += f'&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: {GREEN}">•</span> '
                html += f'<span style="color: {WHITE}">{line.strip()[1:]}</span><br>'
            else:
                html += f'<span style="color: {WHITE}">{line}</span><br>'
    
    html += "</div></div></div>"
    return html

def init_assistant(pdf_url):
    db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
    knowledge_base = PDFUrlKnowledgeBase(
        urls=[pdf_url],
        vector_db=PgVector2(collection="pdf_content", db_url=db_url),
    )
    knowledge_base.load()
    
    return Assistant(
        knowledge_base=knowledge_base,
        search_knowledge=True
    )

def main():
    st.set_page_config(
        page_title="Thai Recipe Master", 
        page_icon="🍜",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #2D2D2D;
            color: white;
        }
        .stSidebar {
            background-color: #1E1E1E;
        }
        .stSidebar .stTextInput > div > div > input {
            background-color: #2D2D2D;
            color: white;
            border: 1px solid #444;
        }
        .stButton > button {
            background-color: #2D2D2D;
            color: white;
            border: 1px solid #444;
        }
        .stButton > button:hover {
            background-color: #3D3D3D;
            color: white;
            border: 1px solid #555;
        }
        .main-title {
            font-size: 3.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-family: 'Arial', sans-serif;
        }
        .subtitle {
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 3rem;
            color: #888;
            font-family: 'Arial', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main title in the center
    st.markdown('<h1 class="main-title">🍜 Thai Recipe Master</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-Powered Guide to Thai Cuisine</p>', unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### Configuration")
        pdf_url = st.text_input(
            "Enter PDF URL:",
            value="https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
            key="pdf_url"
        )
        load_pdf = st.button("Load PDF", use_container_width=True)
    
    # Main content area
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "assistant" not in st.session_state or load_pdf:
        with st.spinner("Loading Thai Recipe Knowledge..."):
            st.session_state.assistant = init_assistant(pdf_url)
            st.session_state.messages = []
            st.success("Recipe knowledge base loaded successfully!")
    
    # Display chat messages
    for msg in st.session_state.messages:
        st.markdown(msg["formatted_content"], unsafe_allow_html=True)
            
    if prompt := st.chat_input("Ask about Thai recipes..."):
        start_time = time.time()
        response = "".join(list(st.session_state.assistant.chat(prompt)))
        response_time = time.time() - start_time
        
        formatted_content = format_console_output(prompt, response, response_time)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "formatted_content": formatted_content
        })
        
        st.markdown(formatted_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()