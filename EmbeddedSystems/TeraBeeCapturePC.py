#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import numpy as np
from openni import openni2
from utils import DepthDataProcessing
import cv2

# Initialize OpenNI
if platform.system() == "Windows":
    openni2.initialize("C:/Program Files/OpenNI2/Redist")  # Specify path for Redist
else:
    openni2.initialize()  # can also accept the path of the OpenNI redistribution

# Connect and open device
dev = openni2.Device.open_any()

# Create depth stream
depth_stream = dev.create_depth_stream()
depth_stream.start()

ldp = DepthDataProcessing(device='TeraBee', frames_per_file=300, display_point_cloud=True, display_rgb=True)

try:
    while ldp.active():    
        frame = depth_stream.read_frame()    
        frame_data = frame.get_buffer_as_uint16()
        depth_array = np.asarray(frame_data).reshape((ldp.height, ldp.width))    
        
        ldp.processing(depth_array)
        
        ldp.plot_rgb(ldp.rgb_array)
        
        pcd = ldp.depth_to_pointcloud_open3d(depth_array)
        ldp.plot_point_cloud_o3d(pcd)

except Exception as e:
    print(f"Error: {e}")

finally:
    depth_stream.stop()
    openni2.unload()