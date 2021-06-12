import socket
import os
import traceback
from threading import Thread
from datetime import datetime
from typing import Tuple

class WorkerThread(Thread):
  # 実行ディレクトリ
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  # 静的配信ディレクトリ
  STATIC_ROOT = os.path.join(BASE_DIR, "public")

  # MIME Types
  MIME_TYPES = {
    "html": "text/html",
    "css": "text/css",
    "png": "image/png",
    "jpg": "image/png",
    "gif": "image/gif",
  }

  def __init__(self, client_socket: socket, address: Tuple[str, int]):
    super().__init__()

    self.client_socket = client_socket
    self.client_address = address

  def run(self,) -> None:
    # クライアントと接続済みの socket を受け取り、リクエストを処理してレスポンスを送信
    # クライアントからの送信データを取得
    try:
      request = self.client_socket.recv(4096)

      # クライアントからの送信データをファイルに書き出し
      with open("server_recv.txt", "wb") as f:
        f.write(request)

      method, path, http_version, request_header, request_body = self.parse_http_request(request)

      try:
        response_body = self.get_static_file_content(path)

        # レスポンスラインを生成
        response_line = "HTTP/1.1 200 OK\r\n"
        
      except OSError:
        # ファイルが見つからなかった場合
        not_found_file_path = os.path.join(self.STATIC_ROOT, "404.html")
        with open(not_found_file_path, "rb") as f:
          response_body = f.read()
        response_line = "HTTP/1.1 404 NotFound\r\n"

      response_header = self.build_response_header(path, response_body)

      # レスポンスを結合し bytes に変換
      response = (response_line + response_header + "\r\n").encode() + response_body

      # レスポンスを送信
      self.client_socket.send(response)

    except Exception:
      # リクエスト処理中に例外が発生した場合
      print("--Worker: リクエスト処理中にエラーが発生--")
      traceback.print_exc()

    finally:
      # 通信終了
      print(f"--Worker: クライアントとの接続完了 address: {self.client_address}--")
      self.client_socket.close()

  def parse_http_request(self, request: bytes) -> Tuple[str, str, str, bytes, bytes]:
    # リクエスト全体をパース
    request_line, remain = request.split(b"\r\n", maxsplit=1)
    request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

    # リクエストラインのーパース
    method, path, http_version = request_line.decode().split(" ")

    return method, path, http_version, request_header, request_body

  def get_static_file_content(self, path: str) -> bytes:
    # リクエストパスから static ファイルの内容を取得
    # path の先頭の / を削除し、相対パスへ
    relative_path = path.lstrip("/")
    # ファイルパスの取得
    static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

    # ファイルからレスポンスボディを取得
    with open(static_file_path, "rb") as f:
      return f.read()

  def build_response_header(self, path: str, response_body: bytes) -> str:
    # レスポンスヘッダーの構築
    # Content-type 取得
    # path から拡張子を取得
    if "." in path:
      ext = path.rsplit(".", maxsplit=1)[-1]
    else:
      ext = ""
    content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

    # レスポンスヘッダーを生成
    response_header = ""
    response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
    response_header += "Host: MyServer/0.1\r\n"
    response_header += f"Content-Length: {len(response_body)}\r\n"
    response_header += "Connection: Close\r\n"
    response_header += f"Content-Type: {content_type}\r\n"
    
    return response_header