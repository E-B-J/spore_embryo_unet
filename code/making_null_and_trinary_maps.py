# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:05:33 2023

@author: ebjam

"""
# For uninfected images: Need to make empty spore map for each embryo map

import os
import cv2
import numpy as np

path = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/embryomap/"
spore_mask_path = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/sporemask/"
embryo_masks = [q for q in os.listdir(path) if q.endswith("tif")]

for embryo_mask in embryo_masks:
    # Load mask
    embryo_mask_img = cv2.imread(os.path.join(path, embryo_mask))
    # Make uninfected spore mask
    uninfected_spore_mask = np.zeros_like(embryo_mask_img, dtype = np.uint8)
    cv2.imwrite(os.path.join(spore_mask_path, embryo_mask), uninfected_spore_mask)
    
    
#%% For Infected: Need to find instances where I miss-ran FIJI macro (TODO fix fiji macro!) and make missing masks
embryopath = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash I_Plate_1804/TimePoint_1/dy96/one_field/crops/embryomap/"
sporepath = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash I_Plate_1804/TimePoint_1/dy96/one_field/crops/sporemap/"
inpath
tri_path
embryomaps = [q for q in os.listdir(embryopath) if q.endswith("tif")]
sporemaps = [q for q in os.listdir(sporepath) if q.endswith("tif")]
tri_maps = [q for q in os.listdir(tri_path) if q.endswith("png")]
inputs = [q for q in os.listdir(inpath) if q.endswith("png")]
embryo_map_absent = [q for q in sporemaps if q not in embryomaps]
spore_map_absent = [q for q in embryomaps if q not in sporemaps]
tri_map_absent = [q for q in inputs if q not in tri_maps]
print("Missing embryo maps: " + str(len(embryo_map_absent)))
print("Missing spore maps: " + str(len(spore_map_absent)))
print("missing trinary: " + str(len(tri_map_absent)))
#%% Now, each of my images has a seperate embryo and spore mask
embryo_path = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/embryomap"
spore_path = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/sporemask"
trinary_mask_path = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/trinary_segmentation/"
os.makedirs(trinary_mask_path, exist_ok=True)
HR_trinary_mask_path = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/random_select/HR_trinary_segmentation/"
os.makedirs(HR_trinary_mask_path, exist_ok=True)
# I want to combine these, spores ontop of embryos
embryo_masks = [q for q in os.listdir(embryo_path) if q.endswith("tif")]
for embryo_mask in embryo_masks:
    embryo_img = cv2.imread(os.path.join(embryo_path, embryo_mask), )
    spore_img = cv2.imread(os.path.join(spore_path, embryo_mask))
    embryo_as_1 = embryo_img / 255
    spore_as_2 = 2*(spore_img / 255)
    quarternary_mask = embryo_as_1 + spore_as_2
    quarternary_mask[quarternary_mask == 3] = 2
    trinary_mask = quarternary_mask.copy().astype(np.uint8)
    savename = embryo_mask.replace(".tif", ".png")
    cv2.imwrite(os.path.join(trinary_mask_path, ("trinary" + savename)), trinary_mask)
    trinary_mask[trinary_mask == 1] = 128
    trinary_mask[trinary_mask == 2] = 255
    cv2.imwrite(os.path.join(HR_trinary_mask_path, ("HRtrinary" + savename)), trinary_mask)
    
    
#%%
import random
inpath = "C:/Users/ebjam/Documents/GitHub/spore_embryo_unet/images/inputs/resized320/"
all_images = [q for q in os.listdir(inpath) if q.endswith("png")]

random.shuffle(all_images)
test = all_images[:30]
train = all_images[30:]
testpath = os.path.join(inpath, "test/")
trainpath = os.path.join(inpath, "train/")
os.makedirs(testpath, exist_ok=True)
os.makedirs(trainpath, exist_ok=True)
for image in test:
    src = os.path.join(inpath, image)
    dst = os.path.join(testpath, image)
    os.rename(src, dst)
for image in train:
    src = os.path.join(inpath, image)
    dst = os.path.join(trainpath, image)
    os.rename(src, dst)