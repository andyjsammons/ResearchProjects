from pathlib import Path
import ImageRegistrationUtils as iru
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndimage
import cv2


dv_folder = Path('./data/depth_vals_5')

dv_out_files = list(dv_folder.glob('*'))

print(dv_out_files)

depth_val_arrays = [np.asarray(np.load(dv_out)) for dv_out in dv_out_files]
frame_num =1
frame =75
depth_val_matrix = depth_val_arrays[70] #len(depth_val_arrays)


Rdata = Path('niftyGradient.Rdata')


Rdata_matrix = iru.RMatrixToNumpy(Rdata)
Rdata_mask = Rdata_matrix[:,1:] >= 0.10


binary_mask = Rdata_mask


binary_mask = ndimage.binary_fill_holes(binary_mask)
#Rdata_mask.resize((mean_30_frames.shape[0], mean_30_frames.shape[1]))

x = list(range(0,len(binary_mask[0])))
y = list(range(0,len(binary_mask[:])))
Z = binary_mask
X,Y = np.meshgrid(x,y)


plot3d = plt.figure().add_subplot(projection='3d')
plot3d.plot_surface(X,Y,Z)
x = list(range(0,len(depth_val_matrix[0])))
y = list(range(0,len(depth_val_matrix[:])))
Z = depth_val_matrix
X,Y = np.meshgrid(x,y)

connected_comps, ncomps = iru.connectedComponents(binary_mask, depth_val_matrix)
new_mask = connected_comps == 15

newplot3d = plt.figure().add_subplot(projection='3d')
newplot3d.plot_surface(X,Y,new_mask)

Zeros = np.zeros([Z.shape[0],Z.shape[1]])
for row_idx in range(Z.shape[0]):
    for col_idx in range(Z.shape[1]):

        if new_mask[row_idx][col_idx] == True:
            Zeros[row_idx][col_idx] = Z[row_idx][col_idx]
        else:
            Zeros[row_idx][col_idx] = np.amax(abs(Z))

Z_filtered = Zeros

Z_filtered_img = plt.figure().add_subplot(projection='3d')
Z_filtered_img.plot_surface(X,Y,Z_filtered)

plt.show()
