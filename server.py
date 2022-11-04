# network connection
import socket
# performing various tasks
import threading

# host ip
host = '127.0.0.1'
# port number
port = 5006

# starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# list of users
clients = []
names = []



# send messages for all users in the server
def translate(msg):
    for client in clients:

        # name = client.recv(1024).decode()
        # if msg.startswith('/private'):
        #     msgSplit = msg.split()
        #     if msgSplit[1] == name:
        #         client.send(msg)
        #         break
        client.send(msg)


def process(client):
    while True:
        try:
            msg = client.recv(1024)
            translate(msg)
        except:
            # remove and close users
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            translate(f"{name} left!".encode())
            names.remove(name)
            break


def receive():
    while True:

        client, addr = server.accept()
        print(f"Connected to host {str(addr[0])} and port {str(addr[1])}")
        client.send('START'.encode())
        name = client.recv(1024).decode()
        names.append(name)
        clients.append(client)
        print(f"Username is {name}")
        translate(f"{name} joined!".encode())
        client.send('Connected to server'.encode())

        thread = threading.Thread(target=process, args=(client,))
        thread.start()


receive()

