import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "What is prompt injection? Explain in 2 lines."}
    ],
)

print(response["message"]["content"])