from openai import OpenAI
import json
from creds import OPENAI_API_KEY


llm = OpenAI(api_key=OPENAI_API_KEY)

# the system prompt workflow -- Thought -> Action -> PAUSE -> Action_Response -> Answer
system_prompt = """   
You run in a loop of Thought, Action, PAUSE, Action_Response.  
At the end of the loop, you output an Answer.

Use Thought to understand the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Action_Response will be the result of running those actions.

Your available actions are:

get_response_time:
e.g. get_response_time: learnwithhasan.com
Returns the response time of a website

Example session:

Question: what is the response time for learnwithhasan.com?
Thought: I should check the response time for the web page first.
Action: 

{
  "function_name": "get_response_time",
  "function_parms": {
    "url": "learnwithhasan.com"
  }
}

PAUSE

You will be called again with this:

Action_Response: 0.5

You then output:

Answer: The response time for learnwithhasan.com is 0.5 seconds.
"""



def get_response_time(url):
    if url == "learnwithhasan.com":
        return 0.5
    if url == "google.com":
        return 0.3
    if url == "openai.com":
        return 0.4
    return "Unknown URL"


available_actions = {
    "get_response_time": get_response_time
}


def generate_text_with_conversation(message, model="gpt-3.5-turbo"):
    response = llm.chat.completions.create(
        model=model,
        messages=message
    )
    return response.choices[0].message.content


def extract_json(response):
    return json.loads(response)
    

user_website = input("Enter the website to know the response time of it: ")
user_prompt = f"What is the response time of {user_website}"


message = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]


turn_count = 1
max_turns = 5

while turn_count <= max_turns:
    print(f"Loop: {turn_count}")
    print("----------------------")

    response = generate_text_with_conversation(message)
    print("Response:", response)

    
    json_function = extract_json(response)

    if json_function:
        function_name = json_function.get("function_name")
        function_parms = json_function.get("function_parms")

        
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_parms}")

        print(f" -- Running {function_name} with parameters {function_parms}")

        
        action_function = available_actions[function_name]
        result = action_function(**function_parms)

        
        function_result_message = f"Action_Response: {result}"
        message.append({"role": "user", "content": function_result_message})
        print(function_result_message)
    else:
        break

    turn_count += 1



