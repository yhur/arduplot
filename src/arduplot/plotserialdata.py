#!/usr/bin/env python3
# Copyright (c) <year> <copyright holders>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import signal
import json
import socket
import click
from serial.serialutil import SerialException
try:
    from platformio.project.config import ProjectConfig
    piomode = True
except ImportError:
    piomode = False

# Handle Ctrl-C
def sighandler(signum, frame):
    exit(9)
signal.signal(signal.SIGINT, sighandler)

# utility function to get the plotter configuration setting
def valueByKey(j, key, value):
    if key in j:
        return j[key]
    else:
        return value

# BEGIN MAIN FUNCTION
@click.command()
@click.option("--width", "-w", type=int, help="Plotter Width")
@click.option("--title", "-t",  help="Plotter Title")
@click.option("--socket", "-s", type=int, help="TCP Socket Port number")
@click.option("--port", "-p", help="Serial Port, a number or a device name")
@click.option("--baud", "-b", type=int, help="Set baudrate, default=115200")
@click.argument("labels", nargs=-1)
def main(**kwargs):
    # Reading data function from the Serial Port
    def uart_in():
        return ser.readline()

    # Reading data function from the TCP socket
    def tcp_in():
        return client_socket.recv(1024)

    # Callback function for plotting the data by animation.FuncAnimation
    def animate(self):
        ax.clear()
        line = getInput().split()
        # data labelling
        if len(line) > len(data_label):             
            i = len(line) - len(data_label)
            j = 0
            while i > j:
                data_label.append('data' + str(j + 1))
                j = j + 1
    
        # data array preparation
        k = 0
        for d in line:
            try:
                d = float(d)
            except ValueError:
                print("Can't convert {} to float. it's zeroed out".format(d))
                d = float(0)
            if len(data) <= k:
                data.append([])
            data[k].append(d)
            data[k] = data[k][-width:]              # truncate to the graph width
            ax.plot(data[k], label=data_label[k])
            k = k + 1
    
        # plotting
        plt.title(title)
        plt.xticks(rotation=90, ha='right')
        plt.legend()
        plt.axis([0, width, 0, None])
        plt.grid(color='gray', linestyle='dotted', linewidth=1)
        fig.tight_layout(pad=2.5)

    # main control
    # main variabls
    data = []
    width = 50
    title = 'Serial Data Plot'
    data_label = []
    tcp_socket = kwargs['socket'] or None

    # check and get the plotter config if the config file exists
    try:
        with open('plotcfg.json') as jfile:
            plot_cfg = json.load(jfile)
        title = valueByKey(plot_cfg, 'title', title)
        width = valueByKey(plot_cfg, 'width', width)
        data_label = valueByKey(plot_cfg, 'label', data_label)
    except FileNotFoundError:
        pass
    title = kwargs['title'] or title
    width = kwargs['width'] or width
    data_label = list(kwargs['labels']) or data_label
    
    if tcp_socket:
        getInput = tcp_in
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', tcp_socket))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
    else:
        getInput = uart_in
        ser = serial.Serial()
        ser.timeout = 10
        ser.port = None
        ser.baudrate = 115200
        if piomode:
            if os.path.isfile(ProjectConfig.get_default_path()):
                config = ProjectConfig.get_instance()  # PIO project config
                for s in config.sections():
                    ser.port = config.get(s, 'monitor_port') or ser.port
                    ser.baudrate = config.get(s, 'monitor_speed') or ser.baudrate
            ser.port = kwargs['port'] or ser.port
            ser.baudrate = kwargs['baud'] or ser.baudrate
            if ser.port == None:
                print("Please check the platformio.ini for the 'monitor_port or the -p option")
                exit(2)
        else:
            ser.baudrate = kwargs['baud'] or ser.baudrate
            ser.port = kwargs['port']
        if not ser.port:
            print('\nPlease provide the serial port information\n')
            print('\t arduplot -p /dev/cu.usbserail-ABCDEEF or arduplot -p COM3\n')
            exit(3)
        try:
            ser.open()
            if ser.is_open==True:
        	    print('\nSerial port listening:')
        	    print('\tport: {}, baud: {}\n'.format(ser.port, ser.baudrate))
        except serial.serialutil.SerialException:
            print('Serial Device {} is not found'.format(ser.port))
            exit(4)

    fig = plt.figure()
    if not tcp_socket:
        fig.canvas.manager.set_window_title(ser.port)
    else:
        fig.canvas.manager.set_window_title('tcp://localhost:'+str(tcp_socket))
    ax = fig.subplots()
    ani = animation.FuncAnimation(fig, animate,  interval=1000)
    plt.show()
# END MAIN FUNCTION

if __name__ == '__main__':
    main()