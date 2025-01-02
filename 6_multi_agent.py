from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from creds import openai_api,serp_api

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key= openai_api)

tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key=serp_api)

agent1 = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent2 = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Agent 1
query1 = "What is the capital of Japan?"
response1 = agent1.invoke(query1)
print("Agent 1's Response (Search):", response1)

# Agent 2
query2 = "What is the square root of 256?"
response2 = agent2.invoke(query2)
print("Agent 2's Response (Math):", response2)
