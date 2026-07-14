# Gemini_Rag_Agent
# RAG + Tool-Calling AI Agent

I built this to actually learn how agentic AI and RAG work, rather than just reading about them. It's a set of small AI agents built with Google's Gemini API, 
each one adding a new capability on top of the last.

## What's in here

**`chat.py`** — A chatbot that actually remembers the conversation. LLMs don't have memory by default — every request is a blank slate.
This resends the full conversation history each time, which is how "memory" actually works under the hood.

**`tool_agent.py`** — An agent that can use tools. LLMs are surprisingly bad at exact math (they predict likely-looking numbers, they don't calculate).
This agent recognizes when a question needs real math, calls a Python calculator function to get the exact answer, and responds with that — instead of guessing.

**`rag_agent.py`** — A RAG pipeline built from scratch. It takes a document, breaks it into chunks,
converts each chunk into an embedding (numbers that represent meaning), and when you ask a question, it finds the most relevant chunk by comparing meanings — not keywords — and
uses that to generate an accurate, grounded answer.

## Example

The `Documents` folder includes a sample company policy file used to test the RAG agent. Example interaction:

**Question:** How many vacation days do I get?

**Agent's answer:** You get 20 paid vacation days per year.

The agent found this by searching the document for the most semantically relevant chunk not just keyword matching and generating an answer grounded in that specific text.

## Stack

Python, Gemini API, NumPy for similarity search. No frameworks like LangChain — built the core logic manually to actually understand what's happening at each step.

## Running it

```
pip install google-genai python-dotenv numpy
```

Add a `.env` file with:
```
GEMINI_API_KEY= API KEY
```

Then run whichever agent you want:
```
python chat.py
python tool_agent.py
python rag_agent.py
```
## Bugs I ran into

The most interesting one: the LLM would send `1308313^2` when asked to square a number, expecting `^` to mean "power." Python interprets `^` as a bitwise XOR operation instead,
giving a completely wrong answer that still *looked* plausible. Fixed by converting `^` to `**` before evaluating. Small bug, but a good lesson — tool-calling only works if you're
strict about the exact format the model is going to send.

## What I'd add next

- Merge tool-calling and RAG into a single agent that can do both
- Swap the in-memory chunk storage for a real vector database (ChromaDB)
- Wrap it in a basic UI instead of a terminal chat
