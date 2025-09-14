import numpy as np
import cv2
import argparse

def rotate_image(image, angle):
    
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    print(type(angle))
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def main():
    parser = argparse.ArgumentParser(description='Rotate an image by a specified angle.')
    parser.add_argument('-i', required=True)
    parser.add_argument('-a', required=True)

    args = vars(parser.parse_args())

    image = cv2.imread(args["i"])

    if image is None:
        print(f"Error: Could not read image from {args['i']}")
        return

    rotated_image = rotate_image(image, float(args["a"]))

    cv2.imshow("Rotated", rotated_image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()