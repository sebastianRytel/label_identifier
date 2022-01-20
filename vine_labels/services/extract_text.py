"""
Module opens, process, and extract text from an image.
Clear extracted text by removing characters which are not letters.
Returns extracted, cleared text from image after two post processes.
"""

import typing as tp

from .img_ocr import ImageEditor, ImagePostProcessed, TextFromGreyImg, TextFromColorImg
from .extracted_text_editor import clear_extracted_text


def initialize_text_extract() -> tp.Union:
    """
    Function opens original file and call functions which are changes image parameters in order to extract text.
    """
    img_edited = ImageEditor('vine_labels\services\\IMG-0963.jpg')
    img_resized = img_edited.img_resized()
    img_post_processed = ImagePostProcessed(img_resized)
    extracted_text_color = TextFromColorImg.extract_text(img_resized)
    extracted_text_grey = TextFromGreyImg.extract_text(img_post_processed)
    text_color_cleared = clear_extracted_text(extracted_text_color)
    text_grey_cleared = clear_extracted_text(extracted_text_grey)
    return text_grey_cleared, text_color_cleared
