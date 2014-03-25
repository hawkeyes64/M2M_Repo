__author__ = 'Lewis'

import bluetooth
from shimmer_defs import *
import struct

current_device_id_count = 1


class ShimmerSensor(object):
    # This constructor sets up the bluetooth socket and connects the sensor
    def __init__(self, hwaddr, verbose=False):
        global current_device_id_count

        self.verbose = verbose

        # Remember the details for the device
        self.device_address = hwaddr
        self.device_channel = current_device_id_count

        self.com_sock = None

        # Increment the channel
        current_device_id_count += 1

        self.connect_device()

    def connect_device(self):
        # Start by connecting the device
        if self.verbose:
            print "ShimmerSensor - About to connect bluetooth device " + self.get_device_address() + " to channel " + \
                  str(current_device_id_count)

        self.com_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.com_sock.connect((self.get_device_address(), self.get_device_channel()))

    # Get the address of the device
    def get_device_address(self):
        return self.device_address

    # Get the bluetooth channel
    def get_device_channel(self):
        return self.device_channel

    # Waits for the sensor to acknowledge
    def __wait_for_ack(self):
        if self.verbose:
            print "ShimmerSensor - Waiting for ACK"

        data = ""
        ack = struct.pack('B', PacketType.ACK_COMMAND_PROCESSED)
        while data != ack:
            data = self.com_sock.recv(1)

        if self.verbose:
            print "ShimmerSensor - ACK Received"

    # Sends raw info to the sensor
    def __send_raw(self, s):
        return self.com_sock.send(s)

    # Receives raw info from the sensor
    def __recv_raw(self, num_bytes):
        return self.com_sock.recv(num_bytes)

    # Read in a specific number of bytes
    def read_buffer(self, num_bytes):
        count = 0
        ddata = ""
        while count < num_bytes:
            ddata += self.__recv_raw(1)
            count = len(ddata)

        return ddata

    # Empty the incoming read buffer
    def empty_read_buffer(self):
        while len(self.__recv_raw(1)):
            pass

    # Send a set sensor command
    def send_set_sensors(   self, accel=False, gyro=False, magneto=False, ecg=False, emg=False, gsr=False,
                            anexchan7=False, anexchan0=False, strain=False, heartrate=False):

        # Construct bytes to send to sensor
        byte0 = 0
        byte1 = 0

        # First byte
        if accel:
            byte0 += 0x80
        if gyro:
            byte0 += 0x40
        if magneto:
            byte0 += 0x20
        if ecg:
            byte0 += 0x10
        if emg:
            byte0 += 0x08
        if gsr:
            byte0 += 0x04
        if anexchan7:
            byte0 += 0x02
        if anexchan0:
            byte0 += 0x01

        # Second byte
        if strain:
            byte1 += 0x80
        if heartrate:
            byte1 += 0x40

        if self.verbose:
            print "ShimmerSensor - Sending SET_SENSORS_COMMAND: byte0: " + hex(byte0) + ", byte1: " + hex(byte1)

        # Send the command
        self.__send_raw(struct.pack('BBB', PacketType.SET_SENSORS_COMMAND, byte0, byte1))

        # And wait for ack
        self.__wait_for_ack()

    # Construct and send a set sample rate command
    def send_set_sample_rate(self, rate):
        if self.verbose:
            print "ShimmerSensor - Sending SET_SAMPLING_RATE_COMMAND: rate: " + hex(rate) + " (" + str(rate) + ")"

        # Send the command
        self.__send_raw(struct.pack('BB', PacketType.SET_SAMPLING_RATE_COMMAND, rate))

        # And wait for ack
        self.__wait_for_ack()

    # Tell the device to start streaming
    def send_start_streaming(self):
        if self.verbose:
            print "ShimmerSensor - Sending START_STREAMING_COMMAND"

        # Send the command
        self.__send_raw(struct.pack('B', PacketType.START_STREAMING_COMMAND))

        # And wait for ack
        self.__wait_for_ack()

    # Tell the device to stop streaming
    def send_stop_streaming(self):
        if self.verbose:
            print "ShimmerSensor - Sending STOP_STREAMING_COMMAND"

        # Send the command
        self.__send_raw(struct.pack('B', PacketType.STOP_STREAMING_COMMAND))

        # And wait for ack
        self.__wait_for_ack()

    # Tell the device how long the buffer should be
    def send_set_buffer_size(self, size):
        if self.verbose:
            print "ShimmerSensor - Sending SET_BUFFER_SIZE_COMMAND: " + str(size)

        # Send the command
        self.__send_raw(struct.pack('BB', PacketType.SET_BUFFER_SIZE_COMMAND, size))

        # And wait for ack
        self.__wait_for_ack()