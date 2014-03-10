__author__ = 'Lewis'

import socket
import sys
from threading import Thread

# socket settings
local_host = ''
local_port = 3487


# this is a basic thread that manages communications with the android app
# it is extremely simple as all it has to do is communicate the current
# state of monitoring, and be able to allow the state to be toggled.
def android_listener_thread(get_monitor_state, on_update_monitor_state):
    # The thread will never return
    while True:

        # Attempt to open the socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            # Oh no... Critical error...
            print 'Failed to create android socket'
            sys.exit()

        s.bind((local_host, local_port))
        s.listen(5)

        print 'Android communication port opened'

        # Now wait for the android app to try to connect
        client, address = s.accept()

        print 'Android client connected'

        # TODO: We should REALLY have some kind of authentication here

        # Now we figure out what the client is telling us to do...
        try:
            # The client will always send us one byte that indicates what it wants us to do
            data = client.recv(1)
            if not data:
                continue

            # TODO: Remove debug crap
            print [data]

            # 0x00 indicates that the client wants the current monitoring state
            if data == '\x00':
                # return the current state as standard bool values (Python transmits true and false as INTS not bytes)
                if get_monitor_state():
                    client.send('\x01')
                else:
                    client.send('\x00')

                # Always close the socket - one command per transaction
                client.close()

            # 0x01 indicates that the client wants to change the monitoring status
            if data == '\x01':
                # Get the new state
                data = client.recv(1)
                if data == '\x01':
                    on_update_monitor_state(True)
                else:
                    on_update_monitor_state(False)

                # TODO: Remove debug crap
                print get_monitor_state()

                # Always close the socket - one command per transaction
                client.close()
        except:
            pass


# This function opens the socket used for communicating with the android management application
def start_android_listener(get_monitor_state, on_update_monitor_state):
    thread = Thread(target=android_listener_thread,
                    args=[get_monitor_state, on_update_monitor_state])
    thread.start()
