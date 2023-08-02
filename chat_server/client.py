import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def receive_messages(self, client_socket):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(message)
        except:
            pass

    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()

        try:
            while True:
                message = input()
                if message.lower() == "exit":
                    break
                client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            pass
        finally:
            client_socket.close()

if __name__ == "__main__":
    client = ChatClient('127.0.0.1', 5555)
    client.start()

