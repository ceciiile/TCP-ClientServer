#!/usr/bin/python

import sys
import socket
import time


IP_ADDRESS = "0.0.0.0"
PORT=''
BUFFER_SIZE= 1024
BLOCK_SIZE=1000

def send_fileClient(conn, file):
    # Handle the data sending to the client
    # returns: nothing

    print("Sending file...")
    file_content=file.read()
    file_size=len(file_content)
    nb_packet=int(file_size/BLOCK_SIZE)+1;

    # Sending header
    header = "HTTP/1.1 200 OK\r\nContent-Length:{}\r\nConnection: close\r\n\r\n".format(file_size)
    conn.send(header.encode())

    # Sending data
    for i in range(0, nb_packet):
        datatoSend = file_content[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
        conn.send(datatoSend)
    print("Finished sending file.")
    print("")

    # Optionnal message: when sending to my client
    # string "end" will close the connection
    time.sleep(0.1)
    conn.send("end".encode())

    return 0


if __name__ == '__main__':

    # Check if arguments passed are correct
    try:
        PORT = int(sys.argv[2])
    except:
        print("Missing an argument")
        print("Execution command is: sudo python3 webserver.py -p portNumber -d filesDirectory")
        exit()

    try:
        object_path = str(sys.argv[4])
    except:
        print("Missing an argument")
        print("Execution command is: sudo python3 webserver.py -p portNumber  -d filesDirectory")
        exit()


    #Open a socket
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.bind((IP_ADDRESS, PORT))
    TCP_socket.listen()
    print("Listening on port:", PORT)
    while True:
        conn,addr = TCP_socket.accept()


        # Handle first message (GET request)
        message = conn.recv(BUFFER_SIZE).decode()
        if message:
            print("--- CLIENT REQUEST ---")
            
            # Extract path to requested object
            ressourcePath = str(object_path+message.split(' ')[1])
            print("Requested ressource:", ressourcePath)

            try:
                file = open(ressourcePath, "rb")
            except:

                # If the server doesn't have the file
                message = "HTTP/1.1 404 Not Found\r\n"
                conn.send(message.encode())
                conn.send("end".encode())
            else:

                # If the file is available
                send_fileClient(conn, file)
