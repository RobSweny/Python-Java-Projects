from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = "192.168.0.136"
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
# The receive socket buffer size determines the maximum receive window for a TCP connection
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # SET UP SERVER


def broadcast(msg, name):
    """
    SEND NEW MESSAGES TO ALL CLIENTS
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(person):
    """
    THREAD TO HANDLE ALL MESSAGES FROM CLIENT
    """
    client = person.client

    # GET PERSONS NAME
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "") # BROADCAST WELCOME MESSAGE

    while True: # WAIT FOR ANY MESSAGES FROM ANY PERSON
       msg = client.recv(BUFSIZ)
       
       if msg == bytes("{quit}", "utf8"):  # IF MESSAGE IS QUIT, THEN DISCONNECT
           client.close()
           persons.remove(person)
           broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
           print(f"[DISCONNECTED] {name} disconnected")
           break
       else:  # OTHERWISE SEND MESSAGES TO ALL OTHER CLIENTS
           broadcast(msg, name+": ")
           print(f"{name}: ", msg.decode("utf8"))


def wait_for_connection():
    """
    WAIT FOR CONNECTION FROM NEW CLIENTS,
    START NEW THREAD ONCE CONNECTED
    """
    while True:
        try:
            client, addr = SERVER.accept()  # WAIT FOR ANY NEW CONNECTIONS
            person = Person(addr, client)  # CREATE NEW PERSON FOR CONNECTION
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # LISTEN FOR CONNECTIONS
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()



