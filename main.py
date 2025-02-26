from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import requests
import torch
from transformers import AutoModelForCausalLM, T5Tokenizer

# 環境変数からInstagram Graph APIの設定を取得
INSTAGRAM_VERIFY_TOKEN = os.environ.get("INSTAGRAM_VERIFY_TOKEN")
INSTAGRAM_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = os.environ.get("IG_USER_ID")

# APIエンドポイントのフォーマット（必要に応じて上書き可能）
INSTAGRAM_API_URL = os.environ.get("INSTAGRAM_API_URL", "https://graph.facebook.com/v17.0/{ig_user_id}/messages")

# 必須の環境変数が設定されているか検証
if not INSTAGRAM_VERIFY_TOKEN or not INSTAGRAM_ACCESS_TOKEN or not IG_USER_ID:
    raise Exception("Missing required environment variables: INSTAGRAM_VERIFY_TOKEN, INSTAGRAM_ACCESS_TOKEN, IG_USER_ID")

# デバイスの設定（MPS, CUDA, もしくはCPU）
device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

# モデルの読み込み
model_path = "./model"
# 元のモデルからトークナイザーを読み込む
tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-medium")
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

app = FastAPI()

# Webhook検証用GETエンドポイント
@app.get("/webhook")
async def verify_webhook(mode: str = None, challenge: str = None, verify_token: str = None):
    if mode and verify_token:
        if mode == "subscribe" and verify_token == INSTAGRAM_VERIFY_TOKEN:
            return challenge
    raise HTTPException(status_code=403, detail="Verification failed")

# Webhook受信用POSTエンドポイント
@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    try:
        entries = payload.get("entry", [])
        for entry in entries:
            messaging = entry.get("messaging", [])
            for message_event in messaging:
                if "message" in message_event:
                    sender_id = message_event["sender"]["id"]
                    message_text = message_event["message"].get("text", "")
                    # モデルで応答を生成
                    response_text = generate_response(message_text)
                    # Instagram DMを送信
                    send_instagram_dm(sender_id, response_text)
        return {"status": "EVENT_RECEIVED"}
    except Exception as e:
        print("Error processing webhook:", e)
        raise HTTPException(status_code=500, detail="Error processing webhook")

def generate_response(input_text: str) -> str:
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    output_ids = model.generate(
        input_ids,
        max_length=100,
        do_sample=True,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_text

def send_instagram_dm(recipient_id: str, message: str):
    url = INSTAGRAM_API_URL.format(ig_user_id=IG_USER_ID)
    headers = {
        "Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print("Failed to send DM:", response.text)
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
