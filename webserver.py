import socket

from workerthread import WorkerThread

class WebServer:
  # Web サーバークラス

  def serve(self):
    # サーバー起動
    print ("--Server: サーバーを起動--")

    try:
      server_socket = self.create_server_socket()

      while True:
        # 外部からの接続をまち、コネクションを確立する
        print("--Server: クライアントからの接続待ち--")
        (client_socket, address) = server_socket.accept()
        print(f"--Server: クライアントとの接続完了 address: {address}--")
        
        # 並行処理するスレッドを作成
        thread = WorkerThread(client_socket, address)
        # スレッド実行
        thread.start()

    finally:
      print("--Server: サーバー停止--")

  def create_server_socket(self) -> socket:
    # socket 生成
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # socket を localhost:8080 へバインド
    server_socket.bind(("localhost", 8080))
    server_socket.listen(10)
    return server_socket

if __name__ == '__main__':
  server = WebServer()
  server.serve()