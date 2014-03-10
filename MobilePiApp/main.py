__author__ = 'Lewis'

import android_communicator

bMonitorEnabled = False


# Called when the android app tells us to alter our monitoring state
def on_update_monitor_state(new_state):
    global bMonitorEnabled
    bMonitorEnabled = new_state


# Called (usually) by the android app requesting the current monitoring state
def get_monitor_state():
    global bMonitorEnabled
    return bMonitorEnabled


# main entry point
def main():
    # start the android application interface
    # notice that we are passing function pointers...
    android_communicator.start_android_listener(get_monitor_state, on_update_monitor_state)

    print 'Loaded successfully.'

    input("Press Enter to continue...")

main()