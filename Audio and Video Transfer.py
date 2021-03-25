from Compiled import audiostream
from vidstream import CameraClient
from vidstream import StreamingServer
import threading
import time
import socket

HOST = socket.gethostname()

receive = StreamingServer(HOST, 7777)
sending = CameraClient(HOST, 7777)
receive_audio = audiostream.AudioReceiverClient(HOST, 8888)
sending_audio = audiostream.AudioSendingClient(HOST, 8888)

t1 = threading.Thread(target=receive.start_server)
t1.start()

t3 = threading.Thread(target=receive_audio.begin_server)
t3.start()

time.sleep(2)

t2 = threading.Thread(target=sending.start_stream)
t2.start()

t4 = threading.Thread(target=sending_audio.begin_server)
t4.start()

while input('') != "STOP":
    continue

receive.stop_server()
sending.stop_stream()
receive_audio.end_server()
sending_audio.end_server()
