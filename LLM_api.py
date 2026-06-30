from dotenv import load_dotenv
from openai import OpenAI
import os
from datetime import datetime
import json

load_dotenv()


def calculator(a, b, operation):

    if operation == "+":
        return a + b

    elif operation == "-":
        return a - b

    elif operation == "*":
        return a * b

    elif operation == "/":
        if b == 0:
            return "Cannot divide by zero."
        return a / b

    return "Invalid operation."


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."


TOOLS = {
    "calculator": calculator,
    "current_time": current_time,
    "file_reader": read_file,
}


PROVIDERS = {
    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY"),
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-2.5-flash",
    },
    "owl": {
        "api_key": os.getenv("Owl_API_KEY"),
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openrouter/owl-alpha",
    },
    "gpt": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-oss-120b:free",
    }
}

provider = PROVIDERS["gemini"]

client = OpenAI(
    api_key=provider["api_key"],
    base_url=provider["base_url"]
)



messages = [
    {
        "role": "system",
        "content": """
You are an AI assistant.

When you need a tool, reply ONLY in JSON.

Calculator:

{
    "action":"calculator",
    "a":10,
    "b":20,
    "operation":"+"
}

Time:

{
    "action":"current_time"
}

File Reader:

{
    "action":"file_reader",
    "filename":"requirements.txt"
}

Rules:

1. If the user asks for calculations, use calculator.
2. If the user asks current time, use current_time.
3. If the user asks to read a file, use file_reader.
4. Otherwise answer normally.
5. dont give " ** " in reply
"""
    }
]

print("Chatbot Started")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:

        response = client.chat.completions.create(
            model=provider["model"],
            messages=messages
        )

        assistant_reply = response.choices[0].message.content

        try:

            tool_request = json.loads(assistant_reply)

            action = tool_request["action"]

          

            if action == "calculator":

                result = TOOLS[action](
                    tool_request["a"],
                    tool_request["b"],
                    tool_request["operation"]
                )

            elif action == "current_time":

                result = TOOLS[action]()

            elif action == "file_reader":

                result = TOOLS[action](
                    tool_request["filename"]
                )

            else:

                result = "Unknown tool."

           
            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

            
            messages.append(
                {
                    "role": "user",
                    "content": f"The tool returned: {result}. Please answer the original question."
                }
            )

            
            response = client.chat.completions.create(
                model=provider["model"],
                messages=messages
            )

            final_reply = response.choices[0].message.content

            print("AI:", final_reply)

            messages.append(
                {
                    "role": "assistant",
                    "content": final_reply
                }
            )

        except json.JSONDecodeError:

            print("AI:", assistant_reply)

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

    except Exception as e:

        print("Error:", e)