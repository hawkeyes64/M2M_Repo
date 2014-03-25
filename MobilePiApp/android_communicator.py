__author__ = 'Lewis'

import pyjsonrpc
from threading import Thread
import sys

# socket settings
local_host = ''
local_port = 3487

# Function pointers
fn_get_monitor_state = None
fn_on_update_monitor_state = None
fn_get_monitor_data = None


# Server export to set the current monitoring state
def set_monitoring_state_export(new_state):
    fn_on_update_monitor_state(new_state)
    return fn_get_monitor_state()


# Server export to fetch the current monitoring state
def get_monitor_state_export():
    return fn_get_monitor_state()


# Server export to fetch the current data from the sensors
def get_monitor_data_export():
    return fn_get_monitor_data()


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    # Register public JSON-RPC methods
    methods = {
        "get_monitor_state": get_monitor_state_export,
        "set_monitor_state": set_monitoring_state_export,
        "get_monitor_data": get_monitor_data_export
    }


# this is a basic thread that manages communications with the android app
# it is extremely simple as all it has to do is communicate the current
# state of monitoring, and be able to allow the state to be toggled.
def android_listener_thread(get_monitor_state, on_update_monitor_state, get_monitor_data):
    global fn_get_monitor_state, fn_on_update_monitor_state, fn_get_monitor_data

    # Set up the function pointers
    fn_get_monitor_state = get_monitor_state
    fn_on_update_monitor_state = on_update_monitor_state
    fn_get_monitor_data = get_monitor_data

    # Threading HTTP-Server
    http_server = pyjsonrpc.ThreadingHttpServer(
        server_address=(local_host, local_port),
        RequestHandlerClass = RequestHandler
    )

    print "Starting HTTP server ..."
    http_server.serve_forever()


# This function opens the socket used for communicating with the android management application
def start_android_listener(get_monitor_state, on_update_monitor_state, get_monitor_data):
    thread = Thread(target=android_listener_thread,
                    args=[get_monitor_state, on_update_monitor_state, get_monitor_data])
    thread.start()
