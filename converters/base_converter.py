# This is the base converter module that defines the abstract class for all file converters
# All specific converters (CSV, PDF, DOCX, etc.) will inherit from this class

# Import the ABC (Abstract Base Class) module to create abstract classes
from abc import ABC, abstractmethod

"""
Abstract base class for all file converters.
This class defines the interface that all converter subclasses must implement.
"""
class BaseConverter(ABC):

    """
    Initializes the converter with an input file path.
    """
    def __init__(self, input_path):
        self.input_path = input_path
        self.output_path = None

    """
    Abstract method to convert the file.
    Every converter class must implement this method.
    True if conversion was successful, otherwise False
    """
    @abstractmethod
    def convert(self, output_path):
        pass

    """
    Abstract method to get the supported file formats for this converter.
    Every converter class must implement this method.
    This will return a list of supported file extensions.
    """
    @abstractmethod
    def get_supported_formats(self):
        pass

    """
    Validate that the input file exists.
    This method can be called by subclasses to check if input file is valid.
    """
    def validate_input(self):
        import os
        return os.path.isfile(self.input_path)
