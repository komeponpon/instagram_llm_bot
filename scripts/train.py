import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, T5Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

base_model_name = "rinna/japanese-gpt2-medium"
tokenizer = T5Tokenizer.from_pretrained(base_model_name)
model = AutoModelForCausalLM.from_pretrained(base_model_name).to(device)

def tokenize_function(examples):
    texts = [f"{prompt}\n{response}" for prompt, response in zip(examples["prompt"], examples["response"])]
    return tokenizer(texts, truncation=True, padding="max_length", max_length=128)

dataset = load_dataset("json", data_files={"train": "./data/train_data.jsonl", "validation": "./data/valid_data.jsonl"})

tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["prompt", "response"])

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./model",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
)

trainer.train()

# モデルとトークナイザーの両方を保存
trainer.save_model("./model")
tokenizer.save_pretrained("./model")
