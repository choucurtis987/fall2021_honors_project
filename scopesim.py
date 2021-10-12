# Python 3 server example
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import time
import os
import random

hostName = "localhost"
serverPort = 5022

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.wav = []
    
        with open('/Users/choucurtis987/Desktop/honors_project_fall_2021/curve.dat') as ff:
            for line in ff: # read rest of lines
                self.wav.append(int(line))
        sc = random.uniform(0.5,1.5)
        msg = ''
        for sample in self.wav:
            msg = msg + str(int(sample*sc))
            msg = msg + ','
        msg = msg[:-1] + '\n'
        time.sleep(1.0)
        print(msg)
        self.send_response(200,message=None)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(msg, "utf-8"))

if __name__ == "__main__":
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
