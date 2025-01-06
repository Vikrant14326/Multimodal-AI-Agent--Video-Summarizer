import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Finance Multi-Agent Chat",
    page_icon="💹",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_agents():
    """Initialize all the agents"""
    web_search_agent = Agent(
        name="Web search Agent",
        role="searching the web for information",
        model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
        tools=[DuckDuckGo()],
        instructions=["Always include the sources"],
        show_tools_calls=True,
        markdown=True,
    )

    financial_agent = Agent(
        name="Finance AI Agent",
        model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
        tools=[YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True
        )],
        instructions=["Use table to display the data"],
        show_tools_calls=True,
        markdown=True,
    )

    return Agent(
        model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
        team=[web_search_agent, financial_agent],
        instructions=["Always include sources", "Use table to display the data"],
        show_tools_calls=True,
        markdown=True,
    )

def get_agent_response(agent, prompt):
    """Get response from agent with proper error handling"""
    try:
        # Use get_response instead of print_response for non-streaming
        response = agent.get_response(prompt)
        
        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)
            
        return response
    except Exception as e:
        return f"Error getting response: {str(e)}"

def main():
    # Header
    st.title("💹 Finance Multi-Agent Chat")
    st.write("Ask questions about stocks, get market analysis, and latest news!")

    # Sidebar
    with st.sidebar:
        st.header("About")
        st.write("""
        This application combines web search and financial analysis capabilities to provide comprehensive market insights.

        Features:
        - Stock Analysis
        - Market News
        - Analyst Recommendations
        - Web Search Integration
        """)

        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # Initialize the multi-agent
    multi_ai_agent = initialize_agents()

    # Chat interface
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask about stocks, market news, or analysis..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = get_agent_response(multi_ai_agent, prompt)
                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()