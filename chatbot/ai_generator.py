from transformers import pipeline
import torch
import re

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",   
    device=0 if torch.cuda.is_available() else -1
)

BAD_PATTERNS = [
    r"\b\d+\s+days?\s+ago\b",
    r"\b\d+\s+comments?\b",
    r"·",
    r"reddit",
    r"posted by",
]

def clean_response(text):
    for pattern in BAD_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()

def generate_response(prompt, history=""):
    # Limit memory to last 500 characters
    history = history[-500:]

    full_prompt = history + "\n" + prompt

    output = generator(
        full_prompt,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2,
        pad_token_id=50256
    )

    generated_text = output[0]["generated_text"]

    # Extract assistant reply only
    response = generated_text.split("Bot:")[-1]

    # Stop if model tries to continue dialogue
    for stop in ["User:", "Bot:"]:
        if stop in response:
            response = response.split(stop)[0]

    response = clean_response(response)

    # Fallback if response is bad
    if len(response) < 5:
        response = "I'm doing well, thanks for asking! How about you?"

    return response
