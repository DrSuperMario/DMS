import sys
import socket
import selectors
import types
import time
import os
from datetime import datetime
from smtp import send_email

sel = selectors.DefaultSelector()


_timelapsed_start = time.time()
_host = ''#socket.gethostname()
_port = 5001
_LOOP_TIME = 10
PASSWD = "<BLANK>"

def execute_func():
    send_email(messages='DEAD MAN SWITCH ACTIVATED', 
                    subject=f"DMS active at {str(datetime.now())}", password=PASSWD)
    os.system("echo 'hello world'")


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
lsock.listen(2)
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

            toolbar_width = int(_timelapsed+1)

            # setup toolbar
            sys.stdout.write(f"Waiting connection: {int(_timelapsed)}s "+"[%s]" % (" " * toolbar_width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
            sys.stdout.flush()
          

            for i in range(toolbar_width+1):
                sys.stdout.flush()
                time.sleep(0.1) # do real work here
                # update the bar
                sys.stdout.write("#")
                sys.stdout.flush()
                

            sys.stdout.write("]\n") # this ends the progress bar
            os.system('cls')
        
                
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()