#ベースイメージはLinux向け
FROM python:3.9-slim

#作業ディレクトリを作成
WORKDIR /app

#依存関係ファイルをコピー
COPY requirements.txt .

#依存関係のインストール
RUN pip install --upgrade pip && pip install -r requirements.txt

#アプリケーションのコピー
COPY . .

# FastAPIの実行
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
