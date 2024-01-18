# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:25:28 2024

@author: ebjam
"""
import os, cv2
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy import ndimage

def rotate_and_resize(path, aspect_ratio = 5):

    # Make rotated folder
    roto_path = os.path.join(path, "rotate_resize/")
    os.makedirs(roto_path, exist_ok=True)
    all_images = [q for q in os.listdir(path) if q.endswith('tif')]
    aspect_ratios = []
    aspect_dict = {}
    for image in all_images:
        # Load image
        img = cv2.imread(os.path.join(path, image))
        dim_list = [int(img.shape[0]), int(img.shape[1])]
        abs_aspect_ratio = max(dim_list) / min(dim_list)
        aspect_ratios.append(abs_aspect_ratio)
        aspect_dict[image] = {'abs_aspect_ratio':abs_aspect_ratio, 'shape':dim_list}
        
    handles = []
    for i in range(len(aspect_ratios)):
        handles.append('handle')
    
    for image in aspect_dict:
        img = cv2.imread(os.path.join(path, image))
        record = aspect_dict[image]
        if record['abs_aspect_ratio'] > 5:
            record['aspect_adjust'] = True
            rotate_45 = ndimage.rotate(img, 45, reshape = True)
            rotate_45_dims = [rotate_45.shape[0], rotate_45.shape[1]]
            adjust_aspect_ratio = max(rotate_45_dims) / min(rotate_45_dims)
            record['adjust_aspect_ratio'] = adjust_aspect_ratio
            record['adjust_shape'] = rotate_45_dims
            resized_rotated_img = cv2.resize(rotate_45, (320,320), interpolation = cv2.INTER_NEAREST)
            cv2.imwrite(os.path.join(roto_path, image), resized_rotated_img)
        # No adjust, just dummy the numbers to make plotting easier later - add a non-adjusted flag to keep this data seperate from rotated images!
        elif record['abs_aspect_ratio'] <= 5:
            record['aspect_adjust'] = False
            record['adjust_aspect_ratio'] = record['abs_aspect_ratio']
            record['adjust_shape'] = record['shape']
            resized_img = cv2.resize(img, (320,320), interpolation = cv2.INTER_NEAREST)
            # Write image to rotated folder
            cv2.imwrite(os.path.join(roto_path, image), resized_img)
    return(aspect_dict)

#%%
path = "C:/Users/ebjam/Documents/GitHub/spore_embryo_unet/images/trinary_segmentation/"
aspect_dict = rotate_and_resize(path)
#%%

adjust_plot_df = pd.DataFrame(aspect_dict).transpose().reset_index()
adjust_plot_df = adjust_plot_df.rename(columns={'index': 'image'})
adjust_plot_df['handle'] = 'handle'
adjust_plot_df['abs_aspect_ratio'] = adjust_plot_df['abs_aspect_ratio'].astype(float)
adjust_plot_df['adjust_aspect_ratio'] = adjust_plot_df['adjust_aspect_ratio'].astype(float)
adjust_plot_df['image'] = adjust_plot_df['image'].astype(str)
adjust_plot_df['aspect_adjust'] = adjust_plot_df['aspect_adjust'].astype(bool)
fig, axes = plt.subplots(1,2, sharey=True)
sns.set(rc = {'figure.figsize': (9,8), "figure.dpi":100, 'savefig.dpi':100})
sns.set_style("ticks")
sns.violinplot(x='handle', y='abs_aspect_ratio', data = adjust_plot_df, cut = 0, inner = None, color = 'grey', ax=axes[0])
sns.swarmplot(x='handle', y='abs_aspect_ratio', data = adjust_plot_df, hue = 'aspect_adjust', palette = 'rocket', size = 5, ax=axes[0])
sns.violinplot(x='handle', y='adjust_aspect_ratio', data = adjust_plot_df, cut = 0, inner = None, color = 'grey', ax=axes[1])
sns.swarmplot(x='handle', y='adjust_aspect_ratio', data = adjust_plot_df, hue = 'aspect_adjust', palette = 'rocket', size = 5, ax=axes[1])
sns.despine(bottom=True)

axes[0].set_xlabel("")
axes[0].set_xticklabels("")
axes[0].set_ylabel("Absolute Aspect Ratio")
axes[0].set_xticks([])
axes[0].get_legend().remove()
axes[0].set_title("Raw Aspect Ratios", fontsize = 16)
axes[0].axhline(5, color='k', linestyle = "--")
axes[1].set_xlabel("")
axes[1].set_xticklabels("")
axes[1].set_ylabel("Absolute Aspect Ratio")
axes[1].set_xticks([])
axes[1].get_yaxis().set_visible(False)
axes[1].set_title("Rotated Aspect Ratios", fontsize = 16)
sns.despine(ax=axes[1], left = True, bottom = True)
axes[1].get_legend().remove()

extreme = mlines.Line2D([], [], color='Purple', marker = 'o', linestyle='--',
                          markersize=10, label= '< 5x Aspect ratio - ("Normal")', linewidth=0)
normal =mlines.Line2D([], [], color='Orange', marker = 'o', linestyle='--',
                          markersize=10, label='> 5x Aspect ratio - ("Extreme")', linewidth=0)

fig.legend(loc = "lower center",handles=[normal, extreme], bbox_to_anchor=(0.5,0), ncol=1, fancybox=True)
roto_path = "C:/Users/ebjam/Documents/GitHub/spore_embryo_unet/images/"
# Save adjust_plot_df as a csv to keep track of transofrmations
adjust_plot_df.to_csv(os.path.join(roto_path, "rotation_transformations.csv"))
#%%
'''
plotdf = pd.DataFrame({'image':all_images, 'aspect_ratio':aspect_ratios, 'handles':handles})
#%%

fig, ax = plt.subplots(1,1)
sns.set(rc = {'figure.figsize': (6,8), "figure.dpi":100, 'savefig.dpi':100})
sns.set_style("ticks")
plotdf = pd.DataFrame({'image':all_images, 'aspect_ratio':aspect_ratios, 'handles':handles})
plotdf['extreme'] = 'Normal'
plotdf.loc[plotdf['aspect_ratio'] > 5.0, 'extreme'] = 'extreme'
plotdf.loc[plotdf['aspect_ratio'] < 0.2, 'extreme'] = 'extreme'
sns.violinplot(x='handles', y='aspect_ratio', data = plotdf, cut = 0, inner = None, color = 'grey', ax=ax)
sns.swarmplot(x='handles', y='aspect_ratio', hue = 'extreme', hue_order = ['Normal', 'extreme'], palette = 'rocket', data = plotdf, ax=ax)
sns.despine()
ax.axhline(5, color = 'k', linestyle = '--', alpha = 0.7)
ax.set_ylabel('Worm Aspect Ratio (1:Y)')
ax.set_xlabel("")
ax.set_xticklabels([""])
# Make legend explainging extreme vs not extreme!!
ax.get_legend().remove()


extreme = mlines.Line2D([], [], color='Orange', marker = 'o', linestyle='--',
                          markersize=10, label= '> 1:5 Aspect ratio - ("Extreme")', linewidth=0)
normal =mlines.Line2D([], [], color='Purple', marker = 'o', linestyle='--',
                          markersize=10, label='< 1:5 Aspect ratio - ("Pretty Normal")', linewidth=0)

ax.legend(loc = "upper center",handles=[normal, extreme], bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True)

#%%
dims = []
for image in aspect_dict:
    record = aspect_dict[image]
    dims.append(record['adjust_shape'][0])
    dims.append(record['adjust_shape'][1])

avg_dim = sum(dims) / len(dims)
print("Average image_dimensions:", avg_dim, "\nImage dimensions to use for UNET:", (avg_dim - (avg_dim % 32)))
'''