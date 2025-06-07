import ollama

# Choose your model name (e.g., llama3, mistral, qwen, etc.)
model_name = "llama3"

print("🤖 Ollama Chatbot is ready! Type 'exit' to stop.\n")

# Store full conversation history
chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Get response from Ollama
    response = ollama.chat(model=model_name, messages=chat_history)

    # Print and save AI's reply
    ai_message = response["message"]["content"]
    print("AI:", ai_message)
    chat_history.append({"role": "assistant", "content": ai_message})
