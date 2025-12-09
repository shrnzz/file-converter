#!/usr/bin/env python3
"""
Project verification script - checks that all components are properly configured.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_imports():
    """Verify all required imports work."""
    print("Checking imports...")
    issues = []
    
    try:
        from converters import BaseConverter, CSVConverter, PDFConverter, DOCXConverter, TXTConverter
        print("  ✓ All converters import successfully")
    except ImportError as e:
        issues.append(f"  ✗ Converter import failed: {e}")
    
    try:
        from utils.file_utils import validate_file, get_output_path, get_file_extension, ensure_directory_exists
        print("  ✓ Utility functions import successfully")
    except ImportError as e:
        issues.append(f"  ✗ Utility import failed: {e}")
    
    try:
        from ui.gui import FileConverterGUI, main
        print("  ✓ GUI imports successfully")
    except ImportError as e:
        issues.append(f"  ✗ GUI import failed: {e}")
    
    return issues


def check_converter_interface():
    """Verify converters implement required methods."""
    print("\nChecking converter interfaces...")
    issues = []
    
    from converters import CSVConverter, PDFConverter, DOCXConverter, TXTConverter
    from converters.base_converter import BaseConverter
    
    converters = {
        'CSVConverter': CSVConverter,
        'PDFConverter': PDFConverter,
        'DOCXConverter': DOCXConverter,
        'TXTConverter': TXTConverter,
    }
    
    for name, converter_class in converters.items():
        # Check inheritance
        if not issubclass(converter_class, BaseConverter):
            issues.append(f"  ✗ {name} doesn't inherit from BaseConverter")
        else:
            print(f"  ✓ {name} inherits from BaseConverter")
        
        # Check methods exist
        if not hasattr(converter_class, 'convert'):
            issues.append(f"  ✗ {name} missing convert() method")
        
        if not hasattr(converter_class, 'get_supported_formats'):
            issues.append(f"  ✗ {name} missing get_supported_formats() method")
    
    return issues


def check_files_exist():
    """Verify all expected files exist."""
    print("\nChecking file structure...")
    issues = []
    
    required_files = [
        'main.py',
        'README.md',
        'requirements.txt',
        'DEVELOPMENT.md',
        'converters/__init__.py',
        'converters/base_converter.py',
        'converters/csv_converter.py',
        'converters/pdf_converter.py',
        'converters/docx_converter.py',
        'converters/txt_converter.py',
        'ui/gui.py',
        'utils/file_utils.py',
        'test_converters.py',
    ]
    
    for file in required_files:
        file_path = os.path.join(os.path.dirname(__file__), file)
        if os.path.exists(file_path):
            print(f"  ✓ {file}")
        else:
            issues.append(f"  ✗ Missing: {file}")
    
    return issues


def check_convert_method_signature():
    """Verify all converters have consistent convert() method signature."""
    print("\nChecking method signatures...")
    issues = []
    
    from converters import CSVConverter, PDFConverter, DOCXConverter, TXTConverter
    import inspect
    
    converters = {
        'CSVConverter': CSVConverter,
        'PDFConverter': PDFConverter,
        'DOCXConverter': DOCXConverter,
        'TXTConverter': TXTConverter,
    }
    
    for name, converter_class in converters.items():
        sig = inspect.signature(converter_class.convert)
        params = list(sig.parameters.keys())
        
        # Should be [self, output_path]
        if params == ['self', 'output_path']:
            print(f"  ✓ {name}.convert() has correct signature")
        else:
            issues.append(f"  ✗ {name}.convert() signature is wrong: {params}")
    
    return issues


def main():
    """Run all checks."""
    print("=" * 60)
    print("File Converter - Project Verification")
    print("=" * 60)
    
    all_issues = []
    
    all_issues.extend(check_imports())
    all_issues.extend(check_files_exist())
    all_issues.extend(check_converter_interface())
    all_issues.extend(check_convert_method_signature())
    
    # Print summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    if all_issues:
        print(f"\n✗ Found {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            print(issue)
        return False
    else:
        print("\n✓ All checks passed! Project is ready to use.")
        print("\nTo start the application, run:")
        print("  python main.py")
        print("\nTo test all converters, run:")
        print("  python test_converters.py")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
