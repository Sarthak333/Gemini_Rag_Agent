from dotenv import load_dotenv
load_dotenv()

import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def calculator(expression):
    expression = expression.replace("^", "**")  # fix: ^ means power, not XOR
    result = eval(expression)
    return result

# Description card so the AI knows this tool exists
calculator_tool = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="calculator",
        description="Evaluates a math expression and returns the exact result.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "expression": types.Schema(type="STRING", description="A math expression like '8473 * 9264'")
            },
            required=["expression"]
        )
    )
])

# Ask the user for a question
user_question = input("Ask me anything (math or general): ")

# Step 1: Send the question, telling the AI the calculator tool is available
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=user_question,
    config=types.GenerateContentConfig(tools=[calculator_tool])
)

part = response.candidates[0].content.parts[0]

# Step 2: Check if the AI wants to use the calculator
if part.function_call:
    expression = part.function_call.args["expression"]
    answer = calculator(expression)
    print(f"[Agent used calculator on: {expression}]")
    print("Answer:", answer)
else:
    # Step 3: If no tool was needed, just print the normal reply
    print("Answer:", part.text)