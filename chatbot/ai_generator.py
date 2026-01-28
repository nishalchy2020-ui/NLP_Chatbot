from transformers import pipeline
import torch

# Load model once
generator = pipeline(
    "text-generation",
    model="gpt2",
    device=0 if torch.cuda.is_available() else -1
)

def generate_response(prompt, history=""):
    full_prompt = history + "\n" + prompt

    output = generator(
        full_prompt,
        max_new_tokens=120,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2,
        pad_token_id=50256
    )

    generated_text = output[0]["generated_text"]

    # Extract only the assistant reply
    response = generated_text.split("Bot:")[-1].strip()

    # Stop at accidental extra turns
    for stop_token in ["User:", "Bot:"]:
        if stop_token in response:
            response = response.split(stop_token)[0]

    return response.strip()
