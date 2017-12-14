import sys
import time

import usb.core
import usb.util


VID = 0x0e8f
PID = 0x0025

ON = 0x55
OFF = 0xaa

dev = usb.core.find(idVendor=VID, idProduct=PID)

interface = 0

if dev.is_kernel_driver_active(interface) is True:
      # tell the kernel to detach
      dev.detach_kernel_driver(interface)
      # claim the device
#      usb.util.claim_interface(dev, interface)

dev.set_configuration()

#try:
print ("Trying ON")
ret = dev.ctrl_transfer(0x21, 0x09, 0x0200, 0, [ON])
time.sleep(5)
print ("Trying OFF")
ret = dev.ctrl_transfer(0x21, 0x09, 0x0200, 0, [OFF])
time.sleep(5)
#except usb.core.USBError as e:
#    data = None
#    if e.args == ('Operation timed out',):

# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)
