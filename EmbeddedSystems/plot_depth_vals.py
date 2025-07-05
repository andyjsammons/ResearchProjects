from pathlib import Path
import numpy as np
import pandas as pd
from pandas import DataFrame as DF
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndimage
from scipy.signal import savgol_filter

dv_folder = Path('./data/depth_vals_4')

dv_out_files = list(dv_folder.glob('*'))

print(dv_out_files)

depth_val_arrays = [np.asarray(np.load(dv_out)) for dv_out in dv_out_files]
frame_num =1
frame =75
mean_30_frames = sum(depth_val_arrays[frame:frame+
                                      frame_num])//frame_num  #len(depth_val_arrays)


x = list(range(0,len(mean_30_frames[0])))
y = list(range(0,len(mean_30_frames[:])))

#Z = savgol_filter(mean_30_frames,len(mean_30_frames)+1,10)
Z = mean_30_frames
X,Y = np.meshgrid(x,y)


plot3d = plt.figure().gca(projection='3d')
plot3d.plot_surface(X,Y,Z)

#filter out values that are less than a third the maximum distance value
# to create binary mask matrix
plt_bn_img = np.zeros([Z.shape[0],Z.shape[1]])
plt_max = np.amax(abs(Z))
plt_bn_img = (plt_max/2.5) >= np.abs(Z) #>= (plt_max/1.5)

bin_30_frames = plt.figure().gca(projection='3d')
bin_30_frames.plot_surface(X,Y,plt_bn_img)

#apply the binary filter to Z distance data to filter out noise

Zeros = np.zeros([Z.shape[0],Z.shape[1]])
for row_idx in range(Z.shape[0]):
    for col_idx in range(Z.shape[1]):

        if plt_bn_img[row_idx][col_idx] == False:
            Zeros[row_idx][col_idx] = Z[row_idx][col_idx]
        else:
            Zeros[row_idx][col_idx] = 4000

Z_filtered = Zeros

Z_filtered_img = plt.figure().gca(projection='3d')
Z_filtered_img.plot_surface(X,Y,Z_filtered)


plt.show()


#want to determine height and width of the object 


