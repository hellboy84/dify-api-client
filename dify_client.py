#!/usr/bin/env python3
"""
DifyのAPIクライアント
質問を投げて回答を記録するプログラム
"""

import requests
import json
import datetime
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

class DifyClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        DifyClientの初期化
        
        Args:
            base_url: DifyのAPIベースURL（環境変数DIFY_BASE_URLからも取得可能）
            api_key: APIキー（環境変数DIFY_API_KEYからも取得可能）
        """
        self.base_url = (base_url or os.getenv('DIFY_BASE_URL', 'http://localhost/v1')).rstrip('/')
        self.api_key = api_key or os.getenv('DIFY_API_KEY')
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        
        # スクリプトのディレクトリを取得してログファイルパスを設定
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(script_dir, 'dify_chat_log.json')
    
    def send_message(self, message: str, user_id: str = "user", conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        メッセージをDifyに送信
        
        Args:
            message: 送信するメッセージ
            user_id: ユーザーID
            conversation_id: 会話ID（継続的な会話の場合）
            
        Returns:
            API応答の辞書
        """
        endpoint = f"{self.base_url}/chat-messages"
        
        payload = {
            "inputs": {},
            "query": message,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": user_id
        }
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # ログに記録
            self._log_interaction(message, result)
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            print(error_msg)
            return {"error": error_msg}
    
    def _log_interaction(self, question: str, response: Dict[str, Any]):
        """
        質問と回答をログファイルに記録
        
        Args:
            question: 質問内容
            response: API応答
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "question": question,
            "response": response
        }
        
        # 既存のログを読み込み
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []
        
        logs.append(log_entry)
        
        # ログを保存
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except PermissionError as e:
            print(f"警告: ログファイル保存権限エラー: {e}")
            print(f"ログファイルパス: {self.log_file}")
            # デスクトップに保存を試行
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            desktop_log_file = os.path.join(desktop_path, 'dify_chat_log.json')
            try:
                with open(desktop_log_file, 'w', encoding='utf-8') as f:
                    json.dump(logs, f, ensure_ascii=False, indent=2)
                print(f"ログをデスクトップに保存しました: {desktop_log_file}")
            except Exception as e2:
                print(f"デスクトップ保存も失敗: {e2}")
        except Exception as e:
            print(f"警告: ログファイル保存エラー: {e}")
    
    def get_answer(self, question: str) -> str:
        """
        質問に対する回答を取得（シンプルな形式）
        
        Args:
            question: 質問内容
            
        Returns:
            回答テキスト
        """
        result = self.send_message(question)
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        # 回答テキストを抽出
        if "answer" in result:
            return result["answer"]
        elif "data" in result and "answer" in result["data"]:
            return result["data"]["answer"]
        else:
            return "No answer found in response"
    
    def print_logs(self):
        """
        保存されたログを表示
        """
        if not os.path.exists(self.log_file):
            print("No logs found.")
            return
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            print(f"\n=== Chat Logs ({len(logs)} entries) ===")
            for i, log in enumerate(logs, 1):
                print(f"\n[{i}] {log['timestamp']}")
                print(f"Q: {log['question']}")
                if "answer" in log['response']:
                    print(f"A: {log['response']['answer']}")
                else:
                    print(f"Response: {json.dumps(log['response'], ensure_ascii=False, indent=2)}")
                print("-" * 50)
        
        except Exception as e:
            print(f"Error reading logs: {e}")


def main():
    """
    メイン関数（インタラクティブなチャット）
    """
    # APIキーを設定してください
    api_key = input("Enter your Dify API key (or press Enter to use environment variable): ").strip()
    if not api_key:
        api_key = None
    
    client = DifyClient(api_key=api_key)
    
    print("=== Dify Chat Client ===")
    print("Commands:")
    print("  /logs - Show chat logs")
    print("  /quit - Exit")
    print("  /help - Show this help")
    print("\nEnter your questions below:")
    
    while True:
        try:
            question = input("\nYou: ").strip()
            
            if not question:
                continue
            
            if question == "/quit":
                break
            elif question == "/logs":
                client.print_logs()
                continue
            elif question == "/help":
                print("Commands:")
                print("  /logs - Show chat logs")
                print("  /quit - Exit")
                print("  /help - Show this help")
                continue
            
            print("Bot: ", end="", flush=True)
            answer = client.get_answer(question)
            print(answer)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
