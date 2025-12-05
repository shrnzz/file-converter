# This file makes the converters folder a Python package
# It imports all converter classes so they can be easily imported from the converters module

# Import base converter class that all other converters inherit from
from .base_converter import BaseConverter

# Import CSV converter class for converting CSV files
from .csv_converter import CSVConverter

# Import PDF converter class for converting PDF files
from .pdf_converter import PDFConverter

# Import DOCX converter class for converting Word documents
from .docx_converter import DOCXConverter

# Import TXT converter class for converting text files
from .txt_converter import TXTConverter

# This list defines what gets imported when someone does "from converters import *"
__all__ = [
    'BaseConverter',
    'CSVConverter',
    'PDFConverter',
    'DOCXConverter',
    'TXTConverter'
]
