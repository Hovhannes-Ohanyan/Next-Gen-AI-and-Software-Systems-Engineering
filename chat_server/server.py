import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.lock = threading.Lock()

    def handle_client(self, client_socket, client_address):
        with self.lock:
            self.clients.append(client_socket)
        
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                with self.lock:
                    for client in self.clients:
                        if client != client_socket:
                            client.send(message.encode('utf-8'))
        except:
            pass
        
        with self.lock:
            self.clients.remove(client_socket)
        client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Chat Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except KeyboardInterrupt:
            print("Chat Server stopped.")
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = ChatServer('127.0.0.1', 5555)
    server.start()

