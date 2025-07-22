#!/usr/bin/env python3
"""
Dify API 質問バッチ処理
質問ファイルから質問を読み込み、回答をCSV形式で保存する
"""


from dify_client import DifyClient
import json
import datetime
import os
import csv
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

def load_questions_from_file(filepath):
    """
    テキストファイルから質問リストを読み込む（空行は無視）
    """
    questions = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                q = line.strip()
                if q:
                    questions.append(q)
    except Exception as e:
        print(f"❌ 質問ファイルの読み込みエラー: {e}")
    return questions

def save_answers_only(answers):
    """
    回答のみをCSV形式で保存（タイムスタンプ付きファイル名）
    
    Args:
        answers: 回答リスト
    """
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ファイル名に日時を追加
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_dify_answers_only.csv"
    
    # 絶対パスでファイルパスを構築
    filepath = os.path.join(script_dir, filename)
    
    print(f"ファイル保存先: {filepath}")
    
    try:
        # CSVファイルに保存
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # ヘッダー行
            writer.writerow(['question_number', 'timestamp', 'question', 'answer'])
            
            # データ行
            for item in answers:
                writer.writerow([
                    item['question_number'],
                    item['timestamp'],
                    item['question'],
                    item['answer']
                ])
        
        print(f"\n回答のみを {filename} に保存しました。")
        
    except PermissionError as e:
        print(f"\n❌ ファイル保存権限エラー: {e}")
        print(f"保存先: {filepath}")
        print("別の場所への保存を試みます...")
        
        # デスクトップに保存を試行
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        desktop_filepath = os.path.join(desktop_path, filename)
        
        try:
            with open(desktop_filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['question_number', 'timestamp', 'question', 'answer'])
                for item in answers:
                    writer.writerow([
                        item['question_number'],
                        item['timestamp'],
                        item['question'],
                        item['answer']
                    ])
            print(f"✓ デスクトップに保存しました: {desktop_filepath}")
        except Exception as e2:
            print(f"❌ デスクトップ保存も失敗: {e2}")
    
    except Exception as e:
        print(f"\n❌ ファイル保存エラー: {e}")
        print(f"保存先: {filepath}")

def main():
    """
    質問バッチ処理のメイン関数
    """
    print("=== Dify API クライアント開始 ===")
    
    # 実行環境の確認
    print(f"スクリプトの場所: {os.path.abspath(__file__)}")
    print(f"現在の作業ディレクトリ: {os.getcwd()}")
    
    # 環境確認
    try:
        import requests
        print("✓ requestsライブラリ確認OK")
    except ImportError:
        print("❌ requestsライブラリが見つかりません")
        print("pip install requests を実行してください")
        return
    
    # クライアントの初期化（.envファイルから設定を読み込み）
    try:
        api_key = os.getenv('DIFY_API_KEY')
        base_url = os.getenv('DIFY_BASE_URL', 'http://localhost/v1')
        
        if not api_key:
            print("❌ APIキーが設定されていません。")
            print(".envファイルにDIFY_API_KEYを設定してください。")
            return
        
        client = DifyClient(
            base_url=base_url,
            api_key=api_key
        )
        print("✓ DifyClient初期化OK")
    except Exception as e:
        print(f"❌ DifyClient初期化エラー: {e}")
        return
    
    # 質問リストをファイルから読み込む
    questions_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.txt")
    questions = load_questions_from_file(questions_file)
    if not questions:
        print("❌ 質問が見つかりません。questions.txt を確認してください。")
        return

    print("=== Dify API Test ===")

    answers_only = []

    for i, question in enumerate(questions, 1):
        print(f"\n[{i}] Question: {question}")

        try:
            # 回答を取得
            answer = client.get_answer(question)
            print(f"Answer: {answer}")

            # 回答のみを記録
            answers_only.append({
                "question_number": i,
                "question": question,
                "answer": answer,
                "timestamp": datetime.datetime.now().isoformat()
            })

        except Exception as e:
            error_msg = f"質問{i}でエラー: {e}"
            print(f"Answer: {error_msg}")

            # エラーも記録
            answers_only.append({
                "question_number": i,
                "question": question,
                "answer": error_msg,
                "timestamp": datetime.datetime.now().isoformat()
            })

        print("-" * 50)

    # 回答のみを保存
    print("\n=== ファイル保存処理 ===")
    save_answers_only(answers_only)

    # 回答のみを表示
    print("\n=== 回答まとめ ===")
    for i, item in enumerate(answers_only, 1):
        print(f"[{i}] {item['answer']}")
        print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("詳細:")
        import traceback
        traceback.print_exc()
    
    # ウィンドウが閉じないよう入力待ち
    input("\n何かキーを押してください...")
