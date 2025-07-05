import sys
import numpy as np
import ArducamDepthCamera as ac
from utils import DepthDataProcessing


def main():
    cam = ac.ArducamCamera()
    if cam.open(ac.TOFConnect.CSI, 0) != 0:
        print("Initialization failed")
        sys.exit(-1)
    if cam.start(ac.TOFOutput.DEPTH) != 0:
        print("Failed to start camera")
        sys.exit(-1)
    cam.setControl(ac.TOFControl.RANG, 4)

    ldp = DepthDataProcessing(device='ArduCam')


    try:
        while ldp.active():
            frame = cam.requestFrame(200)
            if frame is not None:
                # Convert to mm scale
                buf = (frame.getDepthData()*1000).astype(np.uint16)
                amplitude_buf = frame.getAmplitudeData()
                cam.releaseFrame(frame)
                
                ldp.processing(buf, amplitude_buf)
                
    except KeyboardInterrupt:
        print("Stopping")
        
    finally:
        cam.stop()
        cam.close()

if __name__ == "__main__":
    main()