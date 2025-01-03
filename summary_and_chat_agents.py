import streamlit as st
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from PyPDF2 import PdfReader
from docx import Document


st.set_page_config(page_title="Interactive File Agent")
st.title("File Upload & Interactive Agent")


st.sidebar.subheader("API Key Configuration")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if not api_key:
    st.sidebar.error("Please enter your API key to proceed.")


if "file_content" not in st.session_state:
    st.session_state.file_content = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""



uploaded_file = st.file_uploader("Upload a File", type=["txt", "pdf", "docx"])
if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    if file_extension == "txt":
        st.session_state.file_content = uploaded_file.read().decode("utf-8")
    elif file_extension == "pdf":
        pdf_reader = PdfReader(uploaded_file)
        st.session_state.file_content = "".join([page.extract_text() for page in pdf_reader.pages])
    elif file_extension == "docx":
        doc = Document(uploaded_file)
        st.session_state.file_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        st.error("Unsupported file type!")    

### till here used the previous tasks

if st.session_state.file_content:
    st.subheader("Uploaded File Content:")
    st.text_area("File Content:", st.session_state.file_content, height=200)

    # Agent to summarize the file content
    if st.button("Summarize File"):
        with st.spinner("Summarizing the file content..."):
            try:
                def summarize_tool(content):
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)
                    return llm.predict(f"Summarize the following content:\n\n{content}")
                    # predict is the method that triggers the model to perform its task 
                    # (in this case, summarization) based on the prompt given

                summarize_tool_instance = Tool(   #This creates a LangChain Tool called summarize_tool_instance 
                                                    # which we create by us and it gets summarized using openai
                    name="Summarization Tool",
                    func=summarize_tool,
                    description="Summarizes a given text content."
                )

        
                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)
                agent = initialize_agent([summarize_tool_instance], llm, 
                                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)   

                # Use the agent to summarize
                st.session_state.summary = agent.run(f"Summarize this:\n\n{st.session_state.file_content}") # runs the agent
                st.subheader(f"Summary (by Summarization Tool):")
                st.write(st.session_state.summary)
            except Exception as e:
                st.error(f"Error during summarization: {e}")

# Chat Interaction
if st.session_state.summary:     # will be accessed if summary exists
    st.subheader("Chat with Agent")
    chat_input = st.text_input("Ask a question about the file content:")

    if chat_input:
        with st.spinner("Generating response..."):
            try:
                memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
                # buffer memory is a class from LangChain that is used to manage and store 
                # the conversation history between the user and the agent
                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)
                # an agent for chat conversation (conversational agent)
                tools = [
                    Tool(
                        name="File Content Assistant",
                        func=lambda query: "The content is irrelevant to the file" if query.lower() 
                        not in st.session_state.file_content.lower() 
                        else st.session_state.file_content,  # here the user can only chat about the content in uploaded fiile
                        description="Assist the user with questions related to the file content.",
                    )
                ]
                agent = initialize_agent(tools, llm, agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, 
                                         memory=memory, verbose=True)
                response = agent.run(chat_input)    #invokes the chat agent here
                st.session_state.chat_history.append({"user": chat_input, "agent": response})
            except Exception as e:
                st.error(f"Error during chat interaction: {e}")

    

    # Summarize Chat agent
    if st.button("Summarize Chat"):
        with st.spinner("Summarizing the chat conversation..."):
            try:
                # a custom chat summarization tool
                def summarize_chat_tool(chat_context):
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)
                    return llm.predict(f"Summarize this conversation:\n\n{chat_context}")

                summarize_chat_tool_instance = Tool(
                    name="Chat Summarization Tool",
                    func=summarize_chat_tool,
                    description="Summarizes a chat conversation."
                )

                # Prepare chat context
                chat_context = "\n".join([f"User: {chat['user']}\nAgent: {chat['agent']}" 
                                          for chat in st.session_state.chat_history])

                # Use the chat summarization tool again
                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=api_key)
                agent = initialize_agent([summarize_chat_tool_instance], llm, 
                                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
                summary = agent.run(f"Summarize this conversation:\n\n{chat_context}")
                st.subheader("Chat Summary:")
                st.write(summary)

            except Exception as e:
                st.error(f"Error during chat summarization: {e}")





