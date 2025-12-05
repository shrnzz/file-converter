# TXT Converter module - converts plain text files to other formats

# Import pandas library for working with data files
import pandas as pd

# Import base converter class that we created earlier
from .base_converter import BaseConverter

# Import os module for file operations and path handling
import os

"""
Converter class for handling plain text (.txt) file conversions.
Can convert text files to CSV, Excel, or JSON formats.
Assumes the text file has structured data with delimiters (like spaces or tabs).
"""
class TXTConverter(BaseConverter):

    """
    Return the file formats that text files can be converted to.
    """
    def get_supported_formats(self):
        # TXT can be converted to these formats
        return ['.csv', '.xlsx', '.json']

    """
    Convert a plain text file to another format (CSV, Excel, or JSON).
    """
    def convert(self, output_path, delimiter=None):
        try:
            # Stores the output path for later use
            self.output_path = output_path
            
            # Checks if the input file exists before attempting to convert
            if not self.validate_input():
                print(f"Error: Input file '{self.input_path}' does not exist.")
                return False
            
            print(f"Reading text file: {self.input_path}")
            
            # If no delimiter is specified, use a pattern that matches any whitespace
            # This includes spaces, tabs, and multiple spaces
            if delimiter is None:
                # '\s+' is a regular expression that matches one or more whitespace characters
                delimiter = '\s+'
            
            # Reads the text file into a pandas DataFrame
            # sep=delimiter tells pandas what character separates the columns
            # engine='python' is more flexible with different delimiters
            df = pd.read_csv(self.input_path, sep=delimiter, engine='python')
            
            # Extracts the file extension from the output path
            # For example: 'myfile.csv' -> '.csv'
            # os.path.splitext() returns a tuple: (filename, extension)
            file_extension = os.path.splitext(output_path)[1].lower()
            
            # Converts to the appropriate format based on the file extension
            if file_extension == '.csv':
                # Converts to CSV format
                print("Converting to CSV format...")
                # index=False means don't save the row numbers as a column
                df.to_csv(output_path, index=False)
                
            elif file_extension == '.xlsx':
                # Converts to Excel format
                print("Converting to Excel format...")
                # index=False means don't save the row numbers as a column
                # engine='openpyxl' tells pandas to use the openpyxl library for Excel files
                df.to_excel(output_path, index=False, engine='openpyxl')
                
            elif file_extension == '.json':
                # Converts to JSON format
                print("Converting to JSON format...")
                # orient='records' means each row becomes a separate object
                # indent=2 makes the JSON file readable with proper indentation
                df.to_json(output_path, orient='records', indent=2)
                
            else:
                # If the file extension is not supported, show an error
                print(f"Error: Unsupported output format '{file_extension}'")
                print(f"Supported formats: {', '.join(self.get_supported_formats())}")
                return False
            
            print(f"Conversion successful! File saved to: {output_path}")
            return True
            
        except Exception as e:
            # If any error occurs during conversion, catch and print the error message
            print(f"Error during TXT conversion: {str(e)}")
            print("Make sure your text file has structured data with clear delimiters")
            print("(like spaces, tabs, or commas separating columns)")
            return False
