from utils import DepthDataProcessing
import time
import keyboard 
from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy

folder = 'data/1721326786_TeraBee_bin'
depth_dir = 'data/depth_vals_5'

ldp = DepthDataProcessing(folder_name=folder, device='TeraBee', display_point_cloud=True, display_rgb=True)
depth_data, amp_data = ldp.read_data(from_gzip=True)

# print(ldp.analyze_distance_log(2000))

fs = 30
delay = 1/fs
suspend = False 

def toggle_suspend():
    global suspend
    suspend = not suspend

keyboard.on_press_key("space", lambda _: toggle_suspend())  # Toggle suspend on space press

try:
    for i in range(int(0), depth_data.shape[0]):        
        ldp.depth_to_rgb(depth_data[i])
        rgb = ldp.rgb_array
        
        ldp.plot_rgb_single_pixel(rgb, depth=depth_data[i], frame_num=i)

        depth_out_filename = depth_dir + '/' + 'depth_file_' +str(i) + '.npy'
        
        numpy.save(depth_out_filename, numpy.asarray(depth_data[i]))

        pcd = ldp.depth_to_pointcloud_open3d(depth_data[i])
        # if i == 
        ldp.save_depth_view(rgb, i)
        ldp.plot_point_cloud_o3d(pcd, suspend=suspend)
        
        time.sleep(delay)
        
except Exception as e:
    print(f"Error: {e}")

finally:
    ldp.terminate()
