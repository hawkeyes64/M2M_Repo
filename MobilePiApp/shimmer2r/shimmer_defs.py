__author__ = 'Lewis'


class SampleRate:
    SAMPLING_1000HZ = 1
    SAMPLING_500HZ = 2
    SAMPLING_250HZ = 4
    SAMPLING_200HZ = 5
    SAMPLING_166HZ = 6
    SAMPLING_125HZ = 8
    SAMPLING_100HZ = 10
    SAMPLING_50HZ = 20
    SAMPLING_10HZ = 100
    SAMPLING_0HZ_OFF = 255


# Packet Types
class PacketType:
    DATA_PACKET = 0x00
    INQUIRY_COMMAND = 0x01
    INQUIRY_RESPONSE = 0x02
    GET_SAMPLING_RATE_COMMAND = 0x03
    SAMPLING_RATE_RESPONSE = 0x04
    SET_SAMPLING_RATE_COMMAND = 0x05
    TOGGLE_LED_COMMAND = 0x06
    START_STREAMING_COMMAND = 0x07
    SET_SENSORS_COMMAND = 0x08
    SET_ACCEL_RANGE_COMMAND = 0x09
    ACCEL_RANGE_RESPONSE = 0x0A
    GET_ACCEL_RANGE_COMMAND = 0x0B
    SET_5V_REGULATOR_COMMAND = 0x0C
    SET_PMUX_COMMAND = 0x0D
    SET_CONFIG_SETUP_BYTE0_COMMAND = 0x0E
    CONFIG_SETUP_BYTE0_RESPONSE = 0x0F
    GET_CONFIG_SETUP_BYTE0_COMMAND = 0x10
    SET_ACCEL_CALIBRATION_COMMAND = 0x11
    ACCEL_CALIBRATION_RESPONSE = 0x12
    GET_ACCEL_CALIBRATION_COMMAND = 0x13
    SET_GYRO_CALIBRATION_COMMAND = 0x14
    GYRO_CALIBRATION_RESPONSE = 0x15
    GET_GYRO_CALIBRATION_COMMAND = 0x16
    SET_MAG_CALIBRATION_COMMAND = 0x17
    MAG_CALIBRATION_RESPONSE = 0x18
    GET_MAG_CALIBRATION_COMMAND = 0x19
    STOP_STREAMING_COMMAND = 0x20
    SET_GSR_RANGE_COMMAND = 0x21
    GSR_RANGE_RESPONSE = 0x22
    GET_GSR_RANGE_COMMAND = 0x23
    GET_SHIMMER_VERSION_COMMAND = 0x24
    SHIMMER_VERSION_RESPONSE = 0x25
    SET_EMG_CALIBRATION_COMMAND = 0x26
    EMG_CALIBRATION_RESPONSE = 0x27
    GET_EMG_CALIBRATION_COMMAND = 0x28
    SET_ECG_CALIBRATION_COMMAND = 0x29
    ECG_CALIBRATION_RESPONSE = 0x2A
    GET_ECG_CALIBRATION_COMMAND = 0x2B
    GET_ALL_CALIBRATION_COMMAND = 0x2C
    ALL_CALIBRATION_RESPONSE = 0x2D
    GET_FW_VERSION_COMMAND = 0x2E
    FW_VERSION_RESPONSE = 0x2F
    SET_BLINK_LED_COMMAND = 0x30
    BLINK_LED_RESPONSE = 0x31
    GET_BLINK_LED_COMMAND = 0x32
    SET_GYRO_TEMP_VREF_COMMAND = 0x33
    SET_BUFFER_SIZE_COMMAND = 0x34
    BUFFER_SIZE_RESPONSE = 0x35
    GET_BUFFER_SIZE_COMMAND = 0x36
    SET_MAG_GAIN_COMMAND = 0x37
    MAG_GAIN_RESPONSE = 0x38
    GET_MAG_GAIN_COMMAND = 0x39
    SET_MAG_SAMPLING_RATE_COMMAND = 0x3A
    MAG_SAMPLING_RATE_RESPONSE = 0x3B
    GET_MAG_SAMPLING_RATE_COMMAND = 0x3C
    ACK_COMMAND_PROCESSED = 0xFF


# Maximum number of channels
class MaxChannels:
    MAX_NUM_2_BYTE_CHANNELS = 12    # 3xAccel + 3xGyro + 3xMag + 2xAnEx + HR
    MAX_NUM_1_BYTE_CHANNELS = 0
    MAX_NUM_CHANNELS = MAX_NUM_2_BYTE_CHANNELS + MAX_NUM_1_BYTE_CHANNELS


# Packet Sizes
class PacketSize:
    DATA_PACKET_SIZE = 3 + (MaxChannels.MAX_NUM_2_BYTE_CHANNELS * 2) + MaxChannels.MAX_NUM_1_BYTE_CHANNELS
    RESPONSE_PACKET_SIZE = 76   # biggest possibly required (3 x kinematic + ECG + EMG calibration responses)
    MAX_COMMAND_ARG_SIZE = 21   # maximum number of arguments for any command sent to shimmer (calibration data)


# Channel contents
class ChannelContents:
    X_ACCEL = 0x00
    Y_ACCEL = 0x01
    Z_ACCEL = 0x02
    X_GYRO = 0x03
    Y_GYRO = 0x04
    Z_GYRO = 0x05
    X_MAG = 0x06
    Y_MAG = 0x07
    Z_MAG = 0x08
    ECG_RA_LL = 0x09
    ECG_LA_LL = 0x0A
    GSR_RAW = 0x0B
    GSR_RES = 0x0C     # GSR resistance (not used in this app)
    EMG = 0x0D
    ANEX_A0 = 0x0E
    ANEX_A7 = 0x0F
    STRAIN_HIGH = 0x10
    STRAIN_LOW = 0x11
    HEART_RATE = 0x12


# Infomem contents;
class InfomemContents:
    NV_NUM_CONFIG_BYTES = 94

    NV_SAMPLING_RATE = 0
    NV_BUFFER_SIZE = 1
    NV_SENSORS0 = 2
    NV_SENSORS1 = 3
    NV_ACCEL_RANGE = 12
    NV_MAG_CONFIG = 13     # upper 4 bits are gain, lower 4 bits are sampling rate
    NV_CONFIG_SETUP_BYTE0 = 14
    NV_ACCEL_CALIBRATION = 18
    NV_GYRO_CALIBRATION = 39
    NV_MAG_CALIBRATION = 60
    NV_EMG_CALIBRATION = 81
    NV_ECG_CALIBRATION = 85
    NV_GSR_RANGE = 93


# Sensor bitmap
class SENSORS0:
    SENSOR_ACCEL = 0x80
    SENSOR_GYRO = 0x40
    SENSOR_MAG = 0x20
    SENSOR_ECG = 0x10
    SENSOR_EMG = 0x08
    SENSOR_GSR = 0x04
    SENSOR_ANEX_A7 = 0x02
    SENSOR_ANEX_A0 = 0x01


class SENSORS1:
    SENSOR_STRAIN = 0x80
    SENSOR_HEART = 0x40


# Config Byte0 bitmap
class ConfigByte0Bitmap:
    CONFIG_5V_REG = 0x80
    CONFIG_PMUX = 0x40
    CONFIG_GYRO_TEMP_VREF = 0x20


# BtStream specific extension to range values
class BtStreamRangeSpecific:
    GSR_AUTORANGE = 0x04
    GSR_X4 = 0x05