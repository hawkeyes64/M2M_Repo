__author__ = 'Lewis'
import sys, struct, array
import bluetooth
from shimmer2r.accelerometer import Accelerometer

valid_model_list = ["RN42"]


# This function searches for bluetooth device, then checks that they are sensors.
# It then proceeds to create appropriate instances of the relevant sensor class
# It returns a list of device classes
def setup_bluetooth_services():

    print "Please wait, searching for bluetooth sensors..."

    # Locate the devices in range
    nearby_devices = bluetooth.discover_devices()

    devices = []

    # Loop over each device
    valid_device_array = []
    for device_addr in nearby_devices:

        # This fails occasionally with None, we need to know the device name! Keep looking up the device until
        # we get its name
        device_name = None
        while device_name is None:
            device_name = bluetooth.lookup_name(device_addr)

        print "Found bluetooth device " + device_name + " @ " + device_addr + ". Testing validity..."

        # Our devices names have the format "MODEL-BTADDR"
        # we need to cut the MODEL out and check it
        if device_name.split("-")[0] not in valid_model_list:
            print "Nope, device is not recognized, continuing search..."
            continue

        # We have a valid sensor device!
        print "Yes, device is recognized, will set up shortly..."
        valid_device_array.append([device_addr, device_name])

    print "Found " + str(len(valid_device_array)) + " devices - attempting to bring them online..."

    # Loop over all the found sensors and set them up
    for dev in valid_device_array:

        # This is a pretty big TODO - How can we detect this automatically?
        print "Please indicate what the type of sensor is, with BlueTooth address ending in: " + dev[0]
        print "1) Accelerometer"

        shim_dev = None

        # Create the handling class
        kind = input("> ")
        if kind == 1:
            shim_dev = Accelerometer(dev[0], True)

        if shim_dev is not None:
            shim_dev.start()
            devices.append(shim_dev)
        else:
            print "Error, invalid device - skipping"

    # return the list of devices
    return devices