#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Copyright (c) 2021, Stephen Goadhouse <sgoadhouse@virginia.edu>
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
 
#-------------------------------------------------------------------------------
#  Instrument Child Class specific to Keithley 2400 SourceMeter
#-------------------------------------------------------------------------------

try:
    from . import instrument
except:
    from instrument import Instrument

# from: https://pypi.org/project/websocket-client/
from websocket import create_connection
import socket
    
class Keithley2400(Instrument):
    """Child instrument class for controlling the Keithley 2400 SourceMeter"""

    def __init__(self, resource):
        """Init the class with the instrument's resource string

        resource   - resource string, URI or VISA descriptor, like TCPIP0::172.16.2.13::INSTR
        """

        ## Number of readings to take and average over (Keithley does the averaging)
        self._NSAMPLES=10

        #  single channel
        #  wait 0.3 second between commands
        #  cmd_prefix is ':'
        #  read_termination is \n
        #  write_termination is \n
        super(Keithley2400, self).__init__(resource, chan=1, wait=0.3,
                                           cmd_prefix = ':',
                                           read_termination = '\n',
                                           write_termination = '\n')

    def _open(self, resource):
        return create_connection(resource,sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY,1),))    

    def _close(self, inst):
        inst.close()

    def _query(self, inst, queryStr):
        inst.send(queryStr)
        return inst.recv()
    
    def _write(self, inst, writeStr):
        return inst.send(writeStr)

    def _setup(self):
        self.open()
        self.write("SENS:VOLT:NPLC 10") ## set to high accuracy for ALL measurements - not just voltage
        self.write("SOUR:CLE:AUTO ON") ## Set AUTO ON mode so Keithley goes to idle after measurements
        ##@@@self.write("SOUR:CLE:AUTO OFF") ## Set AUTO OFF mode so Keithley stays enabled after measurement
        ##@@@self.write("ARM:COUN 6") ## set ARM Count = 6
        self.write("ARM:COUN 1") ## set ARM Count = 1
        self.write("ARM:SOUR IMM") ## set ARM Source = Immediate
        ##@@@self.write("ARM:SOUR TIM") ## set ARM Source = Timer
        ##@@@self.write("ARM:TIM 0.010") ## set ARM Timer to 10 ms
        self.write("TRIG:COUN 1") ## set Trigger Count = 1
        self.write("TRIG:SOUR IMM") ## set Trigger Source = Immediate
        self.write("SENS:AVER:TCON REP") ## Repeating Filter mode
        self.write("SENS:AVER:COUNT {}".format(self._NSAMPLES)) ## Average over NSAMPLES readings
        ##@@@self.write("SENS:AVER ON") ## Enable Filter mode - should see FILT on display
        self.write("SENS:AVER OFF") ## Disable Filter mode - let user manually enable if desired
        self.write("SENS:CURR:RANG:AUTO ON") ## Enable Auto Range Mode for Current Measurement 
        self.write("SENS:VOLT:RANG:AUTO ON") ## Enable Auto Range Mode for Voltage Measurement 
        self.write("SOUR:DEL 0.25") ## Delay 0.25 seconds after enable Source and before Measuring
        ##@@@self.write("SOUR:DEL:AUTO ON") ## Auto Delay after enable Source and before Measuring

        ##@@@
        #if (MODE_LOAD_CURRENT_INCR != 0):
        #    self.write("SOUR:CURR:RANG:AUTO ON")

        #@@@
        #if (MODE_LOAD_VOLTAGE_INCR != 0):
        #    self.write("SOUR:VOLT:RANG:AUTO ON")

        ## Put instrument back in front panel input mode
        self.write("SYST:LOC")

        self.close()

    def _action(self):
        self.open()
        result = self.query("READ?") ## read present value
        self.write("SYST:LOC")
        self.close()
        return result
