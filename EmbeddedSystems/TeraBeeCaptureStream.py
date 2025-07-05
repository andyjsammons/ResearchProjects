import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from openni import openni2
import numpy as np
import socket
from utils import DepthDataProcessing
from picamera2.encoders import H264Encoder
import subprocess
import os
import threading
import queue

transferPC = True

# PIR Sensor
pir_port = 27

# Relay for IR LED
relay_port = 4

# Setup GPIO mode to Broadcom
GPIO.setmode(GPIO.BCM)

# Configure the PIR pin as input pin
GPIO.setup(pir_port, GPIO.IN)

# Configure the relay pin as output pin
GPIO.setup(relay_port, GPIO.OUT)

time.sleep(1)
# Deactivate the relay at the beginning
GPIO.output(relay_port, GPIO.HIGH)

# Initialize variables to count motion detections
motion_count = 0
motion_threshold = 2

# Time to keep the relay on (in seconds)
relay_on_time = 10

# Initialize Picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(10000000)

# Initialize OpenNI for LiDAR
openni2.initialize()
dev = openni2.Device.open_any()
depth_stream = dev.create_depth_stream()
depth_stream.start()

# Set up the socket connection to the server
def setup_socket_connection(host_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_ip, port))
    return client_socket

# Replace with your PC's IP address
HOST_IP = "192.168.137.1"
PORT = 12345
if transferPC:
    client_socket = setup_socket_connection(HOST_IP, PORT)
ldp = DepthDataProcessing(device='TeraBee')

# Queue for MP4 conversion and data logging
conversion_queue = queue.Queue()
processing_queue = queue.Queue()

def convert_videos():
    while True:
        h264_file = conversion_queue.get()
        if h264_file is None:
            break
        print("Convert file: ", h264_file)
        
        mp4_file = h264_file.replace('.h264', '.mp4')
        # Convert H.264 to MP4
        subprocess.run(['ffmpeg', '-i', h264_file, '-c', 'copy', mp4_file])
        print(f"Converted {h264_file} to {mp4_file}")

        # Delete the original H.264 file
        os.remove(h264_file)
        print(f"Deleted {h264_file}")

        conversion_queue.task_done()
        
def process_depth_data():
    while True:
        buf = processing_queue.get()
        if buf is None:
            break
        ldp.processing(buf)
        processing_queue.task_done()


# Start the conversion thread
conversion_thread = threading.Thread(target=convert_videos)
conversion_thread.start()

processing_thread = threading.Thread(target=process_depth_data)
processing_thread.start()

try:
    while True:
        if GPIO.input(pir_port) == 0:
            print("No motion detected")
            motion_count = 0 
        else:
            # Motion detected
            print("Motion detected")
            motion_count += 1

            if motion_count >= motion_threshold:
                print("Motion detected twice in a row. Activating relay and starting recording.")
                
                # Activate the relay
                GPIO.output(relay_port, GPIO.LOW)
                time.sleep(0.1)
                
                picam2.start()
                
                folder_name = ldp.folder_name
                
                # Record video for the specified duration
                h264_file = f"{folder_name}/video_{str(int(time.time()))}.h264"
                picam2.start_recording(encoder, h264_file)
                print("Video recording started")
                
                # Capture LiDAR frames while recording video
                start_time = time.time()
                while time.time() - start_time < relay_on_time:
                    frame = depth_stream.read_frame()
                    frame_data = frame.get_buffer_as_uint16()
                    buf = np.frombuffer(frame_data, dtype=np.uint16)
                    
                    # Log raw data to file in a separate thread
                    processing_queue.put(buf)
                    
                    # Stream back to PC
                    serialized_buf = buf.tobytes()
                    header = bytearray([0xab, 0xba])
                    data_to_send = header + serialized_buf
                    
                    if transferPC:
                        client_socket.sendall(data_to_send)
                                                                                                                                                                                                                                                                                                                                                                                            
                # Stop video recording
                picam2.stop_recording()
                print("Video recording stopped")
                
                # Add the mp4 conversion task to the queue
                conversion_queue.put(h264_file)

                # Deactivate the relay
                GPIO.output(relay_port, GPIO.HIGH)
                
                picam2.stop()
                motion_count = 0
        
        # Wait for 0.5 second between checks
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.output(relay_port, GPIO.HIGH)
    
    # Add termination to close the file and log data if any here
    ldp.terminate()
    
    depth_stream.stop()
    openni2.unload()
    if transferPC:
        client_socket.close()
    GPIO.cleanup()
    print("Exiting")

    # Stop the conversion thread
    conversion_queue.put(None)
    conversion_thread.join()
    processing_queue.put(None)
    processing_thread.join()
