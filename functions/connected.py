# look for consecutive spikes with max gaps ------------------------------------------------------------------------

import numpy as np

def consecutive_gaps(gaps, max_gaps = 7):
    if len(gaps) > max_gaps - 1:
        last_elements = gaps[-max_gaps:]
        first_elements = [e[0] for e in last_elements]
        return all(first_elements[i] + 1 == first_elements[i + 1] for i in range(len(first_elements) - 1))
    return False

# check if a row have a neighbour peak in next width with a possibility to have gaps between
def check(matrix, peaks, i, j, window, path, gaps):
    if i + 2 > matrix.shape[0]:
       return path, gaps
    if consecutive_gaps(gaps):
        return path, gaps[:-7]
    # print("calling w: i:", i, " j:", j, "window:", window, "path/gaps:", path, gaps)

    next_row = peaks[i + 1, max(0, j - window):min(j + window + 1, matrix.shape[1])]

    next_row_peaks = np.where(next_row > 0)[0]

    lp, lg = path, gaps
    next_window = 5

    if len(next_row_peaks) > 0:
        for n in next_row_peaks:
            if (i + 1, n + j - window) not in lp:
                # if (i + 1, n + j - window) not in local_spikes:
                lp.append((i + 1, n + j - window))
                # why is this a 5 constant? -----
                next_window = window if matrix[i + 1, max(0, min(matrix.shape[1], n + j - window))] == 0 else int(matrix[i + 1, max(0, min(matrix.shape[1], n + j - window))] / 2)
                lp, lg = check(matrix, peaks, i + 1, max(0, min(matrix.shape[1], n + j - window)), next_window, lp, lg)
    else:
        lg.append((i + 1, j))
        next_window = window if matrix[i + 1, j] == 0 else int(matrix[i + 1, j] / 2)
        lp, lg = check(matrix, peaks, i + 1, j, next_window, lp, lg)

    return lp, lg

# look for consecutive diagonal spikes with max gaps -------------------------------------------------------------------

# check if a diagonal have a neighbour peak in next width with a possibility to have gaps between

from utils import get_diags_from_coords, get_coords_from_diags

# all time move from the current (i,j) point to next diagonal
def check_diag(matrix, i, j, window, path, gaps):
    if i + 2 > matrix.shape[0]:
       return path, gaps
    if consecutive_gaps(gaps, 2):
        return path, gaps[:-7]

    # convert matrix to diag coordinates
    di, dj = get_diags_from_coords(matrix.shape[0], i, j)

    # check if the conversion works
    a, b = get_coords_from_diags(matrix.shape[0], matrix.shape[0] + di - 1, dj)
    # if a != i or b != j:
        # print('!!! --------- Bad conversion for ', i, j)

    # get next diagonal and crop the window
    next_diagonal = matrix[::-1, :].diagonal(di + 1)
    # need to verify if the next diagonal is longer or not
    w_left = max(0, dj - window)
    w_right = min(len(next_diagonal), dj + window + 1)
    next_window_diagonal = next_diagonal[w_left:w_right]  # --- replace with window
    # print('next diagonal for point di, dj: ', di + 1, dj, next_window_diagonal)
    # print('next_window diagonal: ', next_window_diagonal, ' next window window: ', w_left, w_right)
    # print("for (a, b)", i, j, ' eq w. ', a, b, ' we got window, di, dj: ', window, di, dj)

    # if in next diagonal there are spikes, for each point get the
    next_diag_peaks = np.where(np.asarray(next_window_diagonal) > 0)[0]
    # print('next_diag_peaks: ', next_diag_peaks)

    # if next diagonal doesn't have peaks, move to the 2nd diagonal
    if len(next_diag_peaks) == 0:
        # print('moving to 2nd diagonal')
        di = di + 1
        dj = dj + 1 if di < 0 else dj - 1
        next_diagonal = matrix[::-1, :].diagonal(di + 1)
        # need to verify if the next diagonal is longer or not
        w_left = max(0, dj - window)
        w_right = min(len(next_diagonal), dj + window + 1)
        next_window_diagonal = next_diagonal[w_left:w_right]  # --- replace with window
        # print('next diagonal for point di, dj: ', di + 1, dj, next_window_diagonal)
        # print('next_window diagonal: ', next_window_diagonal, ' next window window: ', w_left, w_right)
        # print("for (a, b)", i, j, ' eq w. ', a, b, ' we got window, di, dj: ', window, di, dj)

        # 2nd diagonal peaks
        next_diag_peaks = np.where(np.asarray(next_window_diagonal) > 0)[0]
        # print('2nd diagonal next_diag_peaks: ', next_diag_peaks)

    lp, lg = path, gaps

    if len(next_diag_peaks) > 0:
        for n in next_diag_peaks:
            # print('##### di, dj for next diagonal to add: ', di + 1, w_left + n)
            # get diagolan matrix indice for peak
            a, b = get_coords_from_diags(matrix.shape[0], matrix.shape[0] + di, w_left + n)
            # print('##### a, b for next diagonal: ', a, b)
    #         # if (i + 1, n + j - window) not in lp:
            if (a, b) not in lp:
                lp.append((a, b))
    #             # get the next diagonal spike width from matrix
                next_window = int(next_window_diagonal[n] / 2)
                # print('next_window: ', next_window)
                lp, lg = check_diag(matrix, a, b, next_window, lp, lg) #max(0, min(matrix.shape[1], b))
    else:
        # print('##### add diagonal gap: ', i + 1, j + 1)
        lg.append((i + 1, j + 1))
        next_window = window # if matrix[i + 1, j] == 0 else int(matrix[i + 1, j] / 2)
        lp, lg = check_diag(matrix, i + 1, j + 1, next_window, lp, lg)

    return lp, lg