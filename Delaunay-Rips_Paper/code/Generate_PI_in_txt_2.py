'''
Author: Amish Mishra
Date: Feb 3, 2022
README: Generate the PIs of various PDs from txt files into a single dataframe with structure
Class | H_1 pixel 1 | H_1 pixel 2 |....| H_2 pixel 1 | H_2 pixel 2 | .....
0     |             |             |    |             |             |
0     |             |             |    |             |             |
0     |             |             |    |             |             |
.     |             |             |    |             |             |
.     |             |             |    |             |             |
.     |             |             |    |             |             |
1     |             |             |    |             |             |
.     |             |             |    |             |             |
.     |             |             |    |             |             |
.     |             |             |    |             |             |
2     |             |             |    |             |             |
.     |             |             |    |             |             |
.     |             |             |    |             |             |
.     |             |             |    |             |             |
5     |             |             |    |             |             |
'''

import matplotlib.pyplot as plt
import numpy as np
import os
from persim import PersistenceImager
import pandas


# Initialize variables
home = os.path.expanduser("~")
basefilepath = f"{home}/Documents/research/Delaunay-Rips_Paper/pd_noise_0_05/"
noise_level = 0.05
filtration_func_arr = ["Alpha", "Del_Rips", "Rips"]
shape_name_arr = ["Circle", "Sphere", "Torus", "Random", "Clusters", "Clusters_in_clusters"]
num_datasets = 5
pts_per_dataset = 500


path = f"C:\\Users\\amish\Documents\\research\\Delaunay-Rips_Paper\\pd_noise_0_05\\\Alpha\\Circle\\PD_0_0.txt"
pd = np.loadtxt(path)
pimgrH0 = PersistenceImager(pixel_size=0.00001)
print(pimgrH0.pers_range)
pimgrH0.fit(pd, skew=True)
print(pimgrH0.pers_range)
pimgrH0.pixel_size = (pimgrH0.pers_range[1]-pimgrH0.pers_range[0])/20
pimgrH0.birth_range = (-pimgrH0.pixel_size/2, pimgrH0.pixel_size/2)
pimgrH0.weight_params = {'n': 1.0}
pimgrH0.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
pimg_H0 = pimgrH0.transform(pd, skew=True)
# print(pimg_H0)

fig, axs = plt.subplots(1, 3, figsize=(10,5))

axs[0].set_title("Original Diagram")
pimgrH0.plot_diagram(pd, skew=False, ax=axs[0])

axs[1].set_title("Birth-Persistence\nCoordinates")
pimgrH0.plot_diagram(pd, skew=True, ax=axs[1])

axs[2].set_title("Persistence Image")

pimgrH0.plot_image(pimg_H0, ax=axs[2])

plt.tight_layout()
plt.show()

exit()

# Find the image range for the H_2 class diagrams
pdgms_H2 = []
k = 2   # Hom class to extract
filtration_func = "Alpha"
for shape_name in shape_name_arr:
    if shape_name.lower()=="circle" and k==2:   # there are no H_2 persistence pairs for the Circle
        continue
    for i in range(num_datasets):
        path = f"C:\\Users\\amish\Documents\\research\\Delaunay-Rips_Paper\\pd_noise_0_05\\\{filtration_func}\\{shape_name}\\PD_{i}_{k}.txt"
        pd = np.loadtxt(path)
        pdgms_H2.append(pd)

# Find the image range for the H_1 class diagrams
pdgms_H1 = []
k = 1   # Hom class to extract
filtration_func = "Alpha"
for shape_name in shape_name_arr:
    if shape_name.lower()=="circle" and k==2:   # there are no H_2 persistence pairs for the Circle
        continue
    for i in range(num_datasets):
        path = f"C:\\Users\\amish\Documents\\research\\Delaunay-Rips_Paper\\pd_noise_0_05\\\{filtration_func}\\{shape_name}\\PD_{i}_{k}.txt"
        pd = np.loadtxt(path)
        pdgms_H1.append(pd)

# Set the persistence image parameters
pimgrH2 = PersistenceImager(pixel_size=0.5)
pimgrH2.fit(pdgms_H2, skew=True)
pimgrH2.weight_params = {'n': 1.0}
pimgrH2.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
pimgrH1 = PersistenceImager(pixel_size=0.5)
pimgrH1.fit(pdgms_H1, skew=True)
pimgrH1.weight_params = {'n': 1.0}
pimgrH1.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}

# Work on just turning the Torus H_2 and H_1 into a flattened PI vector
shape_name = 'Torus'
path = f"{basefilepath}{filtration_func}/{shape_name}/"
data_list = [None]*num_datasets
for i in range(num_datasets):
    # Make PI of H_2 diagram
    if shape_name.lower() != 'circle':    
        filename = str("PD_"+str(i)+"_"+str(2))               
        print(f'{path}{filename}')
        pd = np.loadtxt(f'{path}{filename}.txt')
        pimg_H2 = pimgrH2.transform(pd, skew=True)
    # Make PI of H_1 diagram
    filename = str("PD_"+str(i)+"_"+str(1))               
    print(f'{path}{filename}')
    pd = np.loadtxt(f'{path}{filename}.txt')
    pimg_H1 = pimgrH1.transform(pd, skew=True)
    # Add vector as a row to data_list
    data_list[i] = np.concatenate(([1], pimg_H2.flatten(), pimg_H1.flatten()))
        
df = pandas.DataFrame(data_list)
print(df)

exit()
path1 = '/home/amishra/Documents/Del_Rips_Paper/research/Delaunay-Rips_Paper/pd_noise_0_05/Alpha/Torus/PD_0_1.txt'
pd1 = np.loadtxt(path1)
pimgr = PersistenceImager(pixel_size=0.01)
pimgr.fit(pd1, skew=True)
pimgr.weight_params = {'n': 1.0}
pimgr.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
pimg_H1 = pimgr.transform(pd1, skew=True)


# fig, axs = plt.subplots(1, 3, figsize=(10,5))
#
# axs[0].set_title("Original Diagram")
# pimgr.plot_diagram(pd2, skew=False, ax=axs[0])
#
# axs[1].set_title("Birth-Persistence\nCoordinates")
# pimgr.plot_diagram(pd2, skew=True, ax=axs[1])
#
# axs[2].set_title("Persistence Image")
#
# pimgr.plot_image(pimg_H2, ax=axs[2])

# plt.tight_layout()
# plt.show()

exit()



# # Fit PI attributes to all H_0 classes

# # Track which path of input PD associates with index in pimgs
# pd_H0_shapes_idx_dict_array = [{}, {}, {}]
# for dict in pd_H0_shapes_idx_dict_array:
#     for shape_name in shape_name_arr:
#         dict[shape_name.lower()] = []
# idx = 0
# pdgms_H0 = []
# k = 0   # Hom class to extract
# for filtration_func in filtration_func_arr:
#     if filtration_func.lower() == 'alpha':
#         dict = pd_H0_shapes_idx_dict_array[0]
#     elif filtration_func.lower() == 'del_rips':
#         dict = pd_H0_shapes_idx_dict_array[1]
#     elif filtration_func.lower() == 'rips':
#         dict = pd_H0_shapes_idx_dict_array[2]
#     for shape_name in shape_name_arr:
#         if shape_name.lower()=="circle" and k==2:   # there are no H_2 persistence pairs for the Circle
#             continue
#         for i in range(num_datasets):
#             path = f"C:\\Users\\amish\Documents\\research\\Delaunay-Rips_Paper\\pd_noise_0_05\\\{filtration_func}\\{shape_name}\\PD_{i}_{k}.txt"
#             pd = np.loadtxt(path)
#             pdgms_H0.append(pd)
#             dict[shape_name.lower()].append(idx)
#             idx += 1

# print(pd_H0_shapes_idx_dict_array)

# pimgr = PersistenceImager(pixel_size=0.01)
# pimgr.fit(pdgms_H0, skew=True)
# pimgr.weight_params = {'n': 1.0}
# pimgr.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
# pimgs_H0 = pimgr.transform(pdgms_H0, skew=True)

# print(pimgs_H0)
# exit()


# Fit PI attributes to all H_1 classes

# Track which path of input PD associates with index in pimgs
pd_H1_shapes_idx_dict_array = [{}, {}, {}]
for dict in pd_H1_shapes_idx_dict_array:
    for shape_name in shape_name_arr:
        dict[shape_name.lower()] = []
idx = 0
pdgms_H1 = []
k = 1   # Hom class to extract
for filtration_func in filtration_func_arr:
    if filtration_func.lower() == 'alpha':
        dict = pd_H1_shapes_idx_dict_array[0]
    elif filtration_func.lower() == 'del_rips':
        dict = pd_H1_shapes_idx_dict_array[1]
    elif filtration_func.lower() == 'rips':
        dict = pd_H1_shapes_idx_dict_array[2]
    for shape_name in shape_name_arr:
        if shape_name.lower()=="circle" and k==2:   # there are no H_2 persistence pairs for the Circle
            continue
        for i in range(num_datasets):
            path = f"C:\\Users\\amish\Documents\\research\\Delaunay-Rips_Paper\\pd_noise_0_05\\\{filtration_func}\\{shape_name}\\PD_{i}_{k}.txt"
            pd = np.loadtxt(path)
            pdgms_H1.append(pd)
            dict[shape_name.lower()].append(idx)
            idx += 1

print(pd_H1_shapes_idx_dict_array)

pimgr = PersistenceImager(pixel_size=0.05)
pimgr.fit(pdgms_H1, skew=True)
pimgr.weight_params = {'n': 1.0}
pimgr.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
pimgs_H1 = pimgr.transform(pdgms_H1, skew=True)

print(pimgs_H1[17])

fig, axs = plt.subplots(1, 3, figsize=(10,5))

disp_idx = 17
axs[0].set_title("Original Diagram")
pimgr.plot_diagram(pdgms_H1[disp_idx], skew=False, ax=axs[0])

axs[1].set_title("Birth-Persistence\nCoordinates")
pimgr.plot_diagram(pdgms_H1[disp_idx], skew=True, ax=axs[1])

axs[2].set_title("Persistence Image")

pimgr.plot_image(pimgs_H1[disp_idx], ax=axs[2])

plt.tight_layout()
plt.show()

exit()


# Fit PI attributes to all H_2 classes
pdgms_H2 = []
k = 0   # Hom class to extract
for filtration_func in filtration_func_arr:
    for shape_name in shape_name_arr:
        if shape_name.lower()=="circle" and k==2:   # there are no H_2 persistence pairs for the Circle
            continue
        for i in range(num_datasets):
            path = f"C:\\Users\\amish\Documents\\research\\Delaunay-Rips_Paper\\pd_noise_0_05\\\{filtration_func}\\{shape_name}\\PD_{i}_{k}.txt"
            pd = np.loadtxt(path)
            pdgms_H2.append(pd)

pimgr = PersistenceImager(pixel_size=0.01, birth_range=(0,1))
pimgr.fit(pdgms_H2, skew=True)
pimgr.weight_params = {'n': 1.0}
pimgr.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
pimgs_H2 = pimgr.transform(pdgms_H2, skew=True)




fig, axs = plt.subplots(1, 3, figsize=(10,5))

axs[0].set_title("Original Diagram")
pimgr.plot_diagram(pdgms_H1[15], skew=False, ax=axs[0])

axs[1].set_title("Birth-Persistence\nCoordinates")
pimgr.plot_diagram(pdgms_H1[15], skew=True, ax=axs[1])

axs[2].set_title("Persistence Image")

pimgr.plot_image(pimgs_H1[15], ax=axs[2])

plt.tight_layout()
plt.show()


exit()



print(pd)

# Printing a PersistenceImager() object will print its defining attributes
pimgr = PersistenceImager(pixel_size=0.2, birth_range=(0,1))
# PersistenceImager() attributes can be adjusted at or after instantiation.
# Updating attributes of a PersistenceImager() object will automatically update all other dependent attributes.
pimgr.pixel_size = 0.01
# pimgr.birth_range = (0, 0.2)
# The `fit()` method can be called on one or more (*,2) numpy arrays to automatically determine the miniumum birth and
# persistence ranges needed to capture all persistence pairs. The ranges and resolution are automatically adjusted to
# accomodate the specified pixel size.
pimgr.fit(pd, skew=True)
# The `transform()` method can then be called on one or more (*,2) numpy arrays to generate persistence images from diagrams.
# The option `skew=True` specifies that the diagrams are currently in birth-death coordinates and must first be transformed
# to birth-persistence coordinates.
pimgr.weight_params = {'n': 1.0}
pimgr.kernel_params = {'sigma': [[0.00001, 0.0], [0.0, 0.00001]]}
pimgs = pimgr.transform(pd, skew=True)
# The `plot_diagram()` and `plot_image()` methods can be used to visualize persistence diagrams and images
fig, axs = plt.subplots(1, 3, figsize=(10,5))

axs[0].set_title("Original Diagram")
pimgr.plot_diagram(pd, skew=False, ax=axs[0])

axs[1].set_title("Birth-Persistence\nCoordinates")
pimgr.plot_diagram(pd, skew=True, ax=axs[1])

axs[2].set_title("Persistence Image")

pimgr.plot_image(pimgs, ax=axs[2])
print(pimgs)

plt.tight_layout()
plt.show()


''''
Notes:
- Put all H_k pds in a k_dgm array and run the .fit transformer on them to set the scale of the diagram
- Currently, I have all H_0, H_1, and H_2 diagrams in PI form for each dataset. I can also associate which
PI goes with the path to its respective PD.
- Next, I need to save the PI in a similar directory structure to the PDs under a new folder like
"pi_noise_0_05"
- Possibly, I will have to write another python script that will concatenate the H_0, 1, 2 classes for each
dataset together into one single vector for input into the ML model
'''