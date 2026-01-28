from chatbot.ai_generator import generate_response
from chatbot.sentiment import analyse_sentiment
from chatbot.utils import is_exit, is_greeting

def main():
    print("AI Chatbot (GPT-based)")
    print("Type 'bye' or 'quit' to exit.\n")

    chat_history = ""

    while True:
        user_input = input("You: ").strip()

        if is_exit(user_input):
            print("Bot: Goodbye! Take care.")
            break

        sentiment = analyse_sentiment(user_input)

        if is_greeting(user_input):
            print("Bot: Hello! How can I help you today?")
            continue

        # Add sentiment-aware prompt
        prompt = (
            f"The user sounds {sentiment}. "
            f"Respond in a friendly and helpful way.\n"
            f"User: {user_input}\nBot:"
        )

        response = generate_response(prompt, chat_history)
        chat_history += f"\nUser: {user_input}\nBot: {response}"

        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
