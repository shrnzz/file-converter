# DOCX Converter module - converts Word (.docx) files to other formats

# Imports Document class from python-docx library for reading Word documents
from docx import Document

# Import the base converter class that we created earlier
from .base_converter import BaseConverter

# Import os module for file operations and path handling
import os


class DOCXConverter(BaseConverter):
    """
    Converter class for handling Word (.docx) file conversions.
    Can extract text from Word documents and save as plain text.
    """

    """
    Return the file formats that Word files can be converted to.
    """
    def get_supported_formats(self):
        # DOCX can be converted to these formats
        return ['.txt']

    """
    Convert a Word (.docx) file to another format (plain text).
    """
    def convert(self, output_path):
        try:
            # Store the output path for later use
            self.output_path = output_path
            
            # Checks if the input file exists before attempting to convert
            if not self.validate_input():
                print(f"Error: Input file '{self.input_path}' does not exist.")
                return False
            
            print(f"Reading Word document: {self.input_path}")
            
            # Open the Word document using python-docx library
            # A Document object represents a .docx file
            doc = Document(self.input_path)
            
            # Extract the file extension from the output path
            # For example: 'myfile.txt' -> '.txt'
            # os.path.splitext() returns a tuple: (filename, extension)
            file_extension = os.path.splitext(output_path)[1].lower()
            
            # Checks if the output format is supported
            if file_extension == '.txt':
                # Converts to plain text format
                print("Converting to plain text format...")
                
                # Creates an empty list to store all the text from the document
                text_content = []
                
                # Loops through each paragraph in the Word document
                # paragraphs is a list of all text blocks in the document
                for paragraph in doc.paragraphs:
                    # Adds the text from each paragraph to our list
                    text_content.append(paragraph.text)
                
                # Joins all paragraphs with newlines to create the final text
                # '\n' means add a new line between each paragraph
                final_text = '\n'.join(text_content)
                
                # Opens the output file and writes the text to it
                # 'w' means open for writing
                # encoding='utf-8' ensures we handle special characters correctly
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(final_text)
                
                print(f"Conversion successful! File saved to: {output_path}")
                return True
                
            else:
                # If the file extension is not supported, show an error
                print(f"Error: Unsupported output format '{file_extension}'")
                print(f"Supported formats: {', '.join(self.get_supported_formats())}")
                return False
            
        except Exception as e:
            # If any error occurs during conversion, catch and print the error message
            print(f"Error during DOCX conversion: {str(e)}")
            return False
