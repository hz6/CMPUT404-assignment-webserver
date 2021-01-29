#  coding: utf-8
import socketserver
import socket
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        pld = self.data.decode()

        if (pld == None):
            self.request.send("HTTP/1.1 400 Bad Request \n")
        else:
            # pld_data = pld.split()
            (http_method, path) = (pld.split()[0], pld.split()[1])

            if http_method != "GET":  # Only GET Method is allowed
                self.request.send(
                    "HTTP/1.1 405 Method Not Allowed \n".encode())
            else:
                if os.path.realpath(os.getcwd() + '/www' + path).startswith(os.getcwd() + '/www'):
                    if os.path.exists("./www" + path + "/index.html") and path.endswith('/'):
                        path = path + "index.html"
                        body = open("./www" + path, 'r').read()
                        if body:
                            self.request.send("HTTP/1.1 200 OK \n".encode())
                            self.request.send(
                                "Content-type: text/html \n".encode())
                            self.request.sendall(body.encode())
                        else:
                            self.request.send(
                                "HTTP/1.1 404 Not Found".encode())
                    elif os.path.exists("./www" + path) and path.endswith(".html"):
                        body = open("./www"+path, 'r').read()
                        self.request.send("HTTP/1.1 200 OK \n".encode())
                        self.request.send(
                            "Content-type: text/html \n".encode())
                        self.request.sendall(body.encode())

                    elif os.path.exists("./www" + path) and path.endswith(".css"):
                        body = open("./www" + path, 'r').read()
                        self.request.send("HTTP/1.1 200 OK\r\n".encode())
                        self.request.send(
                            "Content-type: text/css \n".encode())
                        self.request.sendall(body.encode())
                    else:
                        try:
                            body = open('./www' + path +
                                        '/index.html', 'r').read()
                            self.request.send(
                                "HTTP/1.1 301 Moved Permanently \n".encode())
                            self.request.send(
                                "Content-type: text/html \n".encode())
                            self.request.sendall(
                                "http://127.0.0.1:8080" + path + "/".encode())
                        except:
                            self.request.send(
                                "HTTP/1.1 404 Not Found \n".encode())
                else:
                    self.request.send(
                        "HTTP/1.1 404 Not Found \n".encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
