import numpy as np
import cv2

def order_points (pts):
    rectangle = np.zeros ((4 , 2) , dtype="float32")

    sum_pts = np.sum (pts , axis = 1)

    rectangle[0] = pts (np.argmin(sum_pts))
    rectangle[2] = pts (np.argmax(sum_pts))

    diff_pts = np.sum (pts , axis = 1)

    rectangle[1] = pts (np.argmin(sum_pts))
    rectangle[3] = pts (np.argmax(sum_pts))