"""PyQt6 GUI implementation for Bambu2Prusa converter.

This is a basic implementation that provides a minimal PyQt6 interface.
It demonstrates the modular frontend architecture.
"""

import logging
import sys
from pathlib import Path

try:
    from PyQt6.QtWidgets import (
        QApplication,
        QFileDialog,
        QLabel,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )
    from PyQt6.QtCore import Qt
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False


from bambu_to_prusa.converter import BambuToPrusaConverter
from bambu_to_prusa.settings import SettingsManager
from frontends.common.helpers import first_existing_dir


class BambuToPrusaWindow(QMainWindow):
    """Main window for PyQt6 GUI."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.converter = BambuToPrusaConverter()
        self.input_file = ""
        self.output_file = ""
        
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Bambu2Prusa Converter (PyQt6)")
        self.setMinimumSize(500, 400)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("Bambu ➜ Prusa Converter")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("PyQt6 interface for converting Bambu Studio 3mf files")
        subtitle.setStyleSheet("font-size: 12px; color: gray; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Input file button
        self.input_button = QPushButton("Select Input Bambu 3mf")
        self.input_button.clicked.connect(self.select_input)
        self.input_button.setMinimumHeight(40)
        layout.addWidget(self.input_button)
        
        # Input file label
        self.input_label = QLabel("No input file selected")
        self.input_label.setStyleSheet("margin: 5px; padding: 5px;")
        layout.addWidget(self.input_label)
        
        # Output file button
        self.output_button = QPushButton("Select Output Prusa 3mf")
        self.output_button.clicked.connect(self.select_output)
        self.output_button.setMinimumHeight(40)
        layout.addWidget(self.output_button)
        
        # Output file label
        self.output_label = QLabel("No output file selected")
        self.output_label.setStyleSheet("margin: 5px; padding: 5px;")
        layout.addWidget(self.output_label)
        
        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        self.convert_button.setMinimumHeight(50)
        self.convert_button.setStyleSheet(
            "background-color: #5865f2; color: white; font-weight: bold; margin-top: 20px;"
        )
        layout.addWidget(self.convert_button)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("margin: 10px; padding: 10px;")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        layout.addStretch()

    def select_input(self):
        """Open file dialog to select input file."""
        initial_dir = first_existing_dir(self.settings.last_input_dir) or str(Path.home())
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Input Bambu 3mf File",
            initial_dir,
            "3MF Files (*.3mf);;All Files (*)"
        )
        
        if file_path:
            self.input_file = file_path
            self.input_label.setText(f"Input: {Path(file_path).name}")
            self.settings.update_last_input_dir(str(Path(file_path).parent))
            self.status_label.setText(f"Input file selected: {Path(file_path).name}")

    def select_output(self):
        """Open file dialog to select output file."""
        initial_dir = first_existing_dir(
            self.settings.last_output_dir,
            self.settings.last_input_dir,
        ) or str(Path.home())
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output Prusa 3mf File",
            initial_dir,
            "3MF Files (*.3mf);;All Files (*)"
        )
        
        if file_path:
            # Ensure .3mf extension
            if not file_path.lower().endswith('.3mf'):
                file_path += '.3mf'
            
            self.output_file = file_path
            self.output_label.setText(f"Output: {Path(file_path).name}")
            self.settings.update_last_output_dir(str(Path(file_path).parent))
            self.status_label.setText(f"Output file selected: {Path(file_path).name}")

    def convert(self):
        """Perform the conversion."""
        if not self.input_file:
            QMessageBox.warning(self, "No Input File", "Please select an input file.")
            return
        
        if not self.output_file:
            QMessageBox.warning(self, "No Output File", "Please select an output file.")
            return
        
        try:
            self.status_label.setText("Converting...")
            self.convert_button.setEnabled(False)
            QApplication.processEvents()  # Update UI
            
            self.converter.convert_archive(self.input_file, self.output_file)
            
            self.status_label.setText(f"✓ Conversion successful! Output: {Path(self.output_file).name}")
            QMessageBox.information(
                self,
                "Success",
                f"File converted successfully!\n\nOutput: {self.output_file}"
            )
        except Exception as exc:
            logging.error("Conversion failed: %s", exc)
            self.status_label.setText(f"✗ Error: {exc}")
            QMessageBox.critical(
                self,
                "Conversion Failed",
                f"An error occurred during conversion:\n\n{exc}"
            )
        finally:
            self.convert_button.setEnabled(True)


def main():
    """Main entrypoint for PyQt6 GUI."""
    if not PYQT6_AVAILABLE:
        print("Error: PyQt6 is not installed.", file=sys.stderr)
        print("Install it with: pip install PyQt6", file=sys.stderr)
        sys.exit(1)
    
    logging.basicConfig(level=logging.INFO)
    
    app = QApplication(sys.argv)
    window = BambuToPrusaWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
