
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
os.environ['R_HOME'] = "C:\\Program Files\\R\\R-4.4.1"
import rpy2.robjects as robjects
from pathlib import Path
from datetime import datetime as dt
from scipy.ndimage.measurements import label
import open3d as o3d
from PIL import Image
import subprocess as sp


def imageSharpening(image_path, output_path = "./"):
    """
    Increase contrast in image.
    """
    pixvals = np.array(Image.open(image_path).convert("L"))
    pixvals = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) * 255
    minval = np.percentile(pixvals, 4)
    maxval = np.percentile(pixvals, 96)
    pixvals = np.clip(pixvals, minval, maxval)
    pixvals = ((pixvals - minval) / (maxval - minval)) * 255
    image = Image.fromarray(pixvals.astype(np.uint8))
    date = dt.strftime(dt.utcnow(), "%Y%m%d%H%M")
    image.save(output_path + '/' + date + "_sharpened.jpg")
    return output_path + '/' + date + "_sharpened.jpg"
    

def imageSmoothing(image_path, smooth_level, output_location = './'):
    """
    given some image, perform median blur smoothing 'smooth_level' times,
    then save to output_location under the name YYYYmmddHHMMSS_smoothed.jpg
    """
    output_location = output_location
    image = cv2.imread(image_path)
    filtered_image = image
    for i in range(smooth_level):
        filtered_image = cv2.medianBlur(filtered_image, 11)
    
    current_time = dt.now().strftime("%Y%m%d%H%M%S")
    output_image_name = output_location + current_time + "_" + 'smoothed.jpg'
    cv2.imwrite(output_image_name, filtered_image)
    return output_image_name

def RMatrixToNumpy(Rdata_path):
    """
    reads Rdata obj, returns numpy obj
    (use this is you run ImgReg_RGB_to_BIN.R to save image registration gradient)
    """
    Rdata = robjects.r['read.csv'](str(Rdata_path))[0] #returns list of strings
    Rdata_array = []

    #convert -Inf string vals to '0'
    for data in Rdata:
        data = data.replace('-Inf','0')
        Rdata_array.append(np.asarray([float(val) for val in data.split(' ')]))
        
    return np.asarray(Rdata_array)


def maskFromGradient(Rdata_path, truth_gradient):
    """
    given a gradient matrix from image registration, return bitmask
    """
    Rdata_matrix = RMatrixToNumpy(Rdata_path)
    Rdata_mask = Rdata_matrix[:,1:] >= truth_gradient
    
    return Rdata_mask


def connectedComponents(data_mask, depth_values):
    """
    iterate through depth values. set current value to False in data_mask if
    surrounding depth values are out of 250mm range. Then apply
    scipy.ndimage.measurements.label to label objects in data_mask.

    returns labeled_features matrix, and integer number of components
    """

    padded_True_indices = []
    padded_depth_values = np.pad(depth_values, ((1,1),(1,1)))
    padded_binary_mask = np.pad(data_mask, ((1,1),(1,1)))

    for row,y in enumerate(data_mask):
        for col,x in enumerate(y):
            if x == True:
                padded_True_indices.append([row+1,col+1])
                                 
    for indices in padded_True_indices:
        row, col = indices
        middle_depth_val = padded_depth_values[row][col]
        neighbors = padded_depth_values[row-1:row+2, col-1:col+2]
        distance_diff = abs(neighbors - float(middle_depth_val))
        
        for difference in distance_diff.reshape((1,9))[0]:
            if difference >= 250:
               #padded_binary_mask[row][col] = False
                pass

    structure = np.array([[0,1,0],[1,1,1],[0,1,0]])

    labeled_features, ncomponents = label(padded_binary_mask, structure)

    return labeled_features[1:-1,1:-1], ncomponents


def reateRGBDfromTUM(rgb_image_path, depth_image_path):
    color_raw = o3d.io.read_image(rgb_image_path)
    depth_raw = o3d.io.read_image(depth_image_path)
    rgbd_image = o3d.geometry.RGBDImage.create_from_tum_format(
        color_raw, depth_raw)
    return rgbd_image


def cropAndResizeRGB(path_to_RGB, path_to_output = "./"):
    img = cv2.imread(path_to_RGB)
    cropped = img[630:-300,1129:-1129]
    resized = cv2.resize(cropped, (80,60))
    time = dt.strftime(dt.utcnow(),"%Y%m%d%H%M%S")
    cv2.imwrite(path_to_output + str(time) + '_cropped_RGB.jpg', resized)
    return path_to_output + str(time) + '_cropped_RGB.jpg'


def RNiftiReg(RGB_image_path, DepthView_image_path, output_location = "./"):
    """
    runs getRegisteredRGBandGradient.R
    """
    if output_location != "./":
        Path(output_location).mkdir(exist_ok=True, parents=True)
    cmd = ['Rscript',
           'getRegisteredRGBandGradient.R',
           RGB_image_path,
           DepthView_image_path,
           output_location]
    completed_proc = sp.run(cmd,capture_output=True)



