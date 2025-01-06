# README

## Overview
This project demonstrates a **dynamic AI agent** designed to interact with users, reason step-by-step, and perform external actions based on user queries. The agent follows a structured workflow of **Thought → Action → PAUSE → Action_Response → Answer**, leveraging tools to execute specific tasks and provide meaningful responses.

---

## Key Features

1. **Interactive Agent Workflow**:
   - The agent thinks through the problem, decides on the required action, executes it, processes the response, and provides an answer.
   - It operates in a loop to handle multi-turn interactions.

2. **Tool Integration**:
   - External tools, such as `get_response_time`, are integrated into the system.
   - Tools are invoked dynamically based on the user's query, enabling the agent to perform specialized tasks.

3. **Customizable Inputs**:
   - Accepts user-defined queries to dynamically adapt the agent's behavior.

4. **Error Handling**:
   - Validates tool names and parameters before execution.
   - Ensures safe and expected behavior even when encountering unknown inputs.

5. **Modular Design**:
   - Actions are mapped to functions using a dictionary (`available_actions`), making the system extensible and easy to modify.

6. **Iterative Execution**:
   - A `while` loop ensures the agent refines its understanding and actions over multiple iterations, supporting multi-step reasoning.

---

## Key Learnings

### 1. **Agent Design Workflow**:
   - The structured workflow ensures that the agent reasons, acts, and adapts iteratively.
   - This approach is essential for building robust, dynamic, and task-oriented agents.

### 2. **Tool Integration in AI Agents**:
   - Tools enhance the agent’s functionality by allowing it to perform specific tasks beyond text generation.
   - Mapping tool names to functions enables seamless dynamic execution.

### 3. **Dynamic JSON Parsing and Execution**:
   - Extracting actionable instructions (e.g., tool name and parameters) from JSON outputs enables efficient task execution.

### 4. **System Prompt Engineering**:
   - A detailed system prompt guides the agent's reasoning and ensures consistent behavior.

### 5. **Seamless Interaction Between LLM and Functions**:
   - Combines the reasoning capabilities of a large language model (LLM) with external tools for enhanced functionality.

---

## How to Run the Code

1. **Dependencies**:
   - Python 3.7 or higher
   - `openai` library
   - `dotenv` for environment variable management

2. **Setup**:
   - Install the required libraries:
     ```bash
     pip install openai python-dotenv
     ```
   - Create a `.env` file in the root directory and add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the Code**:
   - Execute the script using:
     ```bash
     python script_name.py
     ```
   - Enter a website URL when prompted to see the agent in action.

---

## Example Interaction

### Input:
```
Enter the website to know the response time of it: google.com
```

### Output:
```
Loop: 1
----------------------
Response: {"function_name": "get_response_time", "function_parms": {"url": "google.com"}}
 -- Running get_response_time with parameters {'url': 'google.com'}
Action_Response: 0.3
```

---

## Additional Notes

- The project highlights the foundational concepts of building **dynamic, tool-using agents**, focusing on:
  - Structured reasoning
  - Tool integration
  - Iterative problem-solving workflows

- These concepts are critical for advanced AI applications such as autonomous agents, chatbots, and task-specific assistants.

---

## Future Enhancements

1. Add support for more tools and actions.
2. Improve error handling for unsupported actions or malformed user inputs.
3. Incorporate a GUI for better user interaction.

