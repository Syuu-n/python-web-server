import socket

class TCPClient:
  # TCP クライアントクラス

  def request(self):
    print("--クライアント起動--")

    try:
      # socket生成
      client_socket = socket.socket()
      client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      # サーバー接続
      print("--サーバーと接続--")
      client_socket.connect(("127.0.0.1", 80))
      print("--サーバとの接続が完了--")

      # リクエストをファイルから取得
      with open("client_send.txt", "rb") as f:
        request = f.read()

      # リクエスト送信
      client_socket.send(request)

      # サーバーからのレスポンス取得
      response = client_socket.recv(4096)

      # レスポンスをファイルへ書き出す
      with open("client_recv.txt", "wb") as f:
        f.write(response)

      # 通信終了
      client_socket.close()

    finally:
      print("--クライアント停止--")

if __name__ == '__main__':
  client = TCPClient()
  client.request()