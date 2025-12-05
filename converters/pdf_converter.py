# PDF Converter module - converts PDF files to other formats

# Import Converter class from pdf2docx library for converting PDF to Word documents
from pdf2docx import Converter

# Import the base converter class 
from .base_converter import BaseConverter

"""
Converter class for handling PDF file conversions.
    Currently converts PDF files to Word (.docx) format.
"""
class PDFConverter(BaseConverter):

    """
    Return the file formats that PDF files can be converted to.
    """
    def get_supported_formats(self):
        # PDF can be converted to this format
        return ['.docx']

    """ 
    Convert a PDF file to Word format (.docx).
    """
    def convert(self, output_path):
        try:
            # Store the output path for later use
            self.output_path = output_path
            
            # Check if the input file exists before attempting to convert
            if not self.validate_input():
                print(f"Error: Input file '{self.input_path}' does not exist.")
                return False
            
            # Verify that the output file has a .docx extension
            if not output_path.endswith('.docx'):
                print("Error: Output file must have a .docx extension")
                print(f"Supported formats: {', '.join(self.get_supported_formats())}")
                return False
            
            print(f"Reading PDF file: {self.input_path}")
            print(f"This may take a moment depending on the file size...")
            
            # Creates a Converter object from the pdf2docx library
            # This object is used to convert PDF files to Word documents
            # pdf2docx converts each page of the PDF to a table in the Word document
            converter = Converter(self.input_path)
            
            # Converts all pages of the PDF to the Word document
            print("Converting PDF to Word format...")
            converter.convert(output_path)
            
            # Closes the converter to free up memory and resources
            # This is important to do after conversion is complete
            converter.close()
            
            print(f"Conversion successful! File saved to: {output_path}")
            return True
            
        except Exception as e:
            # If any error occurs during conversion, catch and print the error message
            print(f"Error during PDF conversion: {str(e)}")
            return False
