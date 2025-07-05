import sys
import time
import queue
import socket
import threading
import numpy as np
import ArducamDepthCamera as ac
from utils import DepthDataProcessing

def setup_socket_connection(host_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_ip, port))
    return client_socket
        
def process_stream_data():
    while True:
        buf = processing_queue.get()
        
        if buf is None:
            break
        
        serialized_buf = buf.tobytes()
        header = bytearray([0xab, 0xba])
        data_to_send = header + serialized_buf
        
        client_socket.sendall(data_to_send)
        processing_queue.task_done()


transferPC = True

HOST_IP = "192.168.137.1"
PORT = 12345

if transferPC:
    client_socket = setup_socket_connection(HOST_IP, PORT)
    
processing_queue = queue.Queue()

processing_thread = threading.Thread(target=process_stream_data)
processing_thread.start()
relay_on_time = 10

cam = ac.ArducamCamera()
if cam.open(ac.TOFConnect.CSI, 0) != 0:
    print("Initialization failed")
    sys.exit(-1)
if cam.start(ac.TOFOutput.DEPTH) != 0:
    print("Failed to start camera")
    sys.exit(-1)
cam.setControl(ac.TOFControl.RANG, 4)

ldp = DepthDataProcessing(device='ArduCam', writedata=True)

try:
    while True:                
        start_time = time.time()
        while time.time() - start_time < relay_on_time:
            
            frame = cam.requestFrame(200)
            if frame is not None:
                # Convert to mm scale
                buf = (frame.getDepthData()*1000).astype(np.uint16)
                amplitude_buf = frame.getAmplitudeData()
                cam.releaseFrame(frame)
            
                if transferPC:
                    processing_queue.put(buf)
                    
                # Log raw data 
                ldp.processing(buf, amplitude_buf)
                

except KeyboardInterrupt:
    ldp.terminate()

    if transferPC:
        client_socket.close()
    print("Exiting")

    processing_queue.put(None)
    processing_thread.join()
