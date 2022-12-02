from  datetime import datetime
import json
import socket 
import base64
from typing import List

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("0.0.0.0", 9990))
listener.listen(0)
print("[+] Waiting for incoming connections")
cl_socket, remote_address = listener.accept()
print(f"[+] Got a connection from {remote_address} ")

try:

    while True:
        command :str = input(">> ")

        if "upload" in command:
            # upload test/test1.txt test/test2.txt
            
            _, path_on_server, path_on_client = command.split(' ')
            with open(path_on_server, 'rb') as file:
                data = file.read()
            data = base64.b64encode(data)

            command = "upload " + path_on_client + " " + str(len(data)) + " "
            cl_socket.send(command.encode() + data)
            
            response = cl_socket.recv(1024).decode()
            print(response)

        elif "download" in command:
            # download test/test1.jpg test/test2.jpg

            _, path_on_client, path_on_server = command.split(' ')
            command = "download " + path_on_client
            cl_socket.send(command.encode())

            response = cl_socket.recv(1024).decode()
            full_size, data = response.split(' ')

            while len(data) != int(full_size):
                data = data + cl_socket.recv(1024).decode()
            data = base64.b64decode(data)
            
            with open(path_on_server, "wb") as file:
                file.write(data)

            _, file = path_on_server.split("/")
            print(f"File {file} is downloaded")

        else:
            cl_socket.send(command.encode())
            response = cl_socket.recv(1024).decode()
            print(response)
        
except KeyboardInterrupt:
    listener.close()
    exit()