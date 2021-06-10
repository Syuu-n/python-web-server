import socket
from datetime import datetime

class WebServer:
  # Web サーバークラス
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

      # 外部からの接続をまち、コネクションを確立する
      print("--クライアントからの接続待ち--")
      (client_socket, address) = server_socket.accept()
      print(f"--クライアントとの接続完了 address: {address}--")

      # クライアントからの送信データを取得
      request = client_socket.recv(4096)

      # クライアントからの送信データをファイルに書き出し
      with open("server_recv.txt", "wb") as f:
        f.write(request)

      # レスポンスボディを生成
      response_body = "<html><body><h1>It works!</h1></body></html>"

      # レスポンスラインを生成
      response_line = "HTTP/1.1 200 OK\r\n"

      # レスポンスヘッダーを生成
      response_header = ""
      response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
      response_header += "Host: MyServer/0.1\r\n"
      response_header += f"Content-Length: {len(response_body.encode())}\r\n"
      response_header += "Connection: Close\r\n"
      response_header += "Content-Type: text/html\r\n"

      # レスポンスを結合し bytes に変換
      response = (response_line + response_header + "\r\n" + response_body).encode()

      # レスポンスを送信
      client_socket.send(response)

      # 通信終了
      client_socket.close()

    finally:
      print("--サーバー停止--")

if __name__ == '__main__':
  server = WebServer()
  server.serve()