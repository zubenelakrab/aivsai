import ollama
import time
import random
from termcolor import colored

# Initialize variables
chat_history = []
topic = "start wars"
agent_a = "Renato"
agent_b = "Elsa"

# Function to get a random temperature
def get_random_temperature():
    return random.uniform(0, 1.5)

# Function to add messages to chat history
def add_to_chat_history(role: str, content: str):
    chat_history.append({
        'role': role,
        'content': content,
    })

# Function to generate a message for an agent
def generate_agent_message(agent_name: str, role: str, expertise: str, message: str):
    temperature = get_random_temperature()
    response = ollama.chat(model='llama3', messages=[{
        "role": role,
        "content": f"You are {agent_name}, an AI assistant expert in {expertise}. Make questions if possible and always answer with something. Answers should be between 20 to 100 words. {message}"
    }], options={'temperature': temperature})
    
    if not response['message']['content']:
        response = ollama.chat(model='llama3', messages=[{
            "role": role,
            "content": f"{agent_name}, make a random question about this topic: {topic}"
        }], options={'temperature': temperature})
    
    return response, temperature

# Function for Agent A to send a message
def send_message_agent_A(message: str):
    try:
        response, temperature = generate_agent_message(agent_a, 'user', 'philosiphy, math, physics', message)
        response_content = response['message']['content']
        print(colored(f"{agent_a}({temperature}): {response_content}\n", 'blue'))
        add_to_chat_history('user', " ".join(response_content.splitlines()))
    except Exception as e:
        print(colored(f"Error in Agent A: {e}", 'red'))
    
    return response

# Function for Agent B to send a message
def send_message_agent_B(message: str):
    try:
        response, temperature = generate_agent_message(agent_b, 'system', 'philosiphy, math, physics', message)
        response_content = response['message']['content']
        print(colored(f"{agent_b}({temperature}): {response_content}\n", 'green'))
        add_to_chat_history('system', " ".join(response_content.splitlines()))
    except Exception as e:
        print(colored(f"Error in Agent B: {e}", 'red'))
    
    return response

# Function to get the last message from a specific agent
def get_last_agent_message(role: str):
    for message in reversed(chat_history):
        if message['role'] == role:
            return message['content']
    return None

# Start conversation loop
def start_conversation(num_exchanges=10):
    add_to_chat_history('user', f"Hi, {agent_a}, I want to talk about {topic}")
    print(colored(f"{agent_a}: Hi, I'm {agent_a}. Let's talk about {topic}.\n", 'yellow'))
    
    for n in range(num_exchanges):
        time.sleep(5)
        last_message_b = get_last_agent_message('system')
        if last_message_b:
            send_message_agent_A(last_message_b)
        
        time.sleep(5)
        last_message_a = get_last_agent_message('user')
        if last_message_a:
            send_message_agent_B(last_message_a)

# Main execution
if __name__ == "__main__":
    start_conversation()
