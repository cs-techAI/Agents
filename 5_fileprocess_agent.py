from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from creds import openai_api, serp_api


serpapi_api_key = serp_api  


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api)


tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=serpapi_api_key)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

query = "What is the capital of France?"
response = agent.invoke(query)

print("Agent's Response:", response)
