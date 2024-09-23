# twotothree-public
Blood Vessel Segmentation and 3D Reconstruction of Neovascularization in Age-Related Macular Degeneration from OCTA Scans
  
Abstract. We propose here a novel method for vessel segmentation and 3D
reconstruction of nAMD from OCTA images. The method has four steps: (1)
creating vessel mask; (2) isolating the Macular Neovascular Membranes from
noise; (3) finding the vessel depth in volume; (4) reconstructing the 3D volume.
Blood vessels were identified by detecting and marking spikes from four different
directions—row, column, and two diagonals—treated as a wave form, combined
with cross-correlation among five neighbouring points. When the parameters
are manually optimised for the available dataset, the method can achieve
up to 100% accuracy. Furthermore, using a kernel extracted from the main image,
the depth of a blood vessel was determined with an accuracy of 95.6%. By
extracting a 3D volume centred around the point of interest, based on previously
calculated coordinates, and retaining only high-intensity points, a 3D reconstruction
of the neovascularization area in AMD pathology was achieved. The
method has been tested on a dataset provided by the Emergency County Hospital,
Cluj-Napoca, Romania.  

Keywords: Age-related Macular Degeneration, Optical Coherence Tomography
Angiography, Image Processing, Vessel Segmentation

### Run the project
we cannot provide a dataset but you can add yours in `/oct` dir. the dataset should be as described in ...

1. adjust the variables in `functions/`