import socketserver
import time
# sample server project 
class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        #self.wfile.write(self.data.upper())
        #self.wfile.write("Test")
        for x in range(0,10000):
            print(x*x)
        
        self.request.sendall(self.data.upper())
        print("send {}", self.data.upper())
        
        while True:
            self.request.sendall(bytes(time.strftime("%d.%m.%Y %H:%M:%S"),"utf-8"))
            print(time.strftime("%d.%m.%Y %H:%M:%S"))
            time.sleep(1)
    


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()