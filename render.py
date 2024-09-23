from vedo import Volume, show, Plotter, Points, Lines, Text2D, Mesh, Image
import numpy as np
from scipy.spatial import KDTree

arrSize = 513 # ie
dataset = 'ie'

kernelMaskArr = np.loadtxt('oct/' + dataset + '/out/kernel_2d_mask.csv')
kernelMaskData = kernelMaskArr.reshape(kernelMaskArr.shape[0], kernelMaskArr.shape[1] // arrSize, arrSize)

kernelScanArr = np.loadtxt('oct/' + dataset + '/out/kernel_scanned.csv')
kernelScanData = kernelScanArr.reshape(kernelScanArr.shape[0], kernelScanArr.shape[1] // arrSize, arrSize)

kernelMask = Volume(kernelMaskData, spacing=[20, 20, 20])
kernelScan = Volume(kernelScanData, spacing=[20, 20, 20])

kernelMask = kernelMask.dilate(neighbours=(1,1,1))
kernelScan = kernelScan.dilate(neighbours=(3, 3, 3))

# values = [9]
isovalues = list(range(3))

kernelMask = kernelMask.isosurface_discrete(isovalues, nsmooth=1) # nsmooth - nr de iteratii
kernelScan = kernelScan.isosurface_discrete(isovalues, nsmooth=20) # nsmooth - nr de iteratii

kernelMask.color('red')
kernelScan.color('red')

show([kernelMask, kernelScan], N=2, viewup='z', axes=1, bg='white').close()

# slicing, but not soo good
# from vedo.applications import Slicer3DPlotter
# plt = Slicer3DPlotter(
#     kernelScan,
#     cmaps=("gist_ncar_r", "jet", "Spectral_r", "hot_r", "bone_r"),
#     use_slider3d=False,
#     bg="white",
#     bg2="blue9",
# )
#
# # Can now add any other vedo object to the Plotter scene:
# plt += Text2D("hello")
#
# plt.show(viewup='z')
# plt.close()