"""
Module is intended to clear all unnecessary whitespace characters from extracted from image text.
"""

import typing as tp

def clear_extracted_text(text:tp.AnyStr) -> tp.AnyStr:
    """
    Function clears whitespace characters from passed as parameter string.
    return: string
    """
    return ' '.join([word for word in text.split('\n') if word not in [' ', '']])