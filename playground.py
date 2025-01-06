from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
import phi
import os
import openai
from dotenv import load_dotenv
from phi.playground import Playground, serve_playground_app  # Or the correct name based on inspection


# Load environment variables
load_dotenv()

# Set the PHI API key
phi.api = os.getenv("PHI_API_KEY")

# Web search agent
web_serch_agent = Agent(
    name="Web search Agent",
    roll="searching the web for information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include the sources"],
    show_tools_calls=True,
    markdown=True,
)

# Financial agent
financial_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["Use table to display the data"],
    show_tools_calls=True,
    markdown=True,
)

# Create the playground app
app = Playground(agents=[web_serch_agent, financial_agent]).get_app()

# Serve the playground app
if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
