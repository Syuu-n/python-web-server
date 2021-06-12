import socket
import os
import traceback
from datetime import datetime

class WebServer:
  # Web サーバークラス

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

  def serve(self):
    # サーバー起動
    print ("--サーバーを起動--")

    try:
      # socket 生成
      server_socket = socket.socket()
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      # socket を localhost:8080 へバインド
      server_socket.bind(("localhost", 8080))
      server_socket.listen(10)

      while True:
        # 外部からの接続をまち、コネクションを確立する
        print("--クライアントからの接続待ち--")
        (client_socket, address) = server_socket.accept()
        print(f"--クライアントとの接続完了 address: {address}--")

        try:
          # クライアントからの送信データを取得
          request = client_socket.recv(4096)

          # クライアントからの送信データをファイルに書き出し
          with open("server_recv.txt", "wb") as f:
            f.write(request)

          # リクエスト全体をパース
          request_line, remain = request.split(b"\r\n", maxsplit=1)
          request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

          # リクエストラインのーパース
          method, path, http_version = request_line.decode().split(" ")

          # path の先頭の / を削除し、相対パスへ
          relative_path = path.lstrip("/")
          # ファイルパスの取得
          static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

          # ファイルからレスポンスボディを取得
          try:
            with open(static_file_path, "rb") as f:
              response_body = f.read()
            # レスポンスラインを生成
            response_line = "HTTP/1.1 200 OK\r\n"
            
          except OSError:
            # ファイルが見つからなかった場合
            not_found_file_path = os.path.join(self.STATIC_ROOT, "404.html")
            with open(not_found_file_path, "rb") as f:
              response_body = f.read()
            response_line = "HTTP/1.1 404 NotFound\r\n"

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

          # レスポンスを結合し bytes に変換
          response = (response_line + response_header + "\r\n").encode() + response_body

          # レスポンスを送信
          client_socket.send(response)

        except Exception:
          # リクエスト処理中に例外が発生した場合
          print("--リクエスト処理中にエラーが発生--")
          traceback.print_exc()

        finally:
          # 通信終了
          client_socket.close()

    finally:
      print("--サーバー停止--")

if __name__ == '__main__':
  server = WebServer()
  server.serve()