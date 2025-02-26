# Architecture Overview

このシステムは、ファインチューニング済みのGPT-2モデルを利用してInstagramのDMに自動返信する仕組みです。

## 主なコンポーネント

- **FastAPIサーバー**
  - InstagramからのWebhookイベントを受け取り、入力メッセージをモデルで処理して応答を生成。
  - Instagram Graph APIを用いてDMで返信。

- **ファインチューニング済みモデル**
  - `scripts/train.py` を用いて、キャラクター設定・下ネタ・時事情報を反映したモデルを作成。
  - 学習済みチェックポイントは `model/` に保存。

- **データ管理**
  - 学習データは `data/` 配下にJSONL形式で管理。

- **Dockerによる環境統一**
  - Dockerfileにより、依存環境を統一し、GCPへのデプロイを容易に。

- **GCPデプロイ**
  - DockerイメージをGoogle Container Registryにプッシュし、Cloud RunまたはGKEでデプロイ。

## データフロー

1. **Instagram** がWebhookイベントを送信。
2. **FastAPIサーバー** がイベントを受信し、送信者IDとメッセージ本文を抽出。
3. **ファインチューニング済みモデル** で応答を生成。
4. **Instagram Graph API** 経由で生成した応答をDMとして返信。

## 運用・モニタリング

- ログ管理、エラーハンドリング、出力フィルタリング等の運用体制を整備。
- 定期的な再トレーニングで最新情報を反映。
