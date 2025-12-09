import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.ttk import Combobox
import threading
import os
from pathlib import Path
import sys

# Add parent directory to path to import converters
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from converters.csv_converter import CSVConverter
from converters.pdf_converter import PDFConverter
from converters.docx_converter import DOCXConverter
from converters.txt_converter import TXTConverter
from utils.file_utils import validate_file, get_output_path, get_file_extension, ensure_directory_exists


class FileConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)
        
        # Theme state
        self.theme = "dark"
        # Default color scheme (dark) - minimalist
        self.bg_primary = "#0f0f0f"      # Pure deep charcoal
        self.bg_secondary = "#1a1a1a"    # Slightly lifted shadows
        self.accent_color = "#3a3a3a"    # Neutral accent (no chroma)
        self.accent_hover = "#2a2a2a"    # Slightly lighter on hover
        self.text_primary = "#e5e5e5"    # Soft gray-white
        self.text_muted = "#9a9a9a"      # Gentle muted gray
        self.border_color = "#2a2a2a"    # Subtle structural lines
        self.success_color = "#4caf50"   # Green
        self.error_color = "#f44336"     # Red
        self.warning_color = "#ff9800"   # Orange

        # Font
        self.font_family = "Helvetica"

        self.root.configure(bg=self.bg_primary)
        
        # Configure style with modern theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure colors and fonts
        self.setup_styles()
        
        # Converter mapping
        self.converters = {
            "CSV": CSVConverter,
            "PDF": PDFConverter,
            "DOCX": DOCXConverter,
            "TXT": TXTConverter,
        }
        
        # Input/Output format mappings
        self.format_options = {
            "CSV": [".csv", ".xlsx", ".json", ".html"],
            "PDF": [".docx"],
            "DOCX": [".txt"],
            "TXT": [".csv", ".xlsx", ".json"],
        }
        
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.conversion_running = False
        
        self.setup_ui()
    
    def setup_styles(self):
        """Configure all style settings for modern appearance."""
        # Configure frame styles
        self.style.configure("TFrame", background=self.bg_primary)
        # Card frames should be visually flat and match primary for minimalism
        self.style.configure("Card.TFrame", background=self.bg_primary, relief="flat")
        
        # Configure label styles
        self.style.configure("TLabel", background=self.bg_primary, foreground=self.text_primary, font=(self.font_family, 10))
        self.style.configure("Title.TLabel", font=(self.font_family, 18, "bold"), foreground=self.text_primary)
        self.style.configure("Header.TLabel", font=(self.font_family, 11, "bold"), foreground=self.text_primary)
        self.style.configure("Subtitle.TLabel", font=(self.font_family, 9), foreground=self.text_muted)
        # LabelFrame styles to avoid default gray panels
        self.style.configure("TLabelframe", background=self.bg_primary)
        self.style.configure("TLabelframe.Label", background=self.bg_primary, foreground=self.text_primary, font=(self.font_family, 11, "bold"))
        
        # Configure button styles
        self.style.configure("Accent.TButton", font=(self.font_family, 10, "bold"))
        self.style.configure("Secondary.TButton", font=(self.font_family, 10))
        
        # Configure combobox styles with explicit fieldbackground and foreground
        self.style.configure("TCombobox", font=(self.font_family, 10), fieldbackground=self.bg_primary, background=self.bg_primary, foreground=self.text_primary)
        # Map ensures the field itself uses the correct colors
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", self.bg_primary)],
                       background=[("readonly", self.bg_primary)],
                       foreground=[("readonly", self.text_primary)])
        
        # Configure progressbar
        self.style.configure("TProgressbar", background=self.success_color, troughcolor=self.bg_primary)

    def apply_theme(self):
        """Apply colors to styles and widgets based on current theme."""
        if self.theme == "dark":
            # Dark theme colors (from user-provided palette)
            self.bg_primary = "#0f0f0f"
            self.bg_secondary = "#1a1a1a"
            self.accent_color = "#3a3a3a"
            self.accent_hover = "#2a2a2a"
            self.text_primary = "#e5e5e5"
            self.text_muted = "#9a9a9a"
            self.border_color = "#2a2a2a"
        else:
            # Light theme colors (from user-provided palette)
            self.bg_primary = "#f8f8f8"
            self.bg_secondary = "#efefef"
            self.accent_color = "#cfcfcf"
            self.accent_hover = "#d7d7d7"
            self.text_primary = "#1a1a1a"
            self.text_muted = "#7c7c7c"
            self.border_color = "#d7d7d7"

        # Update root and styles
        try:
            self.root.configure(bg=self.bg_primary)
        except Exception:
            pass

        self.setup_styles()

        # Header
        try:
            self.header_frame.config(bg=self.bg_primary)
            self.title_label.config(bg=self.bg_primary, fg=self.text_primary, font=(self.font_family, 20, "bold"))
            self.theme_button.config(bg=self.bg_primary, fg=self.text_muted, text=("☀️ Light" if self.theme == "dark" else "🌙 Dark"))
        except Exception:
            pass

        # Input / Output frames and displays
        try:
            self.input_file_label.config(bg=self.bg_primary, fg=self.text_primary, font=(self.font_family, 10, "bold"))
            self.output_file_label.config(bg=self.bg_primary, fg=self.text_primary, font=(self.font_family, 10, "bold"))
            self.input_frame.config(bg=self.bg_primary, highlightbackground=self.border_color)
            self.input_display.config(bg=self.bg_primary, fg=(self.text_primary if self.input_file_path.get() else self.text_muted), font=(self.font_family, 9))
            self.browse_btn.config(bg=self.accent_color, fg=self.text_primary, font=(self.font_family, 9))

            self.output_frame.config(bg=self.bg_primary, highlightbackground=self.border_color)
            self.output_display.config(bg=self.bg_primary, fg=(self.text_primary if self.output_file_path.get() else self.text_muted), font=(self.font_family, 9))
            self.browse_out_btn.config(bg=self.accent_color, fg=self.text_primary, font=(self.font_family, 9))
        except Exception:
            pass

        # Progress label and bar
        try:
            self.progress_label.config(bg=self.bg_primary)
            # Update format labels too
            self.input_format_label.config(bg=self.bg_primary, fg=self.text_primary, font=(self.font_family, 10, "bold"))
            self.output_format_label.config(bg=self.bg_primary, fg=self.text_primary, font=(self.font_family, 10, "bold"))
            # progress bar style is handled by ttk style
        except Exception:
            pass

        # Buttons
        try:
            self.convert_button.config(bg=self.accent_color, fg=self.text_primary, font=(self.font_family, 11, "bold"))
            self.clear_button.config(bg=self.bg_primary, fg=self.text_muted, font=(self.font_family, 11))
            self.exit_button.config(bg=self.bg_primary, fg=self.text_muted, font=(self.font_family, 11))
        except Exception:
            pass
    
    def setup_ui(self):
        """Create the GUI components with modern styling."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        self.header_frame = tk.Frame(main_frame, bg=self.accent_color, height=80)
        self.header_frame.pack(fill=tk.X, padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            self.header_frame,
            text="📁 File Converter",
            font=(self.font_family, 20, "bold"),
            bg=self.bg_primary,
            fg=self.text_primary
        )
        self.title_label = title_label
        self.title_label.pack(pady=15)
        
        # subtitle removed per user request

        # Theme toggle button (placed in header, right)
        self.theme_button = tk.Button(
            self.header_frame,
            text="☀️ Light",
            command=self.toggle_theme,
            bg=self.bg_primary,
            fg=self.text_muted,
            font=(self.font_family, 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
        )
        self.theme_button.place(relx=0.95, rely=0.18, anchor=tk.NE)
        
        # Content area with padding
        content_frame = ttk.Frame(main_frame, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # File Selection Section
        file_section = ttk.LabelFrame(content_frame, text="📂 File Selection", padding="15")
        file_section.pack(fill=tk.X, pady=(0, 15))
        
        # Input file with custom styling
        self.input_file_label = tk.Label(file_section, text="Input File:", font=(self.font_family, 10, "bold"), bg=self.bg_primary, fg=self.text_primary)
        self.input_file_label.pack(anchor=tk.W, pady=(0, 5))
        
        # input/output frames use primary background and subtle border for minimalism
        self.input_frame = tk.Frame(file_section, bg=self.bg_primary, highlightthickness=1, highlightbackground=self.border_color)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_display = tk.Label(
            self.input_frame,
            textvariable=self.input_file_path,
            font=(self.font_family, 9),
            bg=self.bg_primary,
            fg=(self.text_primary if self.input_file_path.get() else self.text_muted),
            wraplength=300,
            justify=tk.LEFT,
            padx=10,
            pady=8
        )
        self.input_display.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Browse buttons with enhanced styling
        self.browse_btn = tk.Button(
            self.input_frame,
            text="Browse",
            command=self.select_input_file,
            bg=self.accent_color,
            fg=self.text_primary,
            font=(self.font_family, 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.browse_btn.pack(side=tk.RIGHT, padx=5, pady=2)
        self.browse_btn.bind("<Enter>", lambda e: self.browse_btn.config(bg=self.accent_hover))
        self.browse_btn.bind("<Leave>", lambda e: self.browse_btn.config(bg=self.accent_color))
        
        # Output file
        self.output_file_label = tk.Label(file_section, text="Output File:", font=(self.font_family, 10, "bold"), bg=self.bg_primary, fg=self.text_primary)
        self.output_file_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.output_frame = tk.Frame(file_section, bg=self.bg_primary, highlightthickness=1, highlightbackground=self.border_color)
        self.output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_display = tk.Label(
            self.output_frame,
            textvariable=self.output_file_path,
            font=(self.font_family, 9),
            bg=self.bg_primary,
            fg=(self.text_primary if self.output_file_path.get() else self.text_muted),
            wraplength=300,
            justify=tk.LEFT,
            padx=10,
            pady=8
        )
        self.output_display.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_out_btn = tk.Button(
            self.output_frame,
            text="Browse",
            command=self.select_output_file,
            bg=self.accent_color,
            fg=self.text_primary,
            font=(self.font_family, 9, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.browse_out_btn.pack(side=tk.RIGHT, padx=5, pady=2)
        self.browse_out_btn.bind("<Enter>", lambda e: self.browse_out_btn.config(bg=self.accent_hover))
        self.browse_out_btn.bind("<Leave>", lambda e: self.browse_out_btn.config(bg=self.accent_color))
        
        # Conversion Settings Section
        settings_frame = ttk.LabelFrame(content_frame, text="⚙️ Conversion Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Input format with label
        self.input_format_label = tk.Label(settings_frame, text="Input Format:", font=(self.font_family, 10, "bold"), bg=self.bg_primary, fg=self.text_primary)
        self.input_format_label.grid(row=0, column=0, sticky=tk.W, pady=8)
        
        self.input_format_var = tk.StringVar()
        self.input_format_combo = Combobox(
            settings_frame,
            textvariable=self.input_format_var,
            values=list(self.converters.keys()),
            state="readonly",
            width=25,
            font=(self.font_family, 10)
        )
        self.input_format_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=8)
        self.input_format_combo.bind("<<ComboboxSelected>>", self.update_output_formats)
        
        # Output format with label
        self.output_format_label = tk.Label(settings_frame, text="Output Format:", font=(self.font_family, 10, "bold"), bg=self.bg_primary, fg=self.text_primary)
        self.output_format_label.grid(row=1, column=0, sticky=tk.W, pady=8)
        
        self.output_format_var = tk.StringVar()
        self.output_format_combo = Combobox(
            settings_frame,
            textvariable=self.output_format_var,
            state="readonly",
            width=25,
            font=(self.font_family, 10)
        )
        self.output_format_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=8)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(content_frame, text="⏱️ Progress", padding="15")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.StringVar(value="Ready to convert")
        self.progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_var,
            font=(self.font_family, 10),
            bg=self.bg_primary,
            fg=self.success_color
        )
        self.progress_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate", length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 0))
        
        # Buttons Section with enhanced styling
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.convert_button = tk.Button(
            button_frame,
            text="🔄 Convert",
            command=self.start_conversion,
            bg=self.accent_color,
            fg=self.text_primary,
            font=(self.font_family, 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        self.convert_button.bind("<Enter>", lambda e: self.convert_button.config(bg=self.accent_hover))
        self.convert_button.bind("<Leave>", lambda e: self.convert_button.config(bg=self.accent_color))
        
        clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_fields,
            bg=self.bg_primary,
            fg=self.text_muted,
            font=(self.font_family, 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2"
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        clear_button.bind("<Enter>", lambda e: clear_button.config(fg=self.text_primary))
        clear_button.bind("<Leave>", lambda e: clear_button.config(fg=self.text_muted))
        
        exit_button = tk.Button(
            button_frame,
            text="❌ Exit",
            command=self.root.quit,
            bg=self.bg_primary,
            fg=self.text_muted,
            font=(self.font_family, 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2"
        )
        exit_button.pack(side=tk.LEFT)
        exit_button.bind("<Enter>", lambda e: exit_button.config(fg=self.text_primary))
        exit_button.bind("<Leave>", lambda e: exit_button.config(fg=self.text_muted))

        # Save references for dynamic theme updates
        self.clear_button = clear_button
        self.exit_button = exit_button

        # Ensure theme reflects initial state
        self.apply_theme()

    def toggle_theme(self):
        """Toggle between dark and light themes."""
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()
    
    def select_input_file(self):
        """Open file dialog to select input file."""
        file_path = filedialog.askopenfilename(
            title="Select a file to convert",
            filetypes=[
                ("All Files", "*.*"),
                ("CSV Files", "*.csv"),
                ("PDF Files", "*.pdf"),
                ("Word Files", "*.docx"),
                ("Text Files", "*.txt"),
            ]
        )
        
        if file_path:
            self.input_file_path.set(file_path)
            # Auto-detect input format from file extension
            file_ext = get_file_extension(file_path).lower()  # e.g., '.csv'
            # Map extensions to converter types
            ext_to_format = {
                '.csv': 'CSV',
                '.pdf': 'PDF',
                '.docx': 'DOCX',
                '.txt': 'TXT',
            }
            if file_ext in ext_to_format:
                detected_format = ext_to_format[file_ext]
                self.input_format_var.set(detected_format)
                # Auto-update output formats based on detected input
                self.update_output_formats()
    
    def select_output_file(self):
        """Open file dialog to select output file path."""
        if not self.output_format_var.get():
            messagebox.showwarning("Warning", "Please select an output format first.")
            return
        
        output_ext = self.output_format_var.get()
        file_path = filedialog.asksaveasfilename(
            defaultextension=output_ext,
            filetypes=[("Files", f"*{output_ext}"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.output_file_path.set(file_path)
    
    def update_output_formats(self, event=None):
        """Update available output formats based on input format."""
        input_fmt = self.input_format_var.get()
        if input_fmt:
            formats = self.format_options.get(input_fmt, [])
            self.output_format_combo["values"] = formats
            if formats:
                self.output_format_combo.set(formats[0])
            self.output_file_path.set("")
    
    def start_conversion(self):
        """Start the file conversion process."""
        # Validation
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an input file.")
            return
        
        if not self.input_format_var.get():
            messagebox.showerror("Error", "Please select an input format.")
            return
        
        if not self.output_format_var.get():
            messagebox.showerror("Error", "Please select an output format.")
            return
        
        if not self.output_file_path.get():
            messagebox.showerror("Error", "Please select an output file path.")
            return
        
        # Run conversion in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.perform_conversion)
        thread.daemon = True
        thread.start()
    
    def perform_conversion(self):
        """Execute the file conversion."""
        try:
            self.conversion_running = True
            self.convert_button.config(state=tk.DISABLED)
            self.progress_bar.start()
            self.progress_var.set("⏳ Converting... (in progress)")
            self.progress_label.config(fg=self.warning_color)
            
            input_file = self.input_file_path.get()
            output_file = self.output_file_path.get()
            input_format = self.input_format_var.get()
            output_format = self.output_format_var.get()
            
            # Ensure output directory exists
            ensure_directory_exists(output_file)
            
            # Get the appropriate converter
            converter_class = self.converters[input_format]
            converter = converter_class(input_file)
            
            # Perform conversion
            success = converter.convert(output_file)
            
            self.progress_bar.stop()
            
            if success:
                self.progress_var.set("✓ Conversion successful!")
                self.progress_label.config(fg=self.success_color)
                messagebox.showinfo("Success", f"File converted successfully!\nOutput: {output_file}")
            else:
                self.progress_var.set("✗ Conversion failed")
                self.progress_label.config(fg=self.error_color)
                messagebox.showerror("Error", "Conversion failed. Please check the file format and try again.")
        
        except Exception as e:
            self.progress_bar.stop()
            self.progress_var.set("✗ Error during conversion")
            self.progress_label.config(fg=self.error_color)
            messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")
        
        finally:
            self.conversion_running = False
            self.convert_button.config(state=tk.NORMAL)
    
    def clear_fields(self):
        """Clear all input fields."""
        self.input_file_path.set("")
        self.output_file_path.set("")
        self.input_format_var.set("")
        self.output_format_var.set("")
        self.progress_var.set("Ready to convert")
        self.progress_label.config(fg=self.success_color)


def main():
    root = tk.Tk()
    app = FileConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
