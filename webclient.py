#!/usr/bin/python

import sys
import socket


PORT=''
SERVER_IP=''
BUFFER_SIZE= 1024

def get_hostName(URL):
    # Extract host name of a server based on the URL
    # returns: host name

    # Parse "https"
    first_part = URL.split("www")
    if first_part[0]:
        URL = 'www' + first_part[1]

    # Parse ".com"
    second_part = URL.split(".com")
    URL = second_part[0] + '.com'
    return(URL)


def get_dataPath(URL):
    # Returns the path to the requested ressouce (without host name)

    data_path = URL.split(get_hostName(URL))[1]
    if not data_path:
        return("\\")
    return data_path


def get_serverIP(hostName):
    # Try to get server IP until it works

    # Sometimes if the server is busy, getting IP needs few attemps
    # (found experimentally that it helped)

    SERVER_IP=''
    try:
        SERVER_IP = socket.gethostbyname(hostName)
    except:
        get_serverIP(hostName)
    return SERVER_IP


def complete_URL(URL):
    # Completes an URL if it misses "https://" or "www"
    # return: a comlete url

    httpsTest = URL.split('https')[0]
    if httpsTest == URL:
        URL = 'https://'+URL

    wwwTest = URL.split("www")[0]
    if wwwTest == URL:
        URL = 'https://www.' + URL.split('https://')[1]
    return(URL)


if __name__ == '__main__':

    # Check if arguments passed are correct
    try:
        server_URL = str(sys.argv[1])
    except:
            print("Missing an argument")
            print("Execution command is: python3 webclient.py requestedObject -p portNumber")
            exit()
    try:
        PORT = int(sys.argv[3])
    except:
        print("Missing an argument")
        print("Execution command is: python3 webclient.py requestedObject -p portNumber")
        exit()

    # For connecting to server in the same device
    if server_URL.find('https://') == -1 and server_URL.find('www.') == -1 and server_URL.find('.com') == -1:
        res = server_URL.split('./')
        dataPath = '/' + res[1]
        hostName = ''
        SERVER_IP = "0.0.0.0"

    # For connecting to remote server
    else:
        server_URL = complete_URL(server_URL)

        hostName = get_hostName(server_URL)
        dataPath = get_dataPath(server_URL)
        SERVER_IP = get_serverIP(hostName)
    print("Connecting to IP: ", SERVER_IP)

    # Connecting to the socket
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.connect((SERVER_IP, PORT))

    message = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(dataPath, hostName)

    # Sending the GET request
    TCP_socket.send(message.encode())
    print("--- CLIENT REQUEST ---")
    print(message)


    # Receiving response from the server
    print("--- SERVER RESPONSE ---")
    while True:
        response = TCP_socket.recv(BUFFER_SIZE)
        if not response or response==b'end':
            exit()
        print(response)
