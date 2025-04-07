#!/usr/bin/env python
# coding: utf-8

# In[1]:


''' title: "4010-Merged"
    author: "Garik Avagyan, Ha, Uyen Tran, Patrick Desmarais"
'''



# Installing and loading all necessary libraries
get_ipython().system('pip install laspy')
import laspy
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


# In[2]:


# Loading the RGB Point Cloud
rgb_las = laspy.read("C:/Users/garoa/Desktop/Data 4010/F_240717_1_RGBPC.las")
rgb_points = np.vstack((rgb_las.x, rgb_las.y, rgb_las.z)).T  # Extracting the x,y,z values from the dataset


# In[ ]:


# Loading the Multispectral Point Cloud
ms_las = laspy.read("C:/Users/garoa/Desktop/Data 4010/F_240717_1_MSPC.las")
ms_points = np.vstack((ms_las.x, ms_las.y, ms_las.z)).T  # Extracting x,y,z values from the dataset
ms_extra_bands = np.vstack((ms_las.red, ms_las.green, ms_las.blue, ms_las.nir)).T  # Extracting the  multispectral features


# In[ ]:


print(list(rgb_las.point_format.dimension_names))# Just to be sure that the features are correct


# In[ ]:


print(list(ms_las.point_format.dimension_names))


# In[ ]:


tree = cKDTree(ms_points)# A k-dimensional tree to perforn the nearest-neighbor algorithm in order to find the best matching between the x,y,z values of each point


# In[ ]:


distances, indices = tree.query(rgb_points, k=1) # Creating variables to identify the distances and the indices of points


# In[ ]:


# Creating new attributes for the RGB dataset
nir_values = np.full_like(rgb_las.x, np.nan, dtype=np.float32)# Assigning new attributes with NaN and 0 for now 
ms_red_values = np.full_like(rgb_las.x, 0, dtype=np.uint16)
ms_green_values = np.full_like(rgb_las.x, 0, dtype=np.uint16)
ms_blue_values = np.full_like(rgb_las.x, 0, dtype=np.uint16)


# In[ ]:


#Finding the approximated closest points in both dataset with a distance threshold of 1
valid_matches = distances < 1
nir_values[valid_matches] = ms_las.nir[indices[valid_matches]]#Assigning the attributes with the matched data. If there is no matched data, it remains Nan or 0
ms_red_values[valid_matches] = ms_las.red[indices[valid_matches]]
ms_green_values[valid_matches] = ms_las.green[indices[valid_matches]]
ms_blue_values[valid_matches] = ms_las.blue[indices[valid_matches]]


# In[ ]:


# Creating a new header for our new merged file
new_header = laspy.LasHeader(point_format=3, version="1.4")

new_header.add_extra_dim(laspy.ExtraBytesParams(name="nir", type=np.float32))
new_header.add_extra_dim(laspy.ExtraBytesParams(name="ms_red", type=np.uint16))
new_header.add_extra_dim(laspy.ExtraBytesParams(name="ms_green", type=np.uint16))
new_header.add_extra_dim(laspy.ExtraBytesParams(name="ms_blue", type=np.uint16))


# In[ ]:


merged_las = laspy.LasData(new_header)


# In[ ]:


# Assigning all the necessary attributes we need to our new created merged file
merged_las.x = rgb_las.x
merged_las.y = rgb_las.y
merged_las.z = rgb_las.z
merged_las.intensity = rgb_las.intensity
merged_las.return_number = rgb_las.return_number
merged_las.number_of_returns = rgb_las.number_of_returns
merged_las.classification = rgb_las.classification
merged_las.red = rgb_las.red  # We still keep the original rgb values from the RGB dataset
merged_las.green = rgb_las.green
merged_las.blue = rgb_las.blue
merged_las.confidence = rgb_las.confidence

# Assigning the new attributes
merged_las["nir"] = nir_values
merged_las["ms_red"] = ms_red_values
merged_las["ms_green"] = ms_green_values
merged_las["ms_blue"] = ms_blue_values


# In[ ]:


nir=merged_las.nir


# In[ ]:


ms_red=merged_las.nir


# In[ ]:


# Creating the new NDVI attribute, which is calculated by using the NIR and ms_res values from the multispectral dataset
ndvi = np.where(
    np.isnan(nir),  
    -1,  # Assiigning NDVI=-1 for missing values
    (nir - ms_red) / (nir + ms_red) 
)


# In[ ]:


merged_las["ndvi"]=ndvi


# In[ ]:


#Creating a new point cloud file for our merged dataset
merged_las.write("merged_with_ndvi.las")

