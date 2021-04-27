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
#  Parent Class for an instrument
#-------------------------------------------------------------------------------

import time

class Instrument(object):
    """Base class for controlling and accessing an Instrument"""

    def __init__(self, resource, chan=1, wait=None, 
                 cmd_prefix = '',
                 read_termination = '',
                 write_termination = ''):
        """Init the class with the instrument's resource string

        resource   - resource string, URI or VISA descriptor, like TCPIP0::172.16.2.13::INSTR
        chan       - number of selected channel if device is multi-channel. Starts with 1
        wait       - float that gives the default number of seconds to wait after sending each command or None if no wait
        cmd_prefix - optional command prefix (ie. some instruments require a ':' prefix)
        read_termination - optional read_termination parameter to pass to open_resource()
        write_termination - optional write_termination parameter to pass to open_resource()
        """
        self._resource = resource
        self._wait = wait
        self._chan = chan
        self._prefix = cmd_prefix
        self._read_termination = read_termination
        self._write_termination = write_termination
        self._inst = None        

    def open(self):
        """Open a connection to the instrument"""
        self._inst = self._open(self._resource)

    def close(self):
        """Close the instrument"""
        self._close(self._inst)
        self._inst = None

    @property
    def channel(self):
        return self._chan

    def query(self, queryStr):
        queryStr = self._prefix + queryStr + self._write_termination
        #print("QUERY:",queryStr)
        result = self._query(self._inst, queryStr)
        if self._wait is not None:
            time.sleep(self._wait)
        return result
        
    def write(self, writeStr):
        writeStr = self._prefix + writeStr + self._write_termination
        #print("WRITE:",writeStr)
        result = self._write(self._inst, writeStr)
        if self._wait is not None:
            time.sleep(self._wait)
        return result

    def setup(self):
        return self._setup()
    
    def action(self):
        """Perform the instrument action (read, stop, screen capture, etc) and return the string to be sent ot computer via USB HID"""
        return self._action()
    
    # Each Child Class must define the following specific to themselves
    def _open(self, resource):
        raise RuntimeError("_open() not defined by child instrument")

    def _close(self, inst):
        raise RuntimeError("_close() not defined by child instrument")

    def _query(self, inst, queryStr):
        raise RuntimeError("_query() not defined by child instrument")
    
    def _write(self, inst, writeStr):
        raise RuntimeError("_write() not defined by child instrument")

    def _setup(self):
        raise RuntimeError("_setup() not defined by child instrument")

    def _action(self):
        raise RuntimeError("_action() not defined by child instrument")
