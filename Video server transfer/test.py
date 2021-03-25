from vidstream import CameraClient
from vidstream import StreamingServer

import threading
import time
import socket

HOST = socket.gethostname()

receive = StreamingServer(HOST, 9999)
sending = CameraClient(HOST, 9999)

t1 = threading.Thread(target=receive.start_server)
t1.start()

time.sleep(2)

t2 = threading.Thread(target=sending.start_stream)
t2.start()

while input('') != "STOP":
    continue

receive.stop_server()
sending.stop_stream()
