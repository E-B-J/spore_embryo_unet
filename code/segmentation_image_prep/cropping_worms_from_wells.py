# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 12:15:17 2023

@author: ebjam
"""

from PIL import Image
import pandas as pd
import os

#bboxes = pd.read_csv(r"D:\Toronto_microscopy\OneDrive_1_11-28-2023_sds\2chan\SDS Wash I_Plate_1804\TimePoint_1\stacks\bboxes.csv")
bboxes = pd.read_csv(r"D:\Toronto_microscopy\OneDrive_1_11-28-2023_sds\2chan\SDS Wash U_Plate_1803\TimePoint_1\dy96\one_field\bbox_locations.csv")
bboxes['Label'] = bboxes['Label'].str.split(':')
# Create new columns for each part of ROI name to let me call images
bboxes[['Image', 'Roi']] = pd.DataFrame(bboxes['Label'].tolist(), index=bboxes.index)
bboxes = bboxes.drop('Label', axis=1)
#bboxes = bboxes.drop('Image_wl', axis=1)

# Get unique images and add to list, want to load each once and crop from there.
images = bboxes['Image'].unique()
# Split bboxes up by image
grouped = bboxes.groupby('Image')
#%%
# Folder where DY96 tifs are stored here:
dy96_path = 'D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field'
# Save crops to this directory:
crop_path = os.path.join(dy96_path, 'crops/')
os.makedirs(crop_path, exist_ok=True)
# For image, load image and relevant bboxes
for image in images:
    # Whatever clipping and string messing around I need to do to make it load DY image here!
    # SDS_Wash_I_E11.tif >> SDS Wash I_E11w2_combo.tif
    #spaced = image.replace('_', ' ', 2)[:-4] + 'w2_combo.tif'
    spaced=image
    im = Image.open(os.path.join(dy96_path, spaced))
    rele_bboxes = grouped.get_group(image)
    for i, bbox in rele_bboxes.iterrows():
        crop_box = (bbox['BX'], bbox['BY'], bbox['BX'] + bbox['Width'], bbox['BY'] + bbox['Height'])
        print(crop_box)
        cropped_image = im.crop(crop_box)
        cropped_image.save(os.path.join(crop_path, (bbox['Roi'] + bbox['Image'])))
        
#%%
for entry, row in rele_bboxes.iterrows():
    print(row['Area'])
              
#%%
import random
import os
croppath = "D:/Toronto_microscopy/OneDrive_1_11-28-2023_sds/2chan/SDS Wash U_Plate_1803/TimePoint_1/dy96/one_field/crops/"
crops = os.listdir(croppath)
select = random.sample(crops, round((len(crops)*0.2)))
select_folder = os.path.join(croppath, "random_select/")
os.makedirs(select_folder, exist_ok=True)
for img in select:
    os.rename(os.path.join(croppath, img), os.path.join(select_folder, img))