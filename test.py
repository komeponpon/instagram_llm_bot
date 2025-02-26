import torch
from transformers import AutoModelForCausalLM, T5Tokenizer

# デバイスの設定
device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

# モデルとトークナイザーの読み込み
model_path = "./model"
# 元のモデルからトークナイザーを読み込む
tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-medium")
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

def generate_response(input_text: str) -> str:
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    output_ids = model.generate(
        input_ids,
        max_length=100,
        do_sample=True,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# テストケース
test_inputs = [
    "今日はどんな一日だった？",
    "ちょっと下ネタって言ったら",
    "明日の天気はどう？",
    "こんにちは！",  # 学習データにない入力
]

print("=== モデルテスト開始 ===")
for test_input in test_inputs:
    print(f"\n入力: {test_input}")
    response = generate_response(test_input)
    print(f"応答: {response}")
print("\n=== テスト完了 ===")

