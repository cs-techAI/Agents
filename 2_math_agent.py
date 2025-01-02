
########### Zero-Shot React Agent for Math Problem Solving ##############

from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from creds import openai_api

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api)   # initializing llm

tools = load_tools(["llm-math"], llm = llm)          # here we use pre-built tool in langchain for math cal.
agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True)  # initial. agent here

# verbose -> Enables detailed logs, showing how the agent processes input, decides on tools, and generates output.

response = agent.invoke("What is the square root of 144?")
print("Agent response: ",response)