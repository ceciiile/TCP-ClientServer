# TCP-ClientServer
Implementation of a TCP client and server for a netwoking course in UNIST university (2020). The client can retrieve files from a remote server as well as from my own server.


## Launching Client app
**For connecting to a remote server**
```
sudo python3 webclient.py <requestedObject> –p <portNumber>
```
> Example: sudo python3 webclient.py www.google.com/test.html –p 80


**For connecting to my server**

Simply include the path to the desired resource. The path should begin with './' and be located in the folder indicated when launching server app (for example ./web directory).

```
sudo python3 webclient.py ./requestedObject-p portNumber
```
> Example: sudo python3 webclient.py ./test_image.jpg -p 80



## Launching Server app
The server can only send files in the directory passed as last argument.

```
sudo python3 webserver.py -p portNumber -d filesDirectory
```
> Example: sudo python3 webserver.py -p 80 -d ./web


The server can answer requests from both my own client and a web browser (with a command like this: http://192.168.0.115/test_file.txt). It also stays available after treating a request, however after treating request from a web browser, it cannot handle requests from anyone else, so for testing my server with different clients, please close it and launch it again.
