# Instagram LLM Bot

このプロジェクトは、ファインチューニング済みのGPT-2モデルを用いてInstagramのDMに自動返信するシステムです。FastAPIでWebhookサーバーを構築し、Instagram Graph API経由でメッセージ送信を行います。

## ディレクトリ構成

```plaintext
instagram_llm_bot/
├── Dockerfile
├── README.md
├── requirements.txt
├── main.py
├── model/
├── data/
│   ├── train_data.jsonl
│   └── valid_data.jsonl
├── scripts/
│   ├── train.py
│   └── generate.py
└── docs/
    └── architecture.md
```

## セットアップ

1. **ローカル環境でのセットアップ**
   pyenvと仮想環境を利用してPython 3.9を使用してください。

   ```bash
   pyenv install 3.9.13
   pyenv local 3.9.13
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

2. **ファインチューニングの実施**
   学習データ（data/train_data.jsonl、data/valid_data.jsonl）を用意後、以下のコマンドでトレーニングを実行します。

   ```bash
   python scripts/train.py
   ```

3. **生成テスト**
   応答生成が正しく行われるか、以下のスクリプトで確認します。

   ```bash
   python scripts/generate.py
   ```

4. **FastAPIサーバーの起動**
   ローカルでWebhookサーバーとして動作確認します。

   ```bash
   uvicorn main:app --reload
   ```
