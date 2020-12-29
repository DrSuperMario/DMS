import socket


_host = "165.227.149.157"
_port = 5001


def start_conn(host, port):
    server_addr = (host, port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    sock.connect(server_addr)
    message = "Keepalive"
    sock.send(message.encode())
    sock.close()
    

if __name__=="__main___":
    start_conn(_host, _port)
