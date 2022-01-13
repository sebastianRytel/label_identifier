from PIL import Image
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def opening_img(filename=None):
    if not filename:
        return cv2.imread('IMG-0964.jpg')
    return Image.open(filename)


def inverting_img(img):
    """
    inverting colors of the img. Dark to Light and oposite.
    """
    inverted_image = cv2.bitwise_not(img)
    file_name = 'inverted.jpg'
    cv2.imwrite(file_name, inverted_image)
    return file_name

def greyscaling(img):
    """
    changing color to grayscale.
    """
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 100, 250, cv2.THRESH_BINARY)
    filename_gray = 'gray.jpg'
    filename_bw = 'bw.jpg'
    cv2.imwrite(filename_gray, gray_image)
    cv2.imwrite(filename_bw, im_bw)
    cv2.imshow(filename_bw, im_bw)
    cv2.waitKey(0)
    return filename_bw

def rotating_img(img):
    my_image_rot = img.rotate(270)
    my_image_rot.save('rotated.jpg')


def convert_img_to_string(my_image):
    img2 = np.array(my_image)
    text = pytesseract.image_to_string(img2)
    return text


def main():
    converting_functions = [inverting_img, greyscaling]
    origin_file = opening_img()
    converted = converting_functions[1](origin_file)
    my_image = opening_img(converted)
    print(convert_img_to_string(my_image))

main()
