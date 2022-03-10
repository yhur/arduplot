#!/usr/bin/env python3
'''
 Copyright (c) <year> <copyright holders>

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

import os
import sys
import signal
import json
import socket
import matplotlib.pyplot as plt
from matplotlib import animation
import serial
import click
from serial.serialutil import SerialException
try:
    from platformio.project.config import ProjectConfig
    PIO_MODE = True
except ImportError:
    PIO_MODE = False

def sighandler(signum, frame):
    '''signal handler for Ctrl-C'''
    sys.exit(9)
signal.signal(signal.SIGINT, sighandler)

def value_by_key(j, key, value):
    '''utility function to get the plotter configuration setting'''
    if key in j:
        return j[key]
    return value

# BEGIN MAIN FUNCTION
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--width", "-w", type=int, help="Plotter Width")
@click.option("--ymin", "-i", type=int, help="Plotter Y axis Min")
@click.option("--ymax", "-x", type=int, help="Plotter Y axis Max")
@click.option("--title", "-t",  help="Plotter Title")
@click.option("--socket", "-s", type=int, help="TCP Socket Port number")
@click.option("--port", "-p", help="Serial Port, a number or a device name")
@click.option("--baud", "-b", type=int, help="Set baudrate, default=115200")
@click.argument("labels", nargs=-1)
def main(**kwargs):
    '''main function'''
    # Reading data function from the Serial Port
    def uart_in():
        return ser.readline()

    # Reading data function from the TCP socket
    def tcp_in():
        return client_socket.recv(1024)

    # Callback function for plotting the data by animation.FuncAnimation
    def animate(self):
        ax.clear()
        lines = get_input().split()
        # data labelling
        if len(lines) > len(data_label):
            i = len(lines) - len(data_label)
            j = 0
            while i > j:
                data_label.append('data' + str(j + 1))
                j = j + 1

        # data array preparation
        k = 0
        for l in lines:
            try:
                l = float(l)
            except ValueError:
                print(f"Can't convert {l} to float. it's zeroed out")
                l = float(0)
            if len(data) <= k:
                data.append([])
            data[k].append(l)
            data[k] = data[k][-width:]              # truncate to the graph width
            ax.plot(data[k], label=data_label[k])
            k = k + 1

        # plotting
        plt.title(title)
        plt.xticks(rotation=90, ha='right')
        plt.legend()
        plt.axis([0, width, ymin, ymax])
        plt.grid(color='gray', linestyle='dotted', linewidth=1)
        fig.tight_layout(pad=2.5)

    # main control
    # main variabls
    data = []
    width = 50
    ymin = None
    ymax = None
    title = 'Serial Data Plot'
    data_label = []
    tcp_socket = kwargs['socket'] or None

    # check and get the plotter config if the config file exists
    try:
        with open('plotcfg.json', 'r', encoding='utf-8') as jfile:
            plot_cfg = json.load(jfile)
        title = value_by_key(plot_cfg, 'title', title)
        width = value_by_key(plot_cfg, 'width', width)
        ymin = value_by_key(plot_cfg, 'ymin', ymin)
        ymax = value_by_key(plot_cfg, 'ymax', ymax)
        data_label = value_by_key(plot_cfg, 'label', data_label)
    except FileNotFoundError:
        pass
    title = kwargs['title'] or title
    width = kwargs['width'] or width
    ymin = kwargs['ymin'] or ymin
    ymax = kwargs['ymax'] or ymax
    data_label = list(kwargs['labels']) or data_label

    if tcp_socket:
        get_input = tcp_in
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', tcp_socket))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
    else:
        get_input = uart_in
        ser = serial.Serial()
        ser.timeout = 10
        ser.port = None
        ser.baudrate = 115200
        if PIO_MODE:
            if os.path.isfile(ProjectConfig.get_default_path()):
                config = ProjectConfig.get_instance()  # PIO project config
                for s in config.sections():
                    ser.port = config.get(s, 'monitor_port') or ser.port
                    ser.baudrate = config.get(s, 'monitor_speed') or ser.baudrate
            ser.port = kwargs['port'] or ser.port
            ser.baudrate = kwargs['baud'] or ser.baudrate
            if ser.port is None:
                print("Please check the platformio.ini for the 'monitor_port or the -p option")
                sys.exit(2)
        else:
            ser.baudrate = kwargs['baud'] or ser.baudrate
            ser.port = kwargs['port']
        if not ser.port:
            print('\nPlease provide the serial port information\n')
            print('\t arduplot -p /dev/cu.usbserail-ABCDEEF or arduplot -p COM3\n')
            sys.exit(3)
        try:
            ser.open()
            if ser.is_open is True:
                print('\nSerial port listening:')
                print(f'\tport: {ser.port}, baud: {ser.baudrate}\n')
        except SerialException:
            print(f'Serial Device {ser.port} is not found')
            sys.exit(4)

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
