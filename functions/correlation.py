# cross correlation function --------------------------------------------------------------------------------------------------

import numpy as np
from scipy.signal import lfilter

# lfilter contrast / smoothing the wave
cc_n = 3  # the larger n is, the smoother curve will be
cc_b = [0.95 / cc_n] * cc_n
cc_a = 1

# get corresponding window from selected row
def get_width(matrix, i, j, window):
    # keep this because near limits the window will be different
    if not (25 < i < matrix.shape[0] - 25) or not (25 < j < matrix.shape[1] - 25):
        return 0, 0
    n = np.where(matrix[i, max(0, j - window):min(matrix.shape[1], j + window + 1)] > 0)[0]
    if len(n) == 0:
        return j, matrix[i, j]
    return j - window + n[0], matrix[i, j - window + n[0]]

# check the cross correlation between 3 rows before and 3 rows after the selected point
def cross_correlation(image, matrix, i, j, direction):
    if direction == 2:
        image = image.T
        matrix = matrix.T
        i_aux = j
        j = i
        i = i_aux
    j0, w0 = get_width(matrix, i, j, int(matrix[i, j] / 2))
    j_1, w_1 = get_width(matrix, i - 1, j, int(w0 / 2))
    j_2, w_2 = get_width(matrix, i - 2, j, int(w_1 / 2))
    j_3, w_3 = get_width(matrix, i - 3, j, int(w_2 / 2))
    j1, w1 = get_width(matrix, i + 1, j, int(w0 / 2))
    j2, w2 = get_width(matrix, i + 2, j, int(w1 / 2))
    j3, w3 = get_width(matrix, i + 3, j, int(w2 / 2))

    w = np.min([int(w_3 / 2), int(w_2 / 2), int(w_1 / 2), int(w0 / 2), int(w1 / 2), int(w2 / 2), int(w3 / 2)])
    if w > 0:
        c = [
             np.corrcoef(lfilter(cc_b, cc_a, image[i - 3][max(0, j_3 - w):min(matrix.shape[1], j_3 + w + 1)]),
                         lfilter(cc_b, cc_a, image[i][max(0, j_2 - w):min(matrix.shape[1], j_2 + w + 1)]))[0, 1],
             np.corrcoef(lfilter(cc_b, cc_a, image[i - 2][max(0, j_2 - w):min(matrix.shape[1], j_2 + w + 1)]),
                         lfilter(cc_b, cc_a, image[i][max(0, j_1 - w):min(matrix.shape[1], j_1 + w + 1)]))[0, 1],
             np.corrcoef(lfilter(cc_b, cc_a, image[i - 1][max(0, j_1 - w):min(matrix.shape[1], j_1 + w + 1)]),
                         lfilter(cc_b, cc_a, image[i][max(0, j0 - w):min(matrix.shape[1], j0 + w + 1)]))[0, 1],
             np.corrcoef(lfilter(cc_b, cc_a, image[i + 1][max(0, j1 - w):min(matrix.shape[1], j1 + w + 1)]),
                         lfilter(cc_b, cc_a, image[i][max(0, j0 - w):min(matrix.shape[1], j0 + w + 1)]))[0, 1],
             np.corrcoef(lfilter(cc_b, cc_a, image[i + 2][max(0, j2 - w):min(matrix.shape[1], j2 + w + 1)]),
                         lfilter(cc_b, cc_a, image[i][max(0, j1 - w):min(matrix.shape[1], j1 + w + 1)]))[0, 1],
             np.corrcoef(lfilter(cc_b, cc_a, image[i + 3][max(0, j3 - w):min(matrix.shape[1], j3 + w + 1)]),
                         lfilter(cc_b, cc_a, image[i][max(0, j2 - w):min(matrix.shape[1], j2 + w + 1)]))[0, 1]
        ]
        return np.mean(c)
    return 0

from utils import get_diags_from_coords, get_coords_from_diags

def fit_lists_by_middle(*lists):
    # Find the middle index of each list
    middles = [len(lst) // 2 for lst in lists]

    # Find the shortest list length
    min_length = min(len(lst) for lst in lists)

    # Calculate the start and end indices for each list
    fitted_lists = []
    for i, lst in enumerate(lists):
        start = max(0, middles[i] - min_length // 2)
        end = start + min_length
        fitted_lists.append(lst[start:end])

    return fitted_lists

# check diagonal cross correlation
# inputs: image, matrix ( widths ), diagonal (di), diagonal_index (dj)
def cross_correlation_diagonal(image, matrix, path):
    diagonal_windows = [] # keep all diagonal windows from path here
    cc = []
    for (i, j) in path:
        # print(i, j)
        # get selected diagonal and width
        di, dj = get_diags_from_coords(image.shape[0], i, j)
        ab_window = int(matrix[i ,j] / 2)
        ab_diagonal = image[::-1, :].diagonal(di)
        w_left = max(0, dj - ab_window)
        w_right = min(len(ab_diagonal), dj + ab_window + 1)
        ab_window_diagonal = ab_diagonal[w_left:w_right]
        diagonal_windows.append(ab_window_diagonal)

    for i in range(len(diagonal_windows) - 4): #[2:-2]
        d_2, d_1, d, d1, d2 = fit_lists_by_middle(diagonal_windows[i - 2], diagonal_windows[i - 1], diagonal_windows[i], diagonal_windows[i + 1], diagonal_windows[i + 2])
        # print(len(d_2))
        # print(d_1)
        # print(d)
        # print(d1)
        # print(d2)

        if len(d) < 5:
            cc.append(0)
        else:
            c = [
                 np.corrcoef(lfilter(cc_b, cc_a, d_2),
                             lfilter(cc_b, cc_a, d_1))[0, 1],
                 np.corrcoef(lfilter(cc_b, cc_a, d_1),
                             lfilter(cc_b, cc_a, d))[0, 1],
                 np.corrcoef(lfilter(cc_b, cc_a, d),
                             lfilter(cc_b, cc_a, d1))[0, 1],
                 np.corrcoef(lfilter(cc_b, cc_a, d1),
                             lfilter(cc_b, cc_a, d2))[0, 1],
            ]
            # print(c)

            cc.append(np.mean(c))
    return cc
