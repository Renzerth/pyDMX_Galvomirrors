from time import sleep
from pyudmx import pyudmx
import numpy as np


def reset_channels(udmx_device):
    """
    Set all channel values to zero
    """
    channel_values = [0 for val in range(0, 512)]

    sent = udmx_device.send_multi_value(1, channel_values)
    print(sent)
    return None

#%% Device channel parameters
    
def main():
    """
    Executes a square laser scanning with galvomirrors using DMX
    """
    #%% Channel function mode presettings
    device_channel_values = [0 for v in range(0, 512)] # DMX address values
    
    device_channel_values[0] = 255 #[Channel 1] laserControlMode
    device_channel_values[1] = 3 #[Channel 2] patternNumber
    device_channel_values[2] = 2 #[Channel 3] colorChannel
    
    device_channel_values[3] = 59 #[Channel 4] x_coordinate_center
    device_channel_values[4] = 67 #[Channel 5] y_coordinate_center
    
    device_channel_values[5] = 75 #[Channel 6] patternXgradient
    device_channel_values[6] = 75 #[Channel 7] patternYgradient
    
    x_coordinate_center = device_channel_values[3]
    y_coordinate_center = device_channel_values[4]
    
    #%% Motion parameters
    center_fraction = 16 # Larger values reduces sweep range
    x_scope_position = x_coordinate_center//center_fraction
    y_scope_position = y_coordinate_center//center_fraction
    
    x_coord_range = np.arange(-x_scope_position, x_scope_position + 1, 1) + x_coordinate_center
    y_coord_range = np.arange(-y_scope_position, y_scope_position + 1, 1) + y_coordinate_center
    
    #%% Device udmx Controller
    laser_device = pyudmx.uDMXDevice()
    laser_device.open()
    print(laser_device.Device)
    
    #%% Initialize Fixture operation
    sent = laser_device.send_multi_value(1, device_channel_values)
    print(sent)
    
    #%% Fixture main motion
    for y_motion_value in y_coord_range:
        device_channel_values[4] = int(y_motion_value)
        sleep(0.01)
        for x_motion_value in x_coord_range:
            device_channel_values[3] = int(x_motion_value)
            laser_device.send_multi_value(1, device_channel_values)
            sleep(0.01)
    
    #%% Release device
    reset_channels(laser_device)
    laser_device.close()

#%% Execution
main()
