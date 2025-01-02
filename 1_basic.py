from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from creds import openai_api, serp_api

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key= openai_api )

tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key = serp_api)
agent_executor = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose= True
)

agent_executor.invoke("Which place is known as rice bowl of Tamilnadu?")