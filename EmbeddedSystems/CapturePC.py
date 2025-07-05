#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import socket
from utils import DepthDataProcessing

def receive_full_frame(conn, buffer_size, header_szie):
    header = conn.recv(header_szie)
    if len(header) < header_szie:
        return None

    # Check if the header matches
    if header[0] != 0xab or header[1] != 0xba:
        print("Invalid header received:", header)
        return None 

    data = b''
    while len(data) < buffer_size:
        packet = conn.recv(buffer_size - len(data))
        if not packet:
            return None
        data += packet

    return data


if __name__ == "__main__":
    ldp = DepthDataProcessing(device='TeraBee', frames_per_file=1, writedata=True,
                              display_point_cloud=True, display_rgb=True)

    BUFFER_SIZE =  ldp.width*ldp.height*2

    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345)) 
    server_socket.listen(1)
    print("Listening for connections...")
    
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    try:
        while ldp.active():        
            data = receive_full_frame(conn, BUFFER_SIZE, 2)
            if not data:
                break
            
            depth_array = np.frombuffer(data, dtype=np.uint16).reshape((ldp.height, ldp.width))
            depth_array = depth_array.copy()    
            
            ldp.processing(depth_array)
            ldp.plot_rgb_single_pixel(ldp.rgb_array)
            
            pcd = ldp.depth_to_pointcloud_open3d(depth_array)
            ldp.plot_point_cloud_o3d(pcd)

            
    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()
        server_socket.close()
