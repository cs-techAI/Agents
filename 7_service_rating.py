import os
import pandas as pd
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.chat_models import ChatOpenAI


llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

# tool for calculating ratings 
def rating_tool(data):
    prompt = f"""
    The following is a dataset of services, providers, thumbs_up, and thumbs_down:
    {data.to_string(index=False)}

    For each provider, calculate the ratings as follows:
    rating = (thumbs_up / (thumbs_up + thumbs_down)) * 5.

    Return the results as a structured table with columns: 
    services, provider_name, thumbs_up, thumbs_down, rating.
    """
    
    response = llm(prompt)
    
    # here we convert the model's output to a pandas dataframe
    try:
        lines = response.splitlines()
        table_data = [line.split(",") for line in lines if "," in line]
        
        processed_data = pd.DataFrame(table_data[1:], columns=["services", "provider_name", "thumbs_up", "thumbs_down", "rating"])
        
        # converting numeric columns as int and float
        processed_data["thumbs_up"] = processed_data["thumbs_up"].astype(int)
        processed_data["thumbs_down"] = processed_data["thumbs_down"].astype(int)
        processed_data["rating"] = processed_data["rating"].astype(float)

        return processed_data
    
    except Exception as e:
        st.error(f"Error processing the model output: {e}")
        return None

# tool for finding top providers
def top_provider_tool(processed_data):


    prompt = f"""
    The following is a dataset of service providers with their ratings:
    {processed_data.to_string(index=False)}

    Identify the top provider for each service category based on the highest rating.
    
    Return the results as a structured table with columns: 
    services, provider_name, rating.
    """
    
    response = llm(prompt)
    
    # converting the model output to a pandas dataframe
    try:
        lines = response.splitlines()
        table_data = [line.split(",") for line in lines if "," in line]
        
        top_providers_data = pd.DataFrame(table_data[1:], columns=["services", "provider_name", "rating"])
        
        # convert numeric columns back 
        top_providers_data["rating"] = top_providers_data["rating"].astype(float)

        return top_providers_data
    

    except Exception as e:
        st.error(f"Error processing the model output: {e}")
        return None

# LangChain tools for both tasks
rating_processing_tool = Tool(
    name="Rating Calculation Tool",
    func=rating_tool,
    description="Calculates ratings for service providers based on thumbs up/down votes."
)

top_provider_processing_tool = Tool(
    name="Top Provider Tool",
    func=top_provider_tool,
    description="Finds the top provider in each service category based on ratings."
)

# agent with two tools
combined_agent = initialize_agent(
    tools=[rating_processing_tool, top_provider_processing_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Streamlit
st.title("Service Ranking Using LangChain Agents with OpenAI")
st.write(
    "Upload a CSV file with columns: services, provider_name, thumbs_up, thumbs_down. "
)


uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(data)

    # checks the req. columns
    required_columns = {'services', 'provider_name', 'thumbs_up', 'thumbs_down'}
    if not required_columns.issubset(data.columns):
        st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}")
    else:
        # run agent when clicks button
        if st.button("Process Data"):
            rated_data = combined_agent.run(data)
            
            if rated_data is not None:
                st.write("Processed Data with Ratings:")
                st.dataframe(rated_data)

                # finds top Pproviders after ratings are calculated using rated data
                top_providers = combined_agent.run(rated_data)
                
                if top_providers is not None:
                    st.write("Top Providers by Service Category:")
                    st.dataframe(top_providers)
