import tkinter as tk
from tkinter import ttk
import threading
import time

from chatbot.ai_generator import generate_response
from chatbot.sentiment import analyse_sentiment
from chatbot.utils import is_exit, is_greeting


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f5f5")

        self.chat_history = ""

        # Chat canvas (for alignment)
        self.canvas = tk.Canvas(root, bg="#f5f5f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.chat_frame = tk.Frame(self.canvas, bg="#f5f5f5")

        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Input area
        self.input_frame = tk.Frame(root, bg="#eeeeee")
        self.input_frame.pack(fill="x", padx=10, pady=10)

        self.user_input = tk.Entry(self.input_frame, font=("Arial", 12))
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame, text="Send", command=self.send_message, bg="#4CAF50", fg="white"
        )
        self.send_button.pack(side="right")

        self.add_message("Bot", "Hello! 😊 How can I help you today?", "bot")

    # ---------- UI HELPERS ----------

    def add_message(self, sender, text, msg_type):
        container = tk.Frame(self.chat_frame, bg="#f5f5f5")

        if msg_type == "user":
            bubble_bg = "#d0e6ff"
            anchor = "w"
        else:
            bubble_bg = "#d6f5d6"
            anchor = "e"

        # Shadow
        shadow = tk.Label(
            container, text=text, bg="#cccccc", wraplength=380, justify="left"
        )
        shadow.pack(anchor=anchor, padx=6, pady=2)

        bubble = tk.Label(
            container,
            text=text,
            bg=bubble_bg,
            wraplength=380,
            justify="left",
            padx=10,
            pady=6
        )
        bubble.place(x=0, y=0)

        container.pack(anchor=anchor, pady=5, padx=10)

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def show_loader(self):
        self.loader = tk.Label(
            self.chat_frame,
            text="...",
            font=("Arial", 14),
            bg="#e0e0e0",
            padx=10,
            pady=5
        )
        self.loader.pack(anchor="e", padx=15, pady=5)
        self.canvas.yview_moveto(1.0)

    def hide_loader(self):
        if hasattr(self, "loader"):
            self.loader.destroy()

    # ---------- CHAT LOGIC ----------

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.add_message("You", user_text, "user")
        self.user_input.delete(0, tk.END)

        if is_exit(user_text):
            self.add_message("Bot", "Goodbye! 👋", "bot")
            self.root.after(1000, self.root.destroy)
            return

        self.send_button.config(state="disabled")
        self.user_input.config(state="disabled")

        self.show_loader()

        threading.Thread(target=self.generate_bot_reply, args=(user_text,)).start()

    def generate_bot_reply(self, user_text):
        if is_greeting(user_text):
            response = "Hello! 😊 How can I help you today?"
        else:
            sentiment = analyse_sentiment(user_text)
            prompt = (
                "You are an intelligent, friendly AI assistant.\n"
                f"User sentiment: {sentiment}\n"
                f"User: {user_text}\nBot:"
            )
            response = generate_response(prompt, self.chat_history)
            self.chat_history += f"\nUser: {user_text}\nBot: {response}"
            self.chat_history = self.chat_history[-500:]

        time.sleep(0.6)  # natural pause
        self.root.after(0, self.display_bot_response, response)

    def display_bot_response(self, response):
        self.hide_loader()
        self.add_message("Bot", response, "bot")

        self.send_button.config(state="normal")
        self.user_input.config(state="normal")
        self.user_input.focus()


def main():
    root = tk.Tk()
    ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
