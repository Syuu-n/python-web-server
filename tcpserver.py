import socket

class TCPServer:
  # TCP サーバークラス

  def serve(self):
    print("--サーバーを起動します---")

    try:
      # socket 生成
      server_socket = socket.socket()
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      # socket を 8080 ポートへ
      server_socket.bind(("localhost", 8080))
      server_socket.listen(10)

      # 外部からの接続を待つ
      print("--クライアントからの接続を待機中--")
      (client_socket, address) = server_socket.accept()
      print(f"--クライアントとの接続が完了しました remote_address: {address}--")

      # クライアントからのデータを取得
      request = client_socket.recv(4096)

      # クライアントからのデータをファイルへ書き出す
      with open("server_recv.txt", "wb") as f:
        f.write(request)

      # クライアントへ送信するレスポンスデータを取得
      with open("server_send.txt", "rb") as f:
        response = f.read()

      client_socket.send(response)

      # 通信を終了
      client_socket.close()

    finally:
      print("--サーバーを停止しました--")

if __name__ == '__main__':
  server = TCPServer()
  server.serve()