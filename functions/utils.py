# global helpers

import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
# Utils:
def npToImg(imgs):
    fig, ax = plt.subplots(1, len(imgs))

    if len(imgs) == 1:
        ax = [ax]

    for i, (image, title) in enumerate(imgs):
        ax[i].imshow(image, cmap='gray_r', vmin=0, vmax=255)
        ax[i].set_title(title)
        ax[i].axis('off')

    plt.tight_layout()
    plt.show()

def npSaveImg(npData, out_dir, title):
    grayscale_image = Image.fromarray(npData.astype(np.uint8))
    rgb_image = grayscale_image.convert('RGB')
    print(title, rgb_image.size)
    rgb_image.save(out_dir + title + '.png')


def crop(npData, crop_h1, crop_h2, crop_w1, crop_w2):
    return npData[crop_w1:crop_w2+1, crop_h1:crop_h2+1]


def percentile(data, pth: int):
    data = data.flatten()
    return np.percentile(data, pth)
    # size = len(data)
    # return data[int(math.ceil((size * perc) / 100)) - 1]


def count_images_in_folder(folder_path):
    # Use glob to find all .py files in the specified folder
    python_files = glob.glob(os.path.join(folder_path, '*.png'))
    return len(python_files)


# Plot waveforms for selected rows
def plot_waveforms(data, rowNo=0, title=''):
    fig, ax = plt.subplots(figsize=(12, 6))

    for row in range(data.shape[0]):
        waveform = data[row, :]
        ax.plot(waveform, label=f'Row {rowNo + row}')

    ax.set_title(title)
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    plt.show()

# translate diagonal into coordinates
# di - diagonal number / 0 to shape x 2
# dj - index in diagonal
def get_coords_from_diags(n, di, dj):
    if di <= n:
        return di - dj, dj
    else:
        return n - dj - 1, di - n + dj + 1

# translate coordinates into diagonal
# i, j = x, y from matrix
def get_diags_from_coords(n, i, j):
    if i == int(n/2) == j:
        return -n + i + j + 1, j
    elif n > i + j:
        return -n + i + j + 1, j
    else:
        return i - (n - j - 1), n - i - 1

#     n = 6
#     8, 0 = 5, 2
#     8, 2 = 3, 4
#     4, 0 = 3, 0
#     4, 2 = 2, 1

#     n = 6
#     0, 0 = 1, 0
#     2, 2 = -1, 2
#     3, 0 = -2, 0
#     3, 2 = 0, 2
#     0, 3 = -2, 3
#     3, 5 = 3, 2
#     4, 4 = 3, 1
#     5, 5 = 5, 0

#
# 1 2 3 4 5 6
# 2 3 4 5 6 7
# 3 4 5 6 7 8
# 4 5 6 7 8 9
# 5 6 7 8 9 0
# 6 7 8 9 0 1


