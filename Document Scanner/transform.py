import numpy as np
import cv2

def order_points(pts):

    # The function takes in four points, the corners, determine which corner is each point and returns it.

    rectangle = np.zeros ((4 , 2) , dtype="float32")

    sum_pts = np.sum (pts , axis = 1)

    rectangle[0] = pts (np.argmin(sum_pts))
    rectangle[2] = pts (np.argmax(sum_pts))

    diff_pts = np.sum (pts , axis = 1)

    rectangle[1] = pts (np.argmin(sum_pts))
    rectangle[3] = pts (np.argmax(sum_pts))

    return rectangle # (tl , br , tr , bl)

def four_point_transform (image, pts):

    rectangle = order_points(pts)
    (tl , tr , br , bl) = rectangle

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    destination = np.array([[0,0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rectangle, destination)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped