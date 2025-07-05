# Nhan Cao - 03/08/2024

import time
import sys
import os
import cv2
import numpy as np
import platform 
import gzip
import math
from scipy.interpolate import CloughTocher2DInterpolator
import matplotlib.pyplot as plt
import re

# Check the operating system and platform
platform_name = platform.platform().lower()

# Try to import open3d if not running on Raspbian
open3d_available = False
if 'armv' not in platform_name:
    try:
        import open3d as o3d
        open3d_available = True
    except ImportError:
        open3d_available = False
        

class UserRect():
    def __init__(self) -> None:
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
    
class DepthDataProcessing:
    DEVICE_MAP = {
        'TeraBee':{'height':60, 'width':80, 'flip':[-1., -1., -1.], 'fov':[74, 57], 'amplitude': False,  'display_amplitude':False},
        'ArduCamOptimal':{'height':90, 'width':120, 'flip':[1., 1., -1.], 'fov':[58.5, 45.6], 'amplitude': False, 'display_amplitude':False},
        'ArduCam':{'height':180, 'width':240, 'flip':[1., 1., -1.], 'fov':[58.5, 45.6], 'amplitude': True, 'display_amplitude':True}
    }
    
    def __init__(self, device='TeraBee',
                 frames_per_file=2000, 
                 folder_name=None, 
                 writedata=True,
                 display_point_cloud=False,
                 display_rgb=False):
        
        self.frame_count = 0
        self.file_index = 0
        self.frames_per_file = frames_per_file
          
        self.name = device
        device_config = self.__class__.DEVICE_MAP[self.name]
        self.height = device_config['height']
        self.width = device_config['width']
        self.flipXYZ = device_config['flip']
        self.fov_h, self.fov_v = device_config['fov']
        self.amplitude = device_config['amplitude']

        self.writedata = writedata
        
        if self.writedata:
            if folder_name != None:
                self.folder_name = folder_name
            else:
                self.folder_name = f'data/{str(int(time.time()))}_{self.name}'
            os.makedirs(self.folder_name, exist_ok=True)

        # Data holders
        self.rgb_array = None

        self.display_rgb = display_rgb
        
        self.fx = self.width / (2 * np.tan(np.deg2rad(self.fov_h / 2)))
        self.fy = self.height / (2 * np.tan(np.deg2rad(self.fov_v / 2)))
        self.cx = self.width / 2
        self.cy = self.height / 2
            
        if display_point_cloud and open3d_available:
            self.vis = o3d.visualization.Visualizer()
            self.vis.create_window(window_name='pointcloud', width=4000, height=3000)
            self.pcd = o3d.geometry.PointCloud()
            self.vis.add_geometry(self.pcd)        
            
        if display_rgb:
            self.selectRect = UserRect()
            self.followRect = UserRect()
            cv2.namedWindow("Depth View", cv2.WINDOW_NORMAL)
            # cv2.setMouseCallback("Depth View", self.on_mouse)
            cv2.setMouseCallback("Depth View", self.on_mouse_single_pixel)

            self.log_count = 0  

        # Buffer for data compression
        self.buffer = []
        self.buffer_amp = []

        self.fov_h_dimension = np.deg2rad(device_config['fov'][0])
        self.fov_v_dimension = np.deg2rad(device_config['fov'][1])
        
        self.intrinsics_rgb = {
            'fx': self.fx, 'fy': self.fy, 'cx': self.cx, 'cy': self.cy
        }
        self.intrinsics_depth = {
            'fx': self.fx, 'fy': self.fy, 'cx': self.cx, 'cy': self.cy
        }

        # Example extrinsic parameters (rotation and translation between RGB and Depth cameras)
        self.extrinsics = {
            'R': np.eye(3),  # Rotation matrix
            'T': np.zeros((3, 1))  # Translation vector
        }

    def active(self):       
        # Init in case no visualization required
        check = True     
        if self.display_rgb:
            check = check and cv2.waitKey(1) == -1 and cv2.getWindowProperty("Depth View", cv2.WND_PROP_FULLSCREEN) != -1

        return check
        

    def processing(self, depth, amp=None):
        self.depth_to_rgb(depth)
        self.depth = depth
        self.amp_array = amp

        if self.writedata:
            self.write_data(depth, self.amp_array)


    def depth_to_rgb(self, depth):  
        depth_process = depth.copy()

        max_distance = 7000
        min_distance = 0
        out_of_range = depth_process > max_distance
        too_close_range = depth_process < min_distance
        depth_process[out_of_range] = max_distance
        depth_process[too_close_range] = min_distance

        # Scaling depth array
        depth_scale_factor = 255.0 / (max_distance - min_distance)
        depth_scale_offset = -(min_distance * depth_scale_factor)
        depth_array_norm = depth_process * depth_scale_factor + depth_scale_offset
        rgb_frame = cv2.applyColorMap(depth_array_norm.astype(np.uint8), cv2.COLORMAP_HOT)
        # Replacing invalid pixel by black color
        rgb_frame[np.where(depth == 0)] = [0, 0, 0]
            
        self.rgb_array = rgb_frame
        

    def depth_to_pointcloud_open3d(self, depth, mapped_rgb=None, object_mask_depth=None):  
        if not open3d_available:
            raise RuntimeError("open3d is not available on this platform")
                
        depth_image_o3d = o3d.geometry.Image(depth.astype(np.float32))        
        pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(self.width, 
                                                                    self.height, 
                                                                    self.fx, 
                                                                    self.fy, 
                                                                    self.cx, 
                                                                    self.cy)
        
        pcd_filtered = o3d.geometry.PointCloud.create_from_depth_image(depth_image_o3d,
                                                            pinhole_camera_intrinsic)
        # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

        points = np.asarray(pcd_filtered.points)
        # distances = np.linalg.norm(points, axis=1)
        # mask = distances > 5   
        # pcd_filtered = pcd.select_by_index(np.where(mask)[0])

        idx = 0
        if mapped_rgb is not None and object_mask_depth is not None:
            colors = np.zeros(points.shape)
                        
            # Apply the RGB values to the corresponding points
            for i in range(points.shape[0]):
                x, y, z = points[i]
                pixel_x = int((x * self.fx / z) + self.cx)
                pixel_y = int((y * self.fy / z) + self.cy)
                
                if 0 <= pixel_x < 80 and 0 <= pixel_y < 60 and object_mask_depth[pixel_y, pixel_x]:
                    idx += 1
                    colors[i] = mapped_rgb[pixel_y, pixel_x]/255 # Normalize RGB values

            pcd_filtered.colors = o3d.utility.Vector3dVector(colors)
            
        pcd_filtered.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        pcd_filtered = pcd_filtered.voxel_down_sample(voxel_size=0.01)

        print('idx: ', idx)


        return pcd_filtered
    

    def write_data(self, depth, amp):
        if self.folder_name is None:
            self.folder_name = f'data/{str(int(time.time()))}_{self.name}'
            os.makedirs(self.folder_name, exist_ok=True)
            
        depth = depth.astype(np.int16)
        self.buffer.append(depth)
        
        if self.amplitude:
            amp = amp.astype(np.int16)
            self.buffer_amp.append(amp)
        
        if len(self.buffer) >= self.frames_per_file:
            self.flush_buffer()
        
        self.frame_count += 1
        if self.frame_count >= self.frames_per_file:
            self.file_index += 1
            self.frame_count = 0
            
            
    def flush_buffer(self):
        # Compress the data under gzip format
        combined_data = np.stack(self.buffer)

        depth_file_name = os.path.join(self.folder_name, f'{self.file_index}.bin.gz')
        with gzip.open(depth_file_name, 'wb') as f:
            f.write(combined_data)
        self.buffer = []

        if self.amplitude:
            combined_data_amp = np.stack(self.buffer_amp)

            amp_file_name = os.path.join(self.folder_name, f'amp_{self.file_index}.bin.gz')
            with gzip.open(amp_file_name, 'wb') as f:
                f.write(combined_data_amp)

            self.buffer_amp = []
        

            
    def read_data(self, from_gzip=False):
        if from_gzip:
            depth_files = sorted([f for f in os.listdir(self.folder_name) if f.endswith('.bin.gz') and not f.startswith('point_cloud') and not f.startswith('rgb') and not f.startswith('amp')],
                                 key=lambda x: int(re.search(r'\d+', x).group()))
            amp_files = sorted([f for f in os.listdir(self.folder_name) if f.startswith('amp') and f.endswith('.bin.gz')],
                               key=lambda x: int(re.search(r'\d+', x).group()))
        else:
            depth_files = sorted([f for f in os.listdir(self.folder_name) if f.endswith('.bin') and not f.startswith('point_cloud') and not f.startswith('rgb') and not f.startswith('amp')],
                                 key=lambda x: int(re.search(r'\d+', x).group()))
            amp_files = sorted([f for f in os.listdir(self.folder_name) if f.startswith('amp') and f.endswith('.bin')],
                               key=lambda x: int(re.search(r'\d+', x).group()))

        all_depth_data = []
        all_amp_data = []
        
        num_frames = []

        for depth_file in depth_files:
            depth_path = os.path.join(self.folder_name, depth_file)
            if from_gzip:
                with gzip.open(depth_path, 'rb') as f:
                    compressed_data = f.read()
                    depth_data = np.frombuffer(compressed_data, dtype=np.uint16)
            else:
                depth_data = np.fromfile(depth_path, dtype=np.uint16)
            
            num_frame = int(len(depth_data) / (self.height * self.width))
            num_frames.append(num_frame)
            depth_data = depth_data.reshape((num_frame, self.height, self.width))
            all_depth_data.append(depth_data)

        for amp_file in amp_files:
            amp_path = os.path.join(self.folder_name, amp_file)
            
            if from_gzip:
                with gzip.open(amp_path, 'rb') as f:
                    compressed_data = f.read()
                    amp_data = np.frombuffer(compressed_data, dtype=np.uint16)
            else:
                amp_data = np.fromfile(amp_path, dtype=np.uint16)
            all_amp_data.append(amp_data)

        final_depth_data = np.concatenate(all_depth_data, axis=0) if all_depth_data else np.empty((0, self.height, self.width), dtype=np.uint16)
        
        if not self.amplitude:
            final_amp_data = final_depth_data
        else:
            final_amp_data = np.concatenate(all_amp_data, axis=0) if all_amp_data else np.empty((0, self.height, self.width), dtype=np.uint16)
        return final_depth_data, final_amp_data        
        
        
    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selectRect.start_x = x
            self.selectRect.start_y = y

        elif event == cv2.EVENT_LBUTTONUP:
            self.selectRect.end_x = x
            self.selectRect.end_y = y

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            self.selectRect.end_x = x
            self.selectRect.end_y = y


    def plot_rgb(self, rgb, depth=None):
        if depth is not None:
            self.depth = depth

        center_x = (self.selectRect.start_x + self.selectRect.end_x) // 2
        center_y = (self.selectRect.start_y + self.selectRect.end_y) // 2
        
        print(center_x, center_y)

        # Get the mean value of the 4 most center pixels
        mean_value = np.mean([
            self.depth[center_y, center_x],
            self.depth[center_y - 1, center_x],
            self.depth[center_y, center_x - 1],
            self.depth[center_y - 1, center_x - 1]
        ])

        rect_width = self.selectRect.end_x - self.selectRect.start_x
        rect_height = self.selectRect.end_y - self.selectRect.start_y

        real_width = 0
        real_height = 0
        # Ensure the rectangle is valid
        if rect_width > 2 and rect_height > 2:
            print(f"Number of pixels within the rectangle: {rect_width}x{rect_height}")

            distance = mean_value  
            real_width = (rect_width / self.fx) * distance
            real_height = (rect_height / self.fy) * distance

            # print(f"Estimated dimensions: width = {real_width:.2f} mm, height = {real_height:.2f} mm")

        if not np.isnan(mean_value):
            log_file_path = os.path.join(self.folder_name, 'mean_values.log')
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"{mean_value:.2f}\n")
                self.log_count += 1  # Increment log count

            if self.log_count >= 5000:
                print("Logged 5000 values, exiting program.")
                self.terminate()

        text = f"{mean_value:.2f}"
        # print("select Rect distance:", mean_value)

        cv2.rectangle(rgb, (self.selectRect.start_x, self.selectRect.start_y),
                    (self.selectRect.end_x, self.selectRect.end_y),
                    (128, 128, 128), 1)
        # cv2.putText(rgb, text,
        #             (self.selectRect.start_x - 15, self.selectRect.start_y - 10),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(rgb, (self.followRect.start_x, self.followRect.start_y),
                    (self.followRect.end_x, self.followRect.end_y),
                    (255, 255, 255), 1)

        window_title = f"Distance: {mean_value:.2f} mm, Height: {real_height:.2f} mm, Width: {real_width:.2f} mm"

        cv2.imshow("Depth View", rgb)
        cv2.setWindowTitle("Depth View", window_title)


    def on_mouse_single_pixel(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selectRect.start_x = x
            self.selectRect.start_y = y

        elif event == cv2.EVENT_LBUTTONUP:
            self.selectRect.end_x = x
            self.selectRect.end_y = y
            self.plot_rgb_single_pixel(self.rgb_array)

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            self.selectRect.end_x = x
            self.selectRect.end_y = y
            self.plot_rgb_single_pixel(self.rgb_array)


    def plot_rgb_single_pixel(self, rgb, amp=None, depth=None, frame_num=None):
        if depth is not None:
            self.depth = depth 
            
        self.depth=self.depth.astype(object)
        
        if amp is not None:
            self.depth[amp < 30] = 4000
        
        x_A, y_A = self.selectRect.start_x, self.selectRect.start_y
        x_B, y_B = self.selectRect.end_x, self.selectRect.end_y

        if x_A < 0 or x_A >= self.width or y_A < 0 or y_A >= self.height or x_B < 0 or x_B >= self.width or y_B < 0 or y_B >= self.height:
            print("Selected points are out of bounds.")
            return

        d_A = self.depth[y_A, x_A]
        d_B = self.depth[y_B, x_B]

        if d_A == 0 or d_B == 0:
            print("Invalid depth value encountered.")
            return

        dx = x_B - x_A
        dy = y_B - y_A

        real_dx = dx * d_A / self.fx
        real_dy = dy * d_A / self.fy
        
        try:
            distance_AB = math.sqrt(real_dx**2 + real_dy**2 + (d_B - d_A)**2)
        except ValueError as e:
            print(f"Error in distance calculation: {e}")
            return
        
        # Draw a line from point A to point B
        cv2.line(rgb, (x_A, y_A), (x_B, y_B), (0, 255, 0), 1)

        window_title = f"Distance between A and B: {distance_AB:.2f} mm"
        if frame_num is not None:
            window_title += f' frame: {frame_num}'
        cv2.imshow("Depth View", rgb)
        cv2.setWindowTitle("Depth View", window_title)


    def create_oriented_bounding_box(self, depth_segmented, depth_array, position_adjustment=(0, 0, 0)):
        # Identify the object pixels (not equal to 255)
        white_pixel_mask = np.all(depth_segmented == [255, 255, 255], axis=-1)
        object_mask = ~white_pixel_mask

        if np.sum(object_mask) == 0:
            print("No object pixels found in the segmented depth image.")
            return None

        # Create a depth image in Open3D format
        depth_image_o3d = o3d.geometry.Image(depth_array.astype(np.float32))
        pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
            self.width, 
            self.height, 
            self.fx, 
            self.fy, 
            self.cx, 
            self.cy
        )

        pcd = o3d.geometry.PointCloud.create_from_depth_image(
            depth_image_o3d,
            pinhole_camera_intrinsic
        )
        pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        
        flat_object_mask = object_mask.flatten()
        object_points = pcd.select_by_index(np.where(flat_object_mask)[0])

        obb = o3d.geometry.OrientedBoundingBox.create_from_points(o3d.utility.Vector3dVector(object_points.points))
        obb.color = [0, 0, 0]  

        obb.translate(position_adjustment)

        return obb


    def create_3d_bounding_box(self, depth_segmented, depth_array):
        # Identify the object pixels (not equal to 255)
        white_pixel_mask = np.all(depth_segmented == [255, 255, 255], axis=-1)
        object_mask = ~white_pixel_mask

        if np.sum(object_mask) == 0:
            print("No object pixels found in the segmented depth image.")
            return None

        # Create a depth image in Open3D format
        depth_image_o3d = o3d.geometry.Image(depth_array.astype(np.float32))
        pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
            self.width, 
            self.height, 
            self.fx, 
            self.fy, 
            self.cx, 
            self.cy
        )

        pcd = o3d.geometry.PointCloud.create_from_depth_image(
            depth_image_o3d,
            pinhole_camera_intrinsic
        )
        pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        
        flat_object_mask = object_mask.flatten()
        object_points = pcd.select_by_index(np.where(flat_object_mask)[0])

        bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(o3d.utility.Vector3dVector(object_points.points))
        bbox.color = [0, 0, 0]  
        
        return bbox


    def plot_point_cloud_with_bbox(self, pcd, bbox, suspend=False):
        if not suspend:
            self.vis.remove_geometry(self.pcd)
            self.pcd = pcd
            self.vis.add_geometry(self.pcd)
            if bbox:
                self.vis.add_geometry(bbox)
            self.vis.update_renderer()
            self.vis.poll_events()
        else:
            geometries = [pcd]
            if bbox:
                geometries.append(bbox)
            o3d.visualization.draw_geometries(geometries)
            
        
    def plot_point_cloud_o3d(self, pcd, suspend=False):    
        # Set the color of all points to gray
        # gray_color = [0.5, 0.5, 0.5]  # This is a mid-gray, change the values between 0 (black) and 1 (white) for different shades
        # num_points = np.asarray(pcd.points).shape[0]
        # pcd.colors = o3d.utility.Vector3dVector([gray_color] * num_points)  # Apply the color to all points

        # remove, create and add new geometry.
        if not suspend:
            # self.vis.clear_geometries()
            self.vis.remove_geometry(self.pcd)
            self.pcd = pcd

            self.vis.add_geometry(self.pcd)
            self.vis.update_renderer()
            self.vis.poll_events()
        else:
            o3d.visualization.draw_geometries([pcd])
            
            # points = np.asarray(pcd.points)

            # x = points[:, 0]
            # y = points[:, 1]
            # z = points[:, 2]

            # # Define grid.
            # xi = np.linspace(min(x), max(x), num=100)
            # yi = np.linspace(min(y), max(y), num=100)
            # xi, yi = np.meshgrid(xi, yi)

            # from scipy.interpolate import griddata
            # zi = griddata((x, y), z, (xi, yi), method='cubic')

            # # Plot the surface.
            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            # surf = ax.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none')
            # fig.colorbar(surf)

            # ax.set_title('Surface Plot')
            # ax.set_xlabel('X')
            # ax.set_ylabel('Y')
            # ax.set_zlabel('Z')
            # plt.show()  
            
            
    def save_depth_view(self, rgb, frame_num):
        """
        Save the RGB representation of the depth view to a jpg file.
        """
        file_path = os.path.join(self.folder_name, f"{frame_num}_depthview_hot.jpg")
        cv2.imwrite(file_path, rgb)
        print(f"Depth view saved to {file_path}")
            
            
    def plot_amplitude(self, amplitude):
        amplitude*=(255/1024)
        amplitude = np.clip(amplitude, 0, 255)

        amplitude = cv2.resize(amplitude, (800, 600), interpolation=cv2.INTER_AREA)
        cv2.imshow("Amplitude", amplitude.astype(np.uint8))
            
            
    def analyze_distance_log(self, true_distance=2280.0):
        log_file_path = os.path.join(self.folder_name, 'mean_values.log')
        if not os.path.exists(log_file_path):
            print("Log file does not exist.")
            return

        with open(log_file_path, 'r') as log_file:
            values = [float(line.strip()) for line in log_file if line.strip()]

        mean_value = np.mean(values)
        offset_values = [value - true_distance for value in values]
        mean_offset = np.mean(offset_values)
        std_dev_offset = np.std(offset_values)
        min_offset = np.min(offset_values)
        max_offset = np.max(offset_values)
        median_offset = np.median(offset_values)

        stats = {
            'mean_value': mean_value,
            'mean_offset': mean_offset,
            'std_dev_offset': std_dev_offset,
            'min_offset': min_offset,
            'max_offset': max_offset,
            'median_offset': median_offset,
        }

        print(f"Log Analysis Results: {stats}")
        return stats

        
    def terminate(self):
        # Log data to file in case of early termination
        if len(self.buffer) > 0:
            self.flush_buffer()
        sys.exit(0)
