__author__ = 'Lewis'

from ShimmerSensor import *
from shimmer_defs import *
from threading import Thread, Lock
import time


# Thread entry point for executing the class
def accel_thread_ep(pclass):
    pclass.thread_ep()


# Simple class for storing accelerometer data
class AccelBuffer():
    def __init__(self, timestamp, samplerate, xaccel, yaccel, zaccel):
        self.timestamp = timestamp
        self.samplerate = samplerate
        self.xaccel = xaccel
        self.yaccel = yaccel
        self.zaccel = zaccel

    def get_timestamp(self):
        return self.timestamp

    def get_sample_rate(self):
        return self.samplerate

    def get_x_accel(self):
        return self.xaccel

    def get_y_accel(self):
        return self.yaccel

    def get_z_accel(self):
        return self.zaccel

    # Convert this record in to a string
    def get_record_as_string(self):
        # int num elems, str[num] headers, int[num] values
        result = "5,"
        result += "Time Stamp,Sample Rate,X Acceleration,Y Acceleration,Z Acceleration,"
        result += str(self.get_timestamp()) + ","
        result += str(self.get_sample_rate()) + ","
        result += str(self.get_x_accel()) + ","
        result += str(self.get_y_accel()) + ","
        result += str(self.get_z_accel())

        return result


# Simple accelerometer class for sensor interface
class Accelerometer(ShimmerSensor):
    # Set up the sensor
    def __init__(self, hwaddr, verbose=False):
        super(Accelerometer, self).__init__(hwaddr, verbose)

        # Set up a thread locking class
        self.thread_lock = Lock()

        self.results = []

        self.monitoring = False

    # Return the kind of device we are
    def get_kind(self):
        return "Accelerometer"

    # Creates a thread to start reading the sensor
    def start(self):
        thread = Thread(target=accel_thread_ep, args=[self])
        thread.start()

    # Returns the latest record placed in the results
    def get_latest_record(self):
        # Lock the access mutex
        self.thread_lock.acquire(True)

        # result is null if there are no results
        result = None
        if len(self.results):
            result = self.results[len(self.results)-1]

        # release the mutex
        self.thread_lock.release()

        return result

    # Starts this device
    def start_monitoring(self):
        self.monitoring = True

    # Stops this device
    def stop_monitoring(self):
        self.monitoring = False

    # This is the entry point of the thread that manages this device - never call this yourself
    # it is blocking
    def thread_ep(self):
        while True:
            try:
                while not self.monitoring:
                    print "Monitoring is currently disabled..."
                    time.sleep(1)

                if self.verbose:
                    print "Accelerometer thread started for device with address: " + self.get_device_address()

                # Send the set sensors command, and enable the accelerometer
                self.send_set_sensors(accel=True)

                # Set the sampling rate
                self.send_set_sample_rate(SampleRate.SAMPLING_10HZ)

                buffer_size = 31  # Maximum buffer size

                # Start by setting the buffer size
                self.send_set_buffer_size(buffer_size)

                # Now start streaming
                self.send_start_streaming()

                # Please not that the following snippet has been modified from
                # https://github.com/ShimmerResearch/tinyos-shimmer/blob/master/apps/BtStream/python/bufferTest.py

                # Set up vars for reading
                ddata = ""
                num_bytes = 0
                sample_size = 8                             # TimeStamp (2), 3xAccel (3x2)
                frame_size = 1+(sample_size*buffer_size)    # Packet type (1), ((TimeStamp (2), 3xAccel (3x2)) x buffersize)
                last_time_stamp = 0

                # Loop while monitoring is taking place
                while self.monitoring:
                    # read incoming data
                    while num_bytes < frame_size:
                        ddata += self.read_buffer(frame_size)
                        num_bytes = len(ddata)

                    # Extract frame data
                    data = ddata[0:frame_size]
                    ddata = ddata[frame_size:]
                    num_bytes = len(ddata)

                    # Extract data from each frame IF it is a valid packet
                    packettype = struct.unpack('B', data[0:1])
                    if packettype[0] == PacketType.DATA_PACKET:
                        for i in range(buffer_size):
                            # Unpack this frame
                            (timestamp, accelx, accely, accelz) = \
                                struct.unpack('HHHH', data[(1+(sample_size*i)):(9+(sample_size*i))])

                            # Calculate the rate
                            if timestamp < last_time_stamp:
                                diff = timestamp + 0xFFFE - last_time_stamp
                            else:
                                diff = timestamp - last_time_stamp

                            rate = float(32768) / diff

                            # Lock the mutex to stop race conditions
                            self.thread_lock.acquire(True)

                            # Record the frame
                            self.results.append(AccelBuffer(timestamp, rate, accelx, accely, accelz))

                            # pop the front object if the buffer is too long - avoid memory wastage
                            if len(self.results) > 1000:
                                self.results = self.results[1:]

                            # Release the mutex
                            self.thread_lock.release()

                            last_time_stamp = timestamp
            except:
                # Some kind of error occured, try to reconnect the sensor
                self.connect_device()