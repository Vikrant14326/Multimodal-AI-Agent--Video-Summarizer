from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
import os
import openai
from dotenv import load_dotenv
load_dotenv

openai.api_key=os.getenv("OPENAI_API_KEY")




##web serch agent

web_serch_agent=Agent(
    name="Web search Agent",
    roll="searching the web for information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=["Always include the sources"],
    show_tools_calls=True,
    markdown=True,
)

## financial agent
financial_agent=Agent(
    name="Finance AI Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,company_news=True)],
    instructions=["Use table to display the data"],
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent=Agent(
    team=[web_serch_agent,financial_agent],
    instructions=["Always include sources","Use table to display the data"],
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent.print_response("summarize the analyst recommendation and share the latest news for NVDA",stream=True)