from tkinter import *
from tkinter import ttk
from vidstream import CameraClient
from vidstream import StreamingServer
from audiostream import AudioReceiverClient
from audiostream import AudioSendingClient
import threading
import logging
import tkinter as tk
import socket
import time

ip___ = socket.gethostname()
ip__ = socket.gethostbyname(ip___)

receive, sending, receive_audio, sending_audio = '', '', '', ''


def connect_(y_ip, o_ip, y_port, o_port):
    global receive, sending, receive_audio, sending_audio

    if y_ip == '' or o_ip == '' or y_port == '' or o_port == '':
        logging.debug("  A field is empty, this might cause an error")
        label_.config(text="A field is empty, this might cause an error")
        return -1

    y_port = int(y_port)
    o_port = int(o_port)

    # for video
    receive = StreamingServer(y_ip, y_port)
    sending = CameraClient(o_ip, o_port)

    # for audio
    receive_audio = AudioReceiverClient(y_ip, y_port + 1)
    sending_audio = AudioSendingClient(o_ip, o_port + 1)

    try:
        t1 = threading.Thread(target=receive.start_server)
        t1.start()

        t3 = threading.Thread(target=receive_audio.begin_server)
        t3.start()

        t2 = threading.Thread(target=sending.start_stream)
        t2.start()

        t4 = threading.Thread(target=sending_audio.begin_server)
        t4.start()

        time.sleep(3)

        print("Connected!")
        label_.config(text="Connected!")

        connect.config(state='disable')
        disconnect_.config(state='normal')
    except Exception as e:
        logging.info(f"  this error occurred {str(e)}, try again")
        label_.config(text=f"this error occurred {str(e)}, try again")


def disconnect():
    global receive, sending, receive_audio, sending_audio

    receive.stop_server()
    sending.stop_stream()
    receive_audio.end_server()
    sending_audio.end_server()

    connect.config(state='normal')
    disconnect_.config(state='disable')


root = tk.Tk()
root.geometry('500x500')
root.resizable(False, False)
root.title('Zoom clone')

Label(root, text="Zoom clone", font=('Arial', 14, 'normal')).place(x=30, y=20)

Label(root, text='Your ip address:').place(x=40, y=80)
Label(root, text='Port:').place(x=200, y=80)

your_ip = Entry(root)
your_ip.place(x=40, y=110, height=30)

your_port = Entry(root, width=7)
your_port.place(x=200, y=110, height=30)

Label(root, text='Receivers ip address:').place(x=40, y=190)
Label(root, text='Receivers Port:').place(x=200, y=190)

other_ip = Entry(root)
other_ip.place(x=40, y=220, height=30)

other_port = Entry(root, width=7)
other_port.place(x=200, y=220, height=30)

ip = your_ip.get()
ip_ = other_ip.get()
port = your_port.get()
port_ = other_port.get()

your_ip.insert(0, ip__)

connect = Button(root, text='Connect', width=12, height=2, command=lambda: connect_(your_ip.get(), other_ip.get(), your_port.get(), other_port.get()))
connect.place(x=40, y=300)

disconnect_ = Button(root, text='Disconnect', width=12, height=2, command=disconnect, state='disabled')
disconnect_.place(x=160, y=300)

label_ = ttk.Label(root, text='')
label_.place(x=40, y=360)

root.mainloop()
