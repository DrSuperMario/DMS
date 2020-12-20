import socket


HOST = '127.0.0.1'
PORT = 30548

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'HELLOW WORLD')
    data = s.recv(1024)

print('recived ', repr(data))