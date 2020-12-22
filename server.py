import sys
import socket
import selectors
import types
import time

sel = selectors.DefaultSelector()


_timelapsed_start = time.time()
_host = "127.0.0.1"
_port = 65432
_LOOP_TIME = 10

def execute_func():
    print("Do something")


def accept(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

#open connection to TCP/IPv4
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((_host, _port))
lsock.listen()
print("listening on", (_host, _port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:

        events = sel.select(timeout=None)
        _timelapsed = time.time() - _timelapsed_start


        for key, mask in events:

            if key.data is None:
                _timelapsed_start = time.time()
                _timelapsed = time.time() - _timelapsed_start
                accept(key.fileobj)
    
            else:
                while _timelapsed > _LOOP_TIME:
                    if(key.data is None):
                        continue
                    break
            if(_timelapsed > _LOOP_TIME + 1):
                execute_func()
                sys.exit(1)    

            print(_timelapsed)

        
                
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()