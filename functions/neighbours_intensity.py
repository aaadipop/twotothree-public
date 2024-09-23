import numpy as np

# --- get all intense spots under the peak points in given width ---------------------------------------
def neighboursIntensity(image, x, y, maskSize):
    if image[x, y] == 0:
        return 0

    maskSize = int(maskSize / 2)
    p = np.asarray(image[max(x - maskSize, 0):min(image.shape[0], x + maskSize + 1),max(y - maskSize, 0):min(image.shape[1], y + maskSize + 1)])

    maxi = p.max()
    mini = p.min()
    avg = p.mean()
    mdr = 0

    if mini > 0 and maxi > 0:
        mdr = int(( mini + maxi ) / 2)

    return maxi + avg + mdr

def neighboursIntensity3D(images, i, x, y, maskSize):
    if images[i, x, y] == 0:
        return 0

    maskSize = int(maskSize / 2)
    p = np.asarray(images[max(i - maskSize, 0):min(images.shape[0], i + maskSize + 1), max(x - maskSize, 0):min(images.shape[1], x + maskSize + 1),max(y - maskSize, 0):min(images.shape[2], y + maskSize + 1)])

    maxi = p.max()
    mini = p.min()
    avg = p.mean()
    mdr = 0

    if mini > 0 and maxi > 0:
        mdr = int(( mini + maxi ) / 2)

    return maxi + avg + mdr

def neighboursLabel(image, x, y):
    maskSize = 1
    l = np.asarray(image[max(x - maskSize, 0):min(image.shape[0], x + maskSize + 1),max(y - maskSize, 0):min(image.shape[1], y + maskSize + 1), 1])
    l = int(np.max(l))
    if l == 0:
        return np.max(image[:, :, 1]) + 1
    return l

def neighboursLabelUnify(image, x, y):
    maskSize = 1
    l = np.asarray(image[max(x - maskSize, 0):min(image.shape[0], x + maskSize + 1),max(y - maskSize, 0):min(image.shape[1], y + maskSize + 1), 1])
    l = int(np.min(l[l != 0]))
    return l
