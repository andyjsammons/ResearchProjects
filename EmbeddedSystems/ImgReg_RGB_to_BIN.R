library(oro.nifti)
library(RNiftyReg)
library(jpeg)
library(mmand)
library(imager)
library(raster)
library(png)
library('lattice')

folder.path = "C:/Users/ajsam/Desktop/trailCam/Trail_cam_20240712/Trail_Camera-nhan-ArduCam_Dimension_Estimation/"

BIN_image <- readJPEG(paste0(folder.path,"data/1721277763_TeraBee_bin/9_depthview_hot.jpg"))
RGB_image <- readJPEG(paste0(folder.path,"image_1721277769_lowres_cropped.jpg"))

BIN_image <- apply(BIN_image,1:2, mean)
RGB_image <- apply(RGB_image,1:2, mean)

BIN_image <- as.cimg(BIN_image)


mmand::display(as.matrix(RGB_image))

result <- niftyreg(RGB_image, BIN_image, nLevels=3)
png('registered_rgb.png')
kernel <- shapeKernel(c(2,2),type="diamond")
gradient <- mmand::dilate(result$image, kernel) - mmand::erode(result$image, kernel)

mmand::display(BIN_image)
mmand::display(mmand::threshold(gradient,method="kmeans"),add=TRUE,color="red")
mmand::display(result$image)

#plot.new()
#dev.new()
#plot(as.cimg(t(result$image)))
#dev.new()
plot(as.cimg(t(as.matrix(BIN_image))))
writePNG(result$image, paste0(file=folder.path, 'registered_rgb.png'))
write.table(gradient,paste0(file=folder.path, 'niftyGradient.Rdata'))
