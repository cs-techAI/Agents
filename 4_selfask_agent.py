from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from creds import openai_api, serp_api

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api)

tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key=serp_api)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

response = agent.invoke("What is the best way to learn programming?")
print("Agent response:", response)
