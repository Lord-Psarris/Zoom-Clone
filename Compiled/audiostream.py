import socket
import pyaudio
import logging

logging.basicConfig(level=logging.DEBUG)


class AudioReceiverClient:

    def __init__(self, host_name, port):
        self.host = host_name
        self.port = port

        self.record = pyaudio.PyAudio()
        chunk = 1024 * 4
        format_ = pyaudio.paInt16
        channels = 2
        rate = 44100

        self.stream = self.record.open(
            format=format_,
            channels=channels,
            rate=rate,
            output=True,
            frames_per_buffer=chunk)

    def begin_server(self):
        with socket.socket() as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            connection, address = server_socket.accept()
            logging.info(" Connection from " + address[0] + ":" + str(address[1]))
            data = connection.recv(4096)

            while data != "":
                try:
                    data = connection.recv(4096)
                    self.stream.write(data)
                except socket.error:
                    logging.info(" Client Disconnected")
                    break
                except Exception as e:
                    logging.error(f" this error occurred: {e}")
                    break

    def end_server(self):
        self.stream.stop_stream()
        self.stream.close()
        self.record.terminate()

# '192.168.43.142'
class AudioSendingClient:

    def __init__(self, host_name, port):
        self.host = host_name
        self.port = port
        self.while_ = True

        self.record = pyaudio.PyAudio()
        self.chunk = 1024 * 4
        format_ = pyaudio.paInt16
        channels = 1
        rate = 44100
        record_seconds = 3
        wave_output_name = "output.wav"
        self.stream = self.record.open(format=format_,
                                       channels=channels,
                                       rate=rate,
                                       input=True,
                                       frames_per_buffer=self.chunk)

    def begin_server(self):
        with socket.socket() as client_socket:
            client_socket.connect((self.host, self.port))
            while self.while_:
                try:
                    data = self.stream.read(self.chunk)
                    client_socket.send(data)
                except ConnectionResetError:
                    logging.info(" Connection forcibly disconnected")
                except Exception as e:
                    logging.error(f" This error occurred: {e}")

    def end_server(self):
        self.while_ = False
