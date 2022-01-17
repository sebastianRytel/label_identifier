from .img_ocr import ImageEditor, ImagePostProcessed, TextFromGreyImg, TextFromColorImg


def initialize_text_extract():
    img_edited = ImageEditor('vine_labels\services\\IMG-0963.jpg')
    img_resized = img_edited.img_resized()
    img_post_processed = ImagePostProcessed(img_resized)
    img_post_processed.error()
    extracted_text_color = TextFromColorImg.extract_text(img_resized)
    extracted_text_grey = TextFromGreyImg.extract_text(img_post_processed)
    return extracted_text_color, extracted_text_grey