from math import sqrt
import sys
import time

import usb.core
import usb.util


class Thinktree(object):
    VID = 0x0e8f
    PID = 0x0025

    ON = 0x55
    OFF = 0xaa

    READ_TIMEOUT = 250

    def __init__(self):
        self._had_driver = False
        self._dev = usb.core.find(idVendor=Thinktree.VID, idProduct=Thinktree.PID)

        if self._dev is None:
            raise ValueError("Device not found")

        if self._dev.is_kernel_driver_active(0):
            self._dev.detach_kernel_driver(0)
            self._had_driver = True

        self._dev.set_configuration()

    def release(self):
        usb.util.release_interface(self._dev, 0)
        if self._had_driver:
            self._dev.attach_kernel_driver(0)

    def change(self, state):
        ret = self._dev.ctrl_transfer(0x21, 0x09, 0x0200, 0, [state])
        return ret == 1

    def main_loop(self):
        while True:
           self.change(Thinktree.ON)
           time.sleep(5)
           self.change(Thinktree.OFF)

if __name__ == "__main__":
    tt = Thinktree()
    tt.main_loop()
