import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

_host = "127.0.0.1"
_port = 65432
_num_conns=1


def start_conn(host, port, num_conns):
    server_addr = (host, port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = b"Keepalive"
    sel.register(sock, events, data=data)


start_conn(_host, int(_port), int(_num_conns))
