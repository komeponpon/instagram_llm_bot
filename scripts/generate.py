# テストコード
import torch
from transformers import AutoModelForCausalLM, T5Tokenizer

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

model_path = "./model"
tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-medium")
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

def generate_text(prompt: str) -> str:
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output_ids = model.generate(
        input_ids,
        max_length=100,
        do_sample=True,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

if __name__ == "__main__":
    while True:
        prompt = input("Enter prompt: ")
        response = generate_text(prompt)
        print("Generated response:", response)
