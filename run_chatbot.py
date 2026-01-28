import tkinter as tk
from tkinter import ttk, font
import threading
import time

from chatbot.ai_generator import generate_response
from chatbot.sentiment import analyse_sentiment
from chatbot.utils import is_exit


# Modern color scheme
BG_COLOR = "#0D1117"
SIDEBAR_COLOR = "#161B22"
CHAT_BG = "#0D1117"
USER_BUBBLE = "#238636"
BOT_BUBBLE = "#21262D"
INPUT_BG = "#21262D"
INPUT_BORDER = "#30363D"
TEXT_PRIMARY = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
ACCENT_COLOR = "#238636"
HOVER_COLOR = "#1F6FEB"


class ModernChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(700, 500)
        
        self.chat_history = ""
        self.first_message = True
        
        # Custom fonts
        self.title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        self.message_font = font.Font(family="Segoe UI", size=11)
        self.input_font = font.Font(family="Segoe UI", size=11)
        
        self.build_ui()
        
    def build_ui(self):
        """Build the complete single-screen UI"""
        # Main container
        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True)
        
        # Header
        self.build_header(main_container)
        
        # Chat area
        self.build_chat_area(main_container)
        
        # Suggestions (visible initially)
        self.build_suggestions()
        
        # Input area
        self.build_input_area(main_container)
        
    def build_header(self, parent):
        """Build modern header with gradient effect"""
        header = tk.Frame(parent, bg=SIDEBAR_COLOR, height=80)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header, bg=SIDEBAR_COLOR)
        header_content.pack(expand=True)
        
        # Bot icon/emoji
        icon_label = tk.Label(
            header_content,
            text="🤖",
            font=("Arial", 32),
            bg=SIDEBAR_COLOR
        )
        icon_label.pack(side="left", padx=(20, 10))
        
        # Title and subtitle
        title_frame = tk.Frame(header_content, bg=SIDEBAR_COLOR)
        title_frame.pack(side="left")
        
        tk.Label(
            title_frame,
            text="AI Assistant",
            font=self.title_font,
            bg=SIDEBAR_COLOR,
            fg=TEXT_PRIMARY
        ).pack(anchor="w")
        
        tk.Label(
            title_frame,
            text="Always here to help",
            font=("Segoe UI", 10),
            bg=SIDEBAR_COLOR,
            fg=TEXT_SECONDARY
        ).pack(anchor="w")
        
    def build_chat_area(self, parent):
        """Build scrollable chat area"""
        chat_container = tk.Frame(parent, bg=CHAT_BG)
        chat_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Canvas and scrollbar
        self.canvas = tk.Canvas(
            chat_container,
            bg=CHAT_BG,
            highlightthickness=0,
            highlightbackground=CHAT_BG
        )
        
        scrollbar = ttk.Scrollbar(
            chat_container,
            command=self.canvas.yview
        )
        
        self.chat_frame = tk.Frame(self.canvas, bg=CHAT_BG)
        
        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.chat_frame,
            anchor="nw",
            tags="chat_frame"
        )
        
        # Bind canvas width to chat_frame width
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def on_canvas_configure(self, event):
        """Adjust chat frame width when canvas is resized"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def build_suggestions(self):
        """Build suggestion chips that appear initially"""
        self.suggestions_frame = tk.Frame(self.chat_frame, bg=CHAT_BG)
        self.suggestions_frame.pack(pady=40, padx=30)
        
        # Welcome message
        welcome = tk.Label(
            self.suggestions_frame,
            text="👋 What can I help you with today?",
            font=("Segoe UI", 14, "bold"),
            bg=CHAT_BG,
            fg=TEXT_PRIMARY
        )
        welcome.pack(pady=(0, 20))
        
        # Suggestion prompts
        prompts = [
            "💼 I need assistance with my account",
            "🍽️ Recommend a good restaurant nearby",
            "🔐 How do I reset my password?",
            "🌤️ What's the weather like today?"
        ]
        
        for prompt in prompts:
            self.create_suggestion_chip(prompt)
            
    def create_suggestion_chip(self, text):
        """Create a modern suggestion chip button"""
        chip = tk.Button(
            self.suggestions_frame,
            text=text,
            font=("Segoe UI", 10),
            bg=BOT_BUBBLE,
            fg=TEXT_PRIMARY,
            activebackground=INPUT_BORDER,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=10,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=INPUT_BORDER,
            highlightcolor=ACCENT_COLOR,
            command=lambda: self.handle_suggestion_click(text)
        )
        chip.pack(pady=6, fill="x")
        
        # Hover effects
        chip.bind("<Enter>", lambda e: chip.config(bg=INPUT_BORDER))
        chip.bind("<Leave>", lambda e: chip.config(bg=BOT_BUBBLE))
        
    def handle_suggestion_click(self, text):
        """Handle suggestion chip click"""
        # Remove emoji from text
        clean_text = ' '.join(text.split()[1:])
        self.hide_suggestions()
        self.process_user_message(clean_text)
        
    def hide_suggestions(self):
        """Hide suggestion chips"""
        if hasattr(self, 'suggestions_frame'):
            self.suggestions_frame.destroy()
            
    def build_input_area(self, parent):
        """Build modern input area with send button"""
        input_container = tk.Frame(parent, bg=BG_COLOR)
        input_container.pack(fill="x", padx=20, pady=20)
        
        # Input frame with border effect
        input_frame = tk.Frame(
            input_container,
            bg=INPUT_BORDER,
            highlightthickness=1,
            highlightbackground=INPUT_BORDER
        )
        input_frame.pack(fill="x")
        
        # Inner frame
        inner_frame = tk.Frame(input_frame, bg=INPUT_BG)
        inner_frame.pack(fill="x", padx=1, pady=1)
        
        # Text input
        self.user_input = tk.Entry(
            inner_frame,
            font=self.input_font,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            highlightthickness=0,
            borderwidth=0
        )
        self.user_input.pack(
            side="left",
            fill="x",
            expand=True,
            padx=16,
            pady=14
        )
        self.user_input.bind("<Return>", self.send_message)
        
        # Focus effects
        self.user_input.bind("<FocusIn>", lambda e: input_frame.config(
            highlightbackground=ACCENT_COLOR,
            bg=ACCENT_COLOR
        ))
        self.user_input.bind("<FocusOut>", lambda e: input_frame.config(
            highlightbackground=INPUT_BORDER,
            bg=INPUT_BORDER
        ))
        
        # Send button
        send_btn = tk.Button(
            inner_frame,
            text="➤",
            font=("Arial", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground=HOVER_COLOR,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=3,
            height=1,
            borderwidth=0,
            command=self.send_message
        )
        send_btn.pack(side="right", padx=8)
        
        # Hover effect
        send_btn.bind("<Enter>", lambda e: send_btn.config(bg=HOVER_COLOR))
        send_btn.bind("<Leave>", lambda e: send_btn.config(bg=ACCENT_COLOR))
        
    def send_message(self, event=None):
        """Handle sending a message"""
        text = self.user_input.get().strip()
        if not text:
            return
            
        self.user_input.delete(0, tk.END)
        self.hide_suggestions()
        self.process_user_message(text)
        
    def process_user_message(self, text):
        """Process user message and generate response"""
        self.add_message(text, "user")
        
        if is_exit(text):
            self.add_message("Goodbye! 👋 Feel free to return anytime!", "bot")
            return
            
        self.show_loader()
        threading.Thread(target=self.generate_bot_reply, args=(text,), daemon=True).start()
        
    def generate_bot_reply(self, text):
        """Generate AI response in background thread"""
        sentiment = analyse_sentiment(text)
        
        prompt = (
            "You are a helpful, friendly AI assistant.\n"
            f"User sentiment: {sentiment}\n"
            f"User: {text}\nBot:"
        )
        
        response = generate_response(prompt, self.chat_history)
        self.chat_history += f"\nUser: {text}\nBot: {response}"
        self.chat_history = self.chat_history[-500:]
        
        time.sleep(0.6)
        self.root.after(0, self.display_bot_response, response)
        
    def add_message(self, text, msg_type):
        """Add a message bubble to the chat"""
        # Message container
        msg_container = tk.Frame(self.chat_frame, bg=CHAT_BG)
        msg_container.pack(fill="x", padx=20, pady=8)
        
        # Determine alignment and colors
        if msg_type == "user":
            anchor = "e"
            bubble_bg = USER_BUBBLE
            text_color = "white"
            max_width = 500
        else:
            anchor = "w"
            bubble_bg = BOT_BUBBLE
            text_color = TEXT_PRIMARY
            max_width = 550
            
        # Message bubble with proper text wrapping
        bubble = tk.Label(
            msg_container,
            text=text,
            font=self.message_font,
            bg=bubble_bg,
            fg=text_color,
            wraplength=max_width,  # Wrap text at max width
            justify="left",
            padx=16,
            pady=12,
            anchor="w"
        )
        bubble.pack(anchor=anchor)
        
        # Auto-scroll to bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
        
    def show_loader(self):
        """Show typing indicator"""
        self.loader_frame = tk.Frame(self.chat_frame, bg=CHAT_BG)
        self.loader_frame.pack(fill="x", padx=20, pady=8)
        
        loader_bubble = tk.Frame(
            self.loader_frame,
            bg=BOT_BUBBLE,
            padx=16,
            pady=12
        )
        loader_bubble.pack(anchor="w")
        
        # Animated dots
        self.loader_label = tk.Label(
            loader_bubble,
            text="●",
            font=("Arial", 12),
            bg=BOT_BUBBLE,
            fg=TEXT_SECONDARY
        )
        self.loader_label.pack()
        
        self.animate_loader()
        
        # Auto-scroll
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
        
    def animate_loader(self, dots=1):
        """Animate typing indicator"""
        if hasattr(self, 'loader_label') and self.loader_label.winfo_exists():
            dot_text = "●" * dots
            self.loader_label.config(text=dot_text)
            next_dots = (dots % 3) + 1
            self.root.after(400, self.animate_loader, next_dots)
            
    def display_bot_response(self, response):
        """Display bot response and remove loader"""
        if hasattr(self, "loader_frame"):
            self.loader_frame.destroy()
        self.add_message(response, "bot")


def main():
    root = tk.Tk()
    ModernChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()