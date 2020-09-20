from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    """
    FOR COMMUNICATION TO SERVER
    """

    HOST = "192.168.0.136"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512


    def __init__(self, name):
        """
        INIT OBJECT, SEND NAME TO SERVER
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()


    def receive_message(self):
        """
        RECEIVE MESSAGES FROM SERVER
        """
        while  True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break


    def send_message(self, msg):
        """
        SEND MESSAGE TO SERVER
        """
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)


    def get_messages(self):
        """
        RETURN STR MESSAGES
        """
        messages_copy = self.messages[:]

        # Make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy


    def disconnect(self):
        self.send_message("{quit}")