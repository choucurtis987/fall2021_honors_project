# Python 3 server example
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import time

import random
import numpy as np
import ROOT

wavfit = ROOT.TF1('wavfit','0.5*[0]*TMath::Erfc((10.0-x)/[4])*TMath::Exp((x-10.0)/-[3]) - 0.5*[1]*TMath::Erfc((81.9-x)/[5])*TMath::Exp((x-10.0)/-[3])+[2]')

hostName = "localhost"
serverPort = 5022
t_wall = 0.0
ct = 0
event = 0

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        global t_wall
        global ct
        global event
        if self.path.find('curve?') >= 0 :
            self.wav = []
            event = event + 1
            with open('curve.dat') as ff:
                for line in ff: # read rest of lines
                    val = int(line)
                    val = val*256
                    val = val + random.randint(-127,127)
                    self.wav.append(val)
            sc = random.randint(-1,1)
            msg = ''
            lifetime = 415.5
            deltaT = 81.9 - 10.0
            exparg = deltaT/lifetime
            downstroke = np.exp(-exparg)*46.685
            wavfit.SetParameter(0,46.685)
            wavfit.SetParameter(1,downstroke)
            wavfit.SetParameter(2,40.235)
            wavfit.FixParameter(3,395.3)
            wavfit.FixParameter(4,1.0)
            wavfit.FixParameter(5,2.9)
            pre = '2;16;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";3.125E-6;0.0E0;-1.3824E4;"V"\n'
            t = [ 1.0e6*(float(pre.split(';')[8])*float(i)+float(pre.split(';')[10])) for i in range(0,500) ]
            for t_i in t:
                t_wall = t_wall + 8.0e-7
                bl = int(16384.0*np.sin(2*np.pi*2500.0*t_wall - ct*np.pi*0.75 ))
                millivolt = wavfit.Eval( t_i )
                dl = float(wfmpre.split(';')[14]) + (millivolt/1.0e3 - float(wfmpre.split(';')[13]))/float(wfmpre.split(';')[12])
                dl = int(dl) + random.randint(-127,127)
                msg = msg + str(dl*(ct%2))
                msg = msg + ','
            ct = ct + 1
            msg = msg[:-1] + '\n'
            print(msg)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(msg, "utf-8"))
        if self.path.find('wfmpre?') >= 0 :
            #msg = '2;16;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";8.0E-4;0.0E0;-5.4E1;"V"\n'
            msg = '2;16;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";3.125E-6;0.0E0;-1.3824E4;"V"\n'
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(msg, "utf-8"))

        time.sleep(1.0)

if __name__ == "__main__":        
    webServer = ThreadingHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


