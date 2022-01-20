"""
When called module creates Singleton object and allows to create logfile and write events into txt file.
"""

import os.path

class LogFile:
    _instance = None

    def __new__(cls, *args, **kwargs) -> object:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def write_log(log_text: str)-> None:
        """
        Opens text file using context manager, writes events passed into write_log function as argument.
        """
        with open('vine_labels\services\logfile.txt', 'a') as f:
            f.write(log_text)
