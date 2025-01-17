import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

# Load environment variables
load_dotenv()

# Load and process the document
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "canada.txt")
loader = TextLoader(file_path)
document = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
docs = text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(docs, embeddings)

retriever = vector_store.as_retriever(search_type="similarity", search_k=3)

## Defining tools with Chain of Thought reasoning

from langchain.tools import Tool

# Weather Tool with CoT reasoning
def get_weather(location: str):
    reasoning_prompt = f"""
    Think step by step to answer the following query:
    What is the current weather in {location}?
    First, check the current weather data for {location}. Then, provide a detailed description of the weather.
    """
    
    result = "The current weather in {location} is sunny at 25° Celsius."  # hardcoded
    return f"{reasoning_prompt}\nResult: {result}"

weather_tool = Tool(
    name="Weather Tool",
    func=get_weather,
    description="Provides weather details of the given location with Chain of Thought reasoning."
)

# document retrieval tool with CoT reasoning
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

retrieval_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

def document_retrieval_with_reasoning(query: str):
    reasoning_prompt = f"""
    Think step by step to answer the following query:
    {query}
    First, break down the key concepts in the query and identify relevant information. 
    Then, search through the document database to find the most relevant information. 
    Finally, summarize the most relevant results clearly.
    """
    
    try:
        result = retrieval_qa_chain.run({"query": query})
        return f"{reasoning_prompt}\nResult: {result}"
    except Exception as e:
        return f"An error occurred: {e}"

document_tool = Tool(
    name="Document Retrieval Tool",
    func=document_retrieval_with_reasoning,
    description="Retrieve knowledge from the document database with Chain of Thought reasoning."
)

## Initializing the Agent with CoT reasoning

from langchain.agents import AgentType, initialize_agent

tools = [document_tool, weather_tool]

# Initializing the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Building agentic chatbot with CoT reasoning
def chatbot_agentic_rag():
    print("Agentic RAG chatbot with Chain of Thought is running! Type 'exit' to quit.")

    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Chatbot session ended.")
            break
        try:
            # Display reasoning steps for user queries
            print("Bot: Let me think about that...")
            response = agent.run(user_query)
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Error: {e}")

# Run the chatbot
if __name__ == "__main__":
    chatbot_agentic_rag()
