import tkinter as tk
from tkinter import scrolledtext

from chatbot.ai_generator import generate_response
from chatbot.sentiment import analyse_sentiment
from chatbot.utils import is_exit, is_greeting


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Text Generation Chatbot")

        self.chat_history = ""

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=60, height=20, state="disabled"
        )
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # User input
        self.user_input = tk.Entry(root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=10)

        self.display_message("Bot", "Hello! 😊 How can I help you today?")

    def display_message(self, sender, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message("You", user_text)
        self.user_input.delete(0, tk.END)

        if is_exit(user_text):
            self.display_message("Bot", "Goodbye! 👋")
            self.root.after(1000, self.root.destroy)
            return

        if is_greeting(user_text):
            self.display_message("Bot", "Hello! 😊 How can I help you today?")
            return

        sentiment = analyse_sentiment(user_text)

        prompt = (
            "You are an intelligent, friendly AI assistant. "
            "Answer clearly, informatively, and politely.\n"
            f"User sentiment: {sentiment}\n"
            f"User: {user_text}\n"
            "Bot:"
        )

        response = generate_response(prompt, self.chat_history)
        self.chat_history += f"\nUser: {user_text}\nBot: {response}"

        self.display_message("Bot", response)


def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
