from transformers import pipeline, set_seed

# Load GPT-2 text generation model
generator = pipeline("text-generation", model="gpt2")
set_seed(42)

def generate_response(prompt, history=""):
    full_prompt = history + "\n" + prompt

    output = generator(
        full_prompt,
        max_length=len(full_prompt.split()) + 60,
        num_return_sequences=1,
        pad_token_id=50256,
        do_sample=True,
        temperature=0.8
    )

    generated_text = output[0]["generated_text"]

    # Extract only the new response
    response = generated_text.split("Bot:")[-1].strip()

    # Clean overly long outputs
    response = response.split("\n")[0]

    return response
