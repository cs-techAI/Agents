
############# Zero-Shot Agent for Text Summarization #############

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from creds import openai_api

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature= 0.7, api_key= openai_api)
tools = load_tools(["llm-summarize"], llm = llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

text = """Machine learning is a field of artificial intelligence (AI) that uses statistical techniques
to give computers the ability to learn from data without being explicitly programmed.
It is considered a part of AI, with the goal of developing algorithms that can help the machine
make decisions and predictions.
"""

result = agent.invoke("Summarize the following text: ", text)
print("The Result : ", result)