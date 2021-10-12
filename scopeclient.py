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
        while True :
            #self.cli_sock.send('???\n'.encode())
            c=''
            data = ''
            # while c != '\n' :
            #     c = self.cli_sock.recv(1).decode()
            #     data = data + c
            f = urllib.request.urlopen('http://localhost:5022/?COMMAND=curve?')
            data = f.read().decode()
            print('received '+data)
            wfm = [ float(u) for u in data.split(',') ]
            # find max and min in first half of wfm
            peak = np.max(wfm) - np.min(wfm)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.xar.append((time.time() - start_time) / 3600.0)
            self.yar.append(peak)

            if len(self.xar) > 5000:
                self.xar.pop(0)
                self.yar.pop(0)
            plt.clf()

            plt.plot(self.xar, self.yar,'r-')
            plt.title("Amplitude vs Time")
            plt.ylabel('Counts')
            plt.xlabel('Sample')

            self.plot_widget.grid(row=0, column=0)

            self.fig.canvas.draw_idle() # SEEMS TO BE BUG HERE

            #toolbar.update()

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
        plt.subplot(111)
#plot1.plot(xar, yar, 'ro-')
        self.fig.text(0.5,0.04,'Time (Hours)',ha ='center',va = 'center')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0)
        self.curve = '-51,-51,-50,-50,-50,-50,-50,-50,-50,-50,-50,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-47,-48,-48,-48,-47,-47,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-50,-50,-50,-50,-50,-50,-50,-50,-50,-50,-51,-51,-51,-51,-51,-51,-51,-51,-51,-51,-51,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-52,-53,-53,-53,-53,-53,-53,-53,-53,-53,-53,-53,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-54,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-56,-55,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-57,-56,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-57,-56,-57,-57,-57,-57,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-56,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-55,-54,-55,-54,-55,-55,-54\n'

        self.fig.canvas.draw()

        self.plotter = threading.Thread(target=self.plotit)

        self.plotter.start()
        self.window.mainloop()

appl = grafit()
