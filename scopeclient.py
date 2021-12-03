from tkinter import *
import socket, threading
import time
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import urllib.request

class grafit(Frame):
    def plotit(self):
        start_time = time.time()
        # SAVING TO CSV:
        # wfm_path = 'Users/choucurtis987/Desktop/fall2021_honors_project/wfm.txt'
        # wfm_file = open(wfm_path, "w")
        while True:
            #self.cli_sock.send('???\n'.encode())
            c=''
            data = ''
            # while c != '\n' :
            #     c = self.cli_sock.recv(1).decode()
            #     data = data + c
            f = urllib.request.urlopen('http://localhost:5022/?COMMAND=curve?')
            data = f.read().decode()
            print('received '+data)
            # SAVING TO CSV:
            # wfm_file.write(data + "\n")
            wfm = [ float(u) for u in data.split(',') ]
            # print(len(wfm))

            # CALLING WFMPRE TO CONVERT WFM TO MS AND VOLTS
            f2 = urllib.request.urlopen('http://localhost:5022/?COMMAND=wfmpre?')
            wfmpre = f2.read().decode()
            print(wfmpre)
            #wfmpre = '1;8;ASC;RP;MSB;500;"Ch1, AC coupling, 2.0E-2 V/div, 4.0E-5 s/div, 500 points, Average mode";Y;8.0E-7;0;-1.2E-4;"s";8.0E-4;0.0E0;-5.4E1;"V"'
            t = [ 1.0e6*(float(wfmpre.split(';')[8])*float(i)+float(wfmpre.split(';')[10])) for i in range(0,len(wfm)) ]
            volt = [ 1.0e3*(( (dl/256) - float(wfmpre.split(';')[14]) )*float(wfmpre.split(';')[12]) - float(wfmpre.split(';')[13])) for dl in wfm ]

            # print(f"t: {len(t)}")
            # print(f"volt: {len(volt)}")

            # find size of half of volt:
            half = int( len(volt) / 2 )
            # take max of (50 to half(volt)) and substract with min of 50 points before half(volt):
            # we want 50 to half(volt) because max is at times in the beginning
            # we want 50 points before half(volt) because the change should be so rapid that in the
            # previous 50 points, there should be a min where the waveform shoots up after
            peak = np.max(volt[50:half]) - np.min(volt[half-50:half])
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.xar.append((time.time() - start_time))
            self.yar.append(peak)

            if len(self.xar) > 5000:
                self.xar.pop(0)
                self.yar.pop(0)
            plt.clf()

            # PLOTTTING PEAKS:
            plt.subplot(211)
            plt.plot(self.xar, self.yar,'ro-')
            plt.title("Amplitude vs Time")
            plt.ylabel('Counts')
            plt.xlabel('Sample')

            # PLOTTING WAVEFORM:
            plt.subplot(212)
            plt.plot(t,volt,'ro-', color='green')
            plt.title("Most recent waveform")
            plt.ylabel("Volts")
            plt.xlabel(u"Time (\u03bcs)")

            plt.subplots_adjust(hspace=0.6, wspace=0.6)
            self.plot_widget.grid(row=0, column=0, rowspan=2)

            # plt.plot(volt,t,'r-')
            # plt.title("Most recent waveform")
            # plt.ylabel("volts")
            # plt.xlabel("time (ms)")
            # self.plot_widget.grid(row=0, column=2)

            # WIDGET TO SEE MOST RECENT PEAK
            T = Text(self.window, height = 5, width = 5)
            peak = round(peak, 1)
            T.insert(END, peak)
            T.grid(row=0, column=1)


            self.fig.canvas.draw_idle()
            # toolbar.update()

            # originally 5:
            time.sleep(1.0)


    def __init__(self):
        self.cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = 'localhost'
        PORT = 5022

        self.xar = []
        self.yar = []
        self.cli_sock.connect((HOST,PORT))
        self.window = Tk()

        self.window.title('Remote data')
#window.geometry("500x500")
        self.fig = plt.figure(1)
        self.fig.text(0.5,0.04,'LOADING...',ha ='center',va = 'center')
        # plt.subplot(111)

#plot1.plot(xar, yar, 'ro-')
        # self.fig.text(0.5,0.04,'Time (Hours)',ha ='center',va = 'center')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0)
        self.curve = '-51,-51,-50,-50,-50,-50,-50,-50,-50,-50,-50,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-48,-48,-48,-47,-47,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-50,-50,-50,-50,-50,-50,-50,-50,-50,-50,-51,-51,-51,-51,-51,-51,-51,-51,-51,-51,-51,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-53,-53,-53,-53,-53,-53,-53,-53,-53,-53,-53,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-56,-55,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-57,-56,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-56,-57,-57,-57,-57,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-54,-55,-54,-55,-55,-54\n'

        self.fig.canvas.draw()

        self.plotter = threading.Thread(target=self.plotit)
        # self.plotter.setDaemon(True) # thread safe in client but not in server
        self.plotter.start()
        exit_button = Button(self.window, text="Exit", command=self.window.destroy)
        exit_button.grid(row=1, column=1)
        self.window.mainloop()

appl = grafit()
