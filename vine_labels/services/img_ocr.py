from PIL import Image
import pytesseract
from pytesseract import Output
from cv2 import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OrigImage:
    """
    Creates object -> loaded original image.
    """
    @staticmethod
    def cv2_img_obj(img_file):
        """
        Loads original image for edit and cv2 postprocessing.
        """
        return cv2.imread(img_file)

    def __new__(self, *args, **kwargs):
        print('\n**Original Image has been loaded**\n')

class ImgAsNpArray:
    """
    Creates object np array data structure from post processed image.
    """

    @staticmethod
    def open_edited_img(img_file):
        """
        Opens post processed image and converts to np array data structure. /for further data conversion.
        """
        return np.array(Image.open(img_file))


class ImgAsData:
    """
    Initialize edited (class ImageEditor) object image as np array for further data conversion.
    """

    def __init__(self, img_file):
        self.img = ImgAsNpArray.open_edited_img(img_file)

    def img_to_string(self):
        """
        Converts object NP array to a string.
        """
        return pytesseract.image_to_string(self.img)

    def img_to_dict(self):
        """
        Converts object NP array to a dictionary with various data.
        """
        return pytesseract.image_to_data(self.img, output_type=Output.DICT)


class ImgPostProcessingOptions:
    """
    Contains set of post processing instructions to be performed on image file loaded as Np array object.
    """

    @staticmethod
    def inverting_img(img_file) -> str:
        """
        inverting colors of the img. Dark to Light and opposite.
        """
        inverted_image = cv2.bitwise_not(img_file)
        file_name = 'vine_labels\services\static\\temp\inverted.jpg'
        cv2.imwrite(file_name, inverted_image)
        return file_name

    def greyscaling(img_file) -> str:
        """
        changing color to grayscale.
        """
        gray_image = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)
        thresh, im_bw = cv2.threshold(gray_image, 100, 250, cv2.THRESH_BINARY)
        filename_gray = 'vine_labels\services\static\\temp\gray.jpg'
        filename_bw = 'vine_labels\services\static\\temp\\bw.jpg'
        cv2.imwrite(filename_gray, gray_image)
        cv2.imwrite(filename_bw, im_bw)
        return filename_bw

    @staticmethod
    def noise_removal(img_file: str, color: bool, filename: str) -> str:
        """
        removing noises from image.
        img_file: String type. Input file to be post processed.
        color: Boolean type. Determines if img_file is color or black and white.
        filename: String type. Name of the output file.
        return: String type. Temporary filename after noise removal.
        """
        if color:
            noise_reduced_image = cv2.fastNlMeansDenoisingColored(img_file, None, 10, 10, 7, 21)
        else:
            noise_reduced_image = cv2.fastNlMeansDenoising(img_file, None, 40, 21, 7)
        cv2.imwrite(filename, noise_reduced_image)
        return filename


class ImgEditorOptions:
    """
    Contains set of edit instructions to be performed on loaded image file.
    """

    @staticmethod
    def rotating_img(img_file) -> str:
        """
        Rotates image base on the check if it is oriented vertical or horizontal.
        return: String type. Temporary filename after noise removal.
        """
        filename = 'vine_labels\services\static\\temp\\rotated.jpg'
        width, height, channels = img_file.shape
        if width > height:
            img_rotated = cv2.rotate(img_file, cv2.ROTATE_180)
            ImgEditorOptions.save_post_processed_img(filename, img_rotated)
        return filename

    @staticmethod
    def resizing_img(img_file, ratio=None) -> str:
        filename = 'vine_labels\services\static\\temp'
        width, height, channels = img_file.shape
        img_resized = cv2.resize(img_file, (height // ratio, width // ratio))
        ImgEditorOptions.save_post_processed_img(filename, img_resized)
        return filename

    @staticmethod
    def save_post_processed_img(filename, post_processed_file):
        if filename not in os.getcwd() + 'vine_labels\services\static\\temp':
            cv2.imwrite(filename, post_processed_file)


class ImageEditor:
    """
    Class creates object which is loaded image file. Class methods are defined as a set of image editorial instructions.
    """
    def __init__(self, img_file):
        self.cv2_opened = OrigImage.cv2_img_obj(img_file)

    def img_resized(self) -> str:
        """
        Method resizes loaded image file.
        return: String type. Temporary filename of the resized image. Used for further post processing.
        """
        return ImgEditorOptions.resizing_img(self.cv2_opened, ratio=5)

    def error(self):
        if self.cv2_opened is None:
            print('\nOriginal Image has not been loaded\n')


class ImagePostProcessed:
    """
    Class initialize image object which is image after editorial operations(class ImageEditor). Image is loaded as NP
    array object.
    """

    def __init__(self, img_file):
        self.img = ImgAsNpArray.open_edited_img(img_file)

    def img_noise_removed(self, filename, color):
        """
        Method removes noises from loaded as NP array image file.
        return: String type. Temporary filename of the post processed image. Used for further text recognition.
        """
        return ImgPostProcessingOptions.noise_removal(self.img, filename=filename, color=color)

    def img_greyscaled(self):
        """
        Method changes color palette in image file loaded as NP array. Color palette is changed from RGB to Black and
        white.
        return: String type. Temporary filename of the post processed image. Used for further text recognition.
        """
        return ImgPostProcessingOptions.greyscaling(self.img)

    def img_inverted(self):
        return ImgPostProcessingOptions.inverting_img(self.img)

    def error(self):
        if self.img is None:
            print('\nEdited Image has not been loaded\n')

class TextFromColorImg:

    filename = 'vine_labels\services\static\\temp\\noises_removed.jpg'

    extracted_text = ''

    @staticmethod
    def extract_text(img_post_processed):
        img_post_processed = ImagePostProcessed(img_post_processed)
        img_noise_removed = img_post_processed.img_noise_removed(filename=TextFromColorImg.filename, color=True)
        data_color = ImgAsData(img_noise_removed)
        TextFromGreyImg.extracted_text = data_color.img_to_string()
        # file1 = open('temp\\my_data_color.txt', 'w')
        # file1.write(my_data_color.img_to_string())


class TextFromGreyImg:

    filename = 'vine_labels\services\static\\temp\\grey_noises.jpg'

    extracted_text = ''

    @staticmethod
    def extract_text(img_post_processed):
        img_grey = ImagePostProcessed(img_post_processed.img_greyscaled())
        img_noise_removed = ImagePostProcessed.img_noise_removed(img_grey, filename=TextFromGreyImg.filename,
                                                                 color=False)
        data_grey = ImgAsData(img_noise_removed)
        TextFromGreyImg.extracted_text = data_grey.img_to_string()
        # file2 = open('temp\my_data_grey.txt', 'w')
        # file2.write(my_data_grey.img_to_string())


