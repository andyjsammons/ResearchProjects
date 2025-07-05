library("oro.nifti")
library(RNiftyReg)
library(jpeg)
library(mmand)
library(imager)
library(raster)
library(png)

args = commandArgs(trailingOnly=TRUE)

#args needs to contain: 
#    1) path to RGB image file
#    2) path to BIN image file
#    3) location to place output image and gradient Rdata file
#    NOTE: if location to output isn't provided, will save in current working dir


if (length(args)==0){
  stop("Please provide paths to RGB image, depthview image, and output file location.n",call.=FALSE)
} else if(length(args)==2){
  args[3] = "./"
}


RGB_image <- readJPEG(paste0(args[1]))
BIN_image <- readJPEG(paste0(args[2]))


RGB_image <- apply(RGB_image,1:2,mean)
BIN_image <- apply(BIN_image,1:2,mean)

BIN_image <- as.cimg(BIN_image)

result <- niftyreg(RGB_image, BIN_image, nLevels=6)
kernel <- shapeKernel(c(2,2), type="diamond")
gradient <- mmand::dilate(result$image, kernel) - mmand::erode(result$image, kernel)

mmand::display(gradient)
writePNG(result$image,paste0(file=args[3],format(Sys.time(),"%Y%m%d%H%M%S"),'_registered_rgb.png'))
write.table(gradient,paste0(file=args[3],format(Sys.time(),"%Y%m%d%H%M%S"), '_niftyGradient.Rdata'))