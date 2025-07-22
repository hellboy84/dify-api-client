# これは何？

**DifyのAPI機能を使用して質問・回答のやり取りを行うPythonプログラムです。**  

MIS40の口頭発表[「Difyで自作したレファレンスチャットボットを用いた文章生成AIの性能比較」](https://plaza.umin.ac.jp/mis/40/program.html) で使用しました。   
対話機能のほか、質問をtxtファイルから読み込み回答をCSV形式で保存する機能を提供します。  
発表内容の補足の意味に加えて、一般的なDifyの利用時にも役に立つ(と思う)プログラムのため公開しました。  

## 🚀 機能

- **インタラクティブチャット**: リアルタイムでDify APIと対話
- **バッチ処理**: 複数の質問を一括処理してCSV出力 ← MIS40の実験ではこれを使用
- **ログ機能**: 全ての質問・回答を自動的にJSONファイルに記録
- **エラーハンドリング**: 権限エラー時の代替保存先対応

## 📁 ファイル構成

```
dify-api-client/
├── .env                    # API設定ファイル（APIキー、ベースURL）
├── dify_client.py          # メインのAPIクライアントクラス
├── question_batch.py       # 質問バッチ処理スクリプト
├── questions.txt           # 質問リスト（1行に1つずつ記載）
├── requirements.txt        # Python依存関係
├── dify_chat_log.json      # チャットログ（自動生成）
└── *_dify_answers_only.csv # 回答のみのCSV（自動生成）
```

## 🛠️ セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/hellboy84/dify-api-client.git
cd dify-api-client
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. 環境設定

`.env`ファイルを編集して、実際のAPIキーを設定してください：

```env
# APIキー（実際の値に変更してください）
DIFY_API_KEY=your-actual-dify-api-key-here

# ローカル開発環境のBASE_URL
DIFY_BASE_URL=http://localhost/v1

# 本番環境のBASE_URL（必要に応じてコメントアウトを解除）
# DIFY_BASE_URL=https://api.dify.ai/v1
```

## 📝 使用方法

### インタラクティブモード

リアルタイムでDify APIと対話できます：

```bash
python dify_client.py
```

利用可能なコマンド：
- `/logs` - チャットログを表示
- `/quit` - 終了
- `/help` - ヘルプを表示

### バッチ処理モード

`questions.txt`に記載された質問を一括処理し、結果をCSVファイルに保存します。  
各行ごとに新しい質問として処理されます：

```bash
python question_batch.py
```

処理結果は`YYYYMMDDHHMMSS_dify_answers_only.csv`という形式でタイムスタンプ付きファイルに保存されます。

### 質問ファイルの編集

`questions.txt`に質問を1行ずつ記載してください：

```txt
大橋病院に勤務しています。研究費で資料を買いましたがどうすればいいですか？
科研費で12万円の専門書を購入しました。どのような手続きが必要でしょうか？
...
```

## 🔧 設定オプション

### 環境変数

- `DIFY_API_KEY`: DifyのAPIキー（必須）
- `DIFY_BASE_URL`: APIのベースURL（デフォルト: `http://localhost/v1`）

### ファイル保存

- **通常**: スクリプトと同じディレクトリに保存
- **権限エラー時**: 自動的にデスクトップに保存を試行

## 📊 出力形式

### CSVファイル（バッチ処理結果）

| question_number | timestamp | question | answer |
|---|---|---|---|
| 1 | 2025-07-22T15:30:00.123456 | 研究費で資料を... | 研究費で購入された... |

### JSONログファイル

```json
[
  {
    "timestamp": "2025-07-22T15:30:00.123456",
    "question": "研究費で資料を買いましたがどうすればいいですか？",
    "response": {
      "answer": "研究費で購入された資料については...",
      "conversation_id": "...",
      "...": "..."
    }
  }
]
```

## 🐛 トラブルシューティング

### よくある問題

1. **APIキーエラー**: `.env`ファイルでDIFY_API_KEYが正しく設定されているか確認
2. **接続エラー**: DIFY_BASE_URLが正しく設定されているか確認
3. **ファイル保存エラー**: ディレクトリの書き込み権限を確認

### エラーログ

詳細なエラー情報はコンソール出力で確認できます。バッチ処理実行時にエラーが発生した場合、エラー内容もCSVファイルに記録されます。

## 🔗 関連リンク

- [Dify API Documentation](https://docs.dify.ai/en/openapi-api-access-readme#api-access)
- [Python Requests Documentation](https://docs.python-requests.org/)

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## ℹ️ 注記

このプログラムはLLMの支援を受けながら作成しました

---

**作成日**: 2025年7月22日
