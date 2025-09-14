import numpy as np
import cv2
import argparse
import imutils

def order_points(pts):

    # The function takes in four points, the corners, determine which corner is each point and returns it.

    rectangle = np.zeros ((4 , 2) , dtype="float32")

    sum_pts = np.sum (pts, axis = 1)

    rectangle[0] = pts [np.argmin(sum_pts)]
    rectangle[2] = pts [np.argmax(sum_pts)]

    diff_pts = np.diff (pts , axis = 1)

    rectangle[1] = pts [np.argmin(diff_pts)]
    rectangle[3] = pts [np.argmax(diff_pts)]

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

def main():

    inputs = argparse.ArgumentParser()
    inputs.add_argument("-i", "--image", required=True, type=str, help="Path to the image to be scanned")
    
    inputs = vars (inputs.parse_args())

    image = cv2.imread(inputs["image"])

    if image is None:
        print(f"Image cannot be loaded from {inputs['image']}")
        return
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur (gray, (5,5), 0)
    edged = cv2.Canny(gray, 100, 100)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    for i in cnts:
        print(cv2.contourArea(i))

    blank_1 = np.zeros_like(image)
    blank_2 = np.zeros_like(image)

    # Draw all contours in green, thickness 2
    cv2.drawContours(blank_1, cnts, 0, (0, 255, 0), 1)
    cv2.drawContours(blank_2, cnts, 2, (255, 0, 0), 1)

    cv2.imshow("Contours1", blank_1)
    cv2.imshow("Contours2", blank_2)
    cv2.imshow("The image", image)
    cv2.imshow("Edged", edged)
    cv2.waitKey(0)



if __name__ == "__main__":
    main()