__author__ = 'Lewis'

import android_communicator
import bluetooth_communicator
import time

bMonitorEnabled = False
Sensor_Array = []


# Called when the android app tells us to alter our monitoring state
def on_update_monitor_state(new_state):
    global bMonitorEnabled, Sensor_Array
    bMonitorEnabled = new_state

    for s in Sensor_Array:
        if bMonitorEnabled:
            s.start_monitoring()
        else:
            s.stop_monitoring()


# Called (usually) by the android app requesting the current monitoring state
def get_monitor_state():
    global bMonitorEnabled
    return bMonitorEnabled


# Called by the android app to fetch live monitor data
def get_monitor_data():
    global Sensor_Array

    # Format is as follows
    # int num sensors , str sensor 1 kind, int num elems, str[num] headers, int[n] values, str sensor 2 kind ...

    result = ""
    num_devs = 0

    # Loop over each device
    for dev in Sensor_Array:
        # Only include this device if it has a record
        last_record = dev.get_latest_record()
        if last_record is not None:
            # This device is ok
            num_devs += 1
            # Append it's type to the results
            result += dev.get_kind() + ","
            # and the latest record as a string
            result += last_record.get_record_as_string() + ","

    # include hoe many valid devices there are
    result = str(num_devs) + "," + result
    return result


# main entry point
def main():
    global Sensor_Array

    # First, set up the bluetooth sensors
    Sensor_Array = bluetooth_communicator.setup_bluetooth_services()

    # start the android application interface
    # notice that we are passing function pointers...
    android_communicator.start_android_listener(get_monitor_state, on_update_monitor_state, get_monitor_data)

    for s in Sensor_Array:
        if bMonitorEnabled:
            s.start_monitoring()
        else:
            s.stop_monitoring()

    print 'Loaded successfully.'

    while True:
        print get_monitor_data()
        time.sleep(1)

main()