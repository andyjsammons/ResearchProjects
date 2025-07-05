"""Try to outline the workflow for image registration to object
    isolation in lidar/RGB images
"""
import ImageRegistrationUtils as iru
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


depth_image = "./data/1721326786_TeraBee_bin/71_depthview_hot.jpg"
RGB_image = "image_71.jpg"
output_loc = "./workflow_test/"

Path(output_loc).mkdir(exist_ok=True, parents=True)

"""
#first lets increase contrast in RGB_image

sharp_img = iru.imageSharpening(RGB_image, output_loc)

#now do some smoothing

smooth_img = iru.imageSmoothing(sharp_img, 3, output_loc)

#now lets crop and resize:

cropped_resized_img = iru.cropAndResizeRGB(smooth_img, output_loc)

#register our image and produce gradient as Rdata object

iru.RNiftiReg(cropped_resized_img, depth_image, output_loc)

#we now have a gradient Rdata object and our registered RGB image
#stored in output_loc

#we can apply operations to the gradient object, namely read in
#Rdata object as a numpy array, upon which I would recommend
#some form of image isolation utilizing both edge detection
#and depth data, either via clustering, or some other algorithm
#of your choice. I attempted to use kmeans clustering, but without
#luck as I lacked the time.
"""
Rdata_gradient_path = output_loc + "20240823150851_niftyGradient.Rdata"

#lets create a binary mask from our RData Gradient object
binary_mask = iru.maskFromGradient(Rdata_gradient_path,0.10)

#do some plotting of our data:

x = list(range(0,len(binary_mask[0])))
y = list(range(0,len(binary_mask[:])))

X,Y = np.meshgrid(x,y)
Z = binary_mask

plot3d = plt.figure().add_subplot(projection='3d')
plot3d.plot_surface(X,Y,Z)
plt.show()




