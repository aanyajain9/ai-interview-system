import ollama_test

response = ollama_test.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "What is Python?"
        }
    ]
)

print(response["message"]["content"])