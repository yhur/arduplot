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

import subprocess
import socket
import os
import signal
import sys
from platformio.commands.device import DeviceMonitorFilter
from platformio.project.config import ProjectConfig

PORT = 19200

class SerialPlotter(DeviceMonitorFilter):
    NAME = "plotter"

    def __init__(self, *args, **kwargs):
        super(SerialPlotter, self).__init__(*args, **kwargs)
        self.buffer = ''
        self.arduplot = 'arduplot'
        self.plot = None
        self.plot_sock = ''
        self.plot = ''

    def __call__(self):
        pio_root = ProjectConfig.get_instance().get_optional_dir("core")
        if sys.platform == 'win32':
            self.arduplot = os.path.join(pio_root, 'penv', 'Scripts' , self.arduplot + '.cmd')
        else:
            self.arduplot = os.path.join(pio_root, 'penv', 'bin' , self.arduplot)
        print('--- serial_plotter is starting')
        self.plot = subprocess.Popen([self.arduplot, '-s', str(PORT)])
        try:
            self.plot_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.plot_sock.connect(('localhost', PORT))
        except socket.error:
            pass
        return self

    def __del__(self):
        if self.plot:
            if sys.platform == 'win32':
                self.plot.send_signal(signal.CTRL_C_EVENT)
            self.plot.kill()

    def rx(self, text):
        if self.plot.poll() is None:    # None means the child is running
            self.buffer += text
            if '\n' in self.buffer:
                try:
                    self.plot_sock.send(bytes(self.buffer, 'utf-8'))
                except BrokenPipeError:
                    try:
                        self.plot_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.plot_sock.connect(('localhost', PORT))
                    except socket.error:
                        pass
                self.buffer = ''
        else:
            os.kill(os.getpid(), signal.SIGINT)
        return text