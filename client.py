import socket


_host = "127.0.0.1"
_port = 5001



def send_ping(host=_host, port=_port):
    server_addr = (host, port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    try:
        sock.connect(server_addr)
        message = "Keepalive"
        sock.send(message.encode())
        sock.close()
    except ConnectionRefusedError:
        logging.error("DMS failed , connection refused")    
    
if __name__=="__main__":
    send_ping()
