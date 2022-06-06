import threading
import socket
import select
import pickle

PORT = 2707
SERVER_ADDRESS = "127.0.0.1"
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

server_address = (SERVER_ADDRESS, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_sockets = [server_socket]
client_sockets = []
client_names = []

def accept_clients(server_socket):
    while True:
        if len(client_sockets) < 2:
            client_socket, client_address = server_socket.accept()
            client_sockets.append(client_socket)
            input_sockets.append(client_socket)
            print(f"{client_address} connection established!")
            
            threading._start_new_thread(handle_connection, (client_socket, client_address))

def handle_connection(client_socket, client_address):
    msg1 = {
        "opponent": None,
        "symbol": None
    }
    
    msg2 = {
        "opponent": None,
        "symbol": None
    }
        
    client_name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    client_names.append(client_name)
    
    print(f"Client Lists:\n{client_names}")
    
    if len(client_names) > 1:
        symbols = ["X", "O"]
        
        msg1['opponent']= client_names[1]
        msg1['symbol']= symbols[0]
            
        msg2['opponent']= client_names[0]
        msg2['symbol']= symbols[1]
        
        p1 = pickle.dumps(msg1)
        p2 = pickle.dumps(msg2)
        
        client_sockets[0].send(p1)
        client_sockets[1].send(p2)
    
    while True:
        
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        
        if client_socket == client_sockets[0]:
            client_sockets[1].send(data)
            
        else:
            client_sockets[0].send(data)
    
    client_sockets.remove(client_socket)
    input_sockets.remove(client_socket)
    client_names.remove(client_name)
    
    client_socket.close()
    print(f"Game Over, {client_address} disconnected!")
    print(f"Client Lists:\n{client_names}")

while True:
    read_ready, write_ready, exception = select.select(input_sockets, [], [])
    
    for sock in read_ready:
        if sock == server_socket and len(client_sockets) < 2:
            threading._start_new_thread(accept_clients, (server_socket,))
        