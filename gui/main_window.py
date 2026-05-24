import sys
from pathlib import Path

def resource_path(relative_path):

    if hasattr(sys, "_MEIPASS"):
        return str(
            Path(sys._MEIPASS) / relative_path
        )

    return relative_path

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QMessageBox,
    QGroupBox,
    QFormLayout
)

from PySide6.QtGui import QIcon

import builder.espressif as espressif
import builder.avr as avr

from builder.manifest import create_manifest

from builder.validators import (
    validate_manifest,
    validate_files
)

from builder.package_writer import (
    write_package
)


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "KitFW Builder"
        )

        self.setWindowIcon(
            QIcon(resource_path("assets/logo.ico"))
        )

        self.resize(
            500,
            450
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.setMinimumSize(500, 450)

        # ------------------------
        # Target
        # ------------------------
        layout.addWidget(QLabel("Target"))
        
        self.target_combo = QComboBox()
        self.target_combo.addItems([
            "espressif",  # Single ESP target
            "avr"
        ])
        
        self.target_combo.currentTextChanged.connect(
            self.on_target_changed
        )
        
        layout.addWidget(self.target_combo)

        # ------------------------
        # ESP Configuration (initially hidden)
        # ------------------------
        self.esp_group = QGroupBox("ESP Configuration")
        self.esp_group.setVisible(False)
        
        esp_layout = QFormLayout()
        
        # Chip selection dropdown
        self.esp_chip = QComboBox()
        self.esp_chip.addItems([
            "esp32",
            "esp32s3",
            "esp32c3",
            "esp32c6",
            "esp32h2",
            "esp8266"
        ])
        self.esp_chip.setCurrentText("esp32")
        esp_layout.addRow("Chip:", self.esp_chip)
        
        # Flash mode (optional, for advanced users)
        self.esp_flash_mode = QComboBox()
        self.esp_flash_mode.addItems(["dio", "qio", "dout", "qout"])
        self.esp_flash_mode.setCurrentText("dio")
        esp_layout.addRow("Flash Mode:", self.esp_flash_mode)
        
        # Flash size (optional)
        self.esp_flash_size = QComboBox()
        self.esp_flash_size.addItems(["detect", "2MB", "4MB", "8MB", "16MB"])
        self.esp_flash_size.setCurrentText("detect")
        esp_layout.addRow("Flash Size:", self.esp_flash_size)
        
        # Flash frequency (optional)
        self.esp_flash_freq = QComboBox()
        self.esp_flash_freq.addItems(["40m", "80m", "26m", "20m"])
        self.esp_flash_freq.setCurrentText("40m")
        esp_layout.addRow("Flash Freq:", self.esp_flash_freq)
        
        help_label = QLabel(
            "<small><i>Tip: Flash mode/size/freq are optional - only needed for custom bootloaders</i></small>"
        )
        help_label.setWordWrap(True)
        esp_layout.addRow("", help_label)
        
        self.esp_group.setLayout(esp_layout)
        layout.addWidget(self.esp_group)

        # ------------------------
        # AVR Configuration (initially hidden)
        # ------------------------

        self.avr_group = QGroupBox("AVR Configuration")
        self.avr_group.setVisible(False)
        
        avr_layout = QFormLayout()
        
        # MCU dropdown with common AVR chips
        self.avr_mcu = QComboBox()
        self.avr_mcu.setEditable(True)  # Allow custom entries
        self.avr_mcu.addItems([
            "atmega328p",
            "atmega328pb",
            "atmega32u4",
            "atmega2560",
            "atmega1280",
            "atmega168",
            "atmega8",
            "attiny85",
            "attiny45",
            "atmega644p",
            "atmega1284p"
        ])
        self.avr_mcu.setCurrentText("atmega328p")
        avr_layout.addRow("MCU:", self.avr_mcu)
        
        # Programmer dropdown with common programmers
        self.avr_programmer = QComboBox()
        self.avr_programmer.setEditable(True)  # Allow custom entries
        self.avr_programmer.addItems([
            "arduino",
            "arduino_as_isp",
            "usbasp",
            "avrisp",
            "avrispmkii",
            "avrdude",
            "buspirate",
            "stk500",
            "stk500v2",
            "stk600",
            "dragon_isp",
            "dragon_jtag",
            "dragon_pp",
            "dragon_hvsp",
            "jtag2isp",
            "jtag2dw",
            "jtag2mkii",
            "jtag2fast",
            "jtag2slow",
            "pickit2",
            "pickit3",
            "linuxgpio",
            "ft232r"
        ])
        self.avr_programmer.setCurrentText("arduino")
        avr_layout.addRow("Programmer:", self.avr_programmer)
        
        # Baud rate dropdown with common speeds
        self.avr_baud_rates = QComboBox()
        self.avr_baud_rates.setEditable(True)  # Allow custom entries
        self.avr_baud_rates.addItems([
            "115200,57600",      # Common for Arduino Uno/Nano (new bootloader)
            "57600,115200",      # Alternative order
            "9600",              # Old/slow devices
            "19200",
            "38400",
            "115200",            # Fast, common default
            "230400",            # Very fast (some bootloaders)
            "115200,57600,9600", # Multiple fallbacks
            "57600",             # Common for older bootloaders
            "1200"               # For flashing via DFU/reset
        ])
        self.avr_baud_rates.setCurrentText("115200,57600")
        avr_layout.addRow("Baud Rates (comma-separated):", self.avr_baud_rates)
        
        # Help text
        help_label = QLabel(
            "<small><i>Tip: You can type custom values. Baud rates are tried in order.</i></small>"
        )
        help_label.setWordWrap(True)
        avr_layout.addRow("", help_label)
        
        self.avr_group.setLayout(avr_layout)
        layout.addWidget(self.avr_group)

        # ------------------------
        # Build Folder
        # ------------------------

        layout.addWidget(
            QLabel("Build Folder")
        )

        folder_layout = QHBoxLayout()

        self.folder_edit = QLineEdit()

        folder_button = QPushButton(
            "Browse"
        )

        folder_button.clicked.connect(
            self.browse_folder
        )

        folder_layout.addWidget(
            self.folder_edit
        )

        folder_layout.addWidget(
            folder_button
        )

        layout.addLayout(
            folder_layout
        )

        # ------------------------
        # Package Name
        # ------------------------

        layout.addWidget(
            QLabel("Package Name")
        )

        self.name_edit = QLineEdit()

        layout.addWidget(
            self.name_edit
        )

        # ------------------------
        # Version
        # ------------------------

        layout.addWidget(
            QLabel("Version")
        )

        self.version_edit = QLineEdit()
        self.version_edit.setText("1.0.0")  # Default version

        layout.addWidget(
            self.version_edit
        )

        # ------------------------
        # Output File
        # ------------------------

        layout.addWidget(
            QLabel("Output File")
        )

        output_layout = QHBoxLayout()

        self.output_edit = QLineEdit()

        output_button = QPushButton(
            "Browse"
        )

        output_button.clicked.connect(
            self.browse_output
        )

        output_layout.addWidget(
            self.output_edit
        )

        output_layout.addWidget(
            output_button
        )

        layout.addLayout(
            output_layout
        )

        # ------------------------
        # Build Button
        # ------------------------

        self.build_button = QPushButton(
            "Build Package"
        )

        self.build_button.clicked.connect(
            self.build_package
        )

        layout.addWidget(
            self.build_button
        )

        # ------------------------
        # Status
        # ------------------------

        self.status_label = QLabel(
            "Ready"
        )

        layout.addWidget(
            self.status_label
        )

        self.setLayout(layout)

        self.on_target_changed(self.target_combo.currentText())

    # ===================================
    # Target Changed Handler
    # ===================================

    def on_target_changed(self, target: str):
        """Show/hide configuration based on selected target"""
        self.esp_group.setVisible(target == "espressif")
        self.avr_group.setVisible(target == "avr")
        
        # Adjust window size
        if target == "espressif":
            self.resize(500, 580)
        elif target == "avr":
            self.resize(500, 550)
        else:
            self.resize(500, 450)

    def get_esp_config(self) -> dict:
        """Get ESP configuration from UI"""
        return {
            "chip": self.esp_chip.currentText(),
            "flash_mode": self.esp_flash_mode.currentText(),
            "flash_size": self.esp_flash_size.currentText(),
            "flash_freq": self.esp_flash_freq.currentText()
        }
    
    # ===================================
    # Get AVR Configuration
    # ===================================

    def get_avr_config(self) -> dict | None:
        """Get AVR configuration from UI, returns None if not AVR target"""
        if self.target_combo.currentText() != "avr":
            return None
        
        # Get MCU (supports both dropdown selection and custom text)
        mcu = self.avr_mcu.currentText().strip()
        if not mcu:
            raise ValueError("MCU is required for AVR target")
        
        # Get programmer
        programmer = self.avr_programmer.currentText().strip()
        if not programmer:
            raise ValueError("Programmer is required for AVR target")
        
        # Parse baud rates
        baud_rates_text = self.avr_baud_rates.currentText().strip()
        if baud_rates_text:
            try:
                baud_rates = [int(b.strip()) for b in baud_rates_text.split(",") if b.strip()]
                if not baud_rates:
                    baud_rates = [115200, 57600]  # Default
            except ValueError:
                raise ValueError("Baud rates must be comma-separated integers")
        else:
            baud_rates = [115200, 57600]  # Default
        
        return {
            "mcu": mcu,
            "programmer": programmer,
            "baud_rates": baud_rates
        }

    # ===================================
    # Folder Browser
    # ===================================

    def browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Build Folder"
        )

        if folder:

            self.folder_edit.setText(
                folder
            )

    # ===================================
    # Output Browser
    # ===================================

    def browse_output(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Package",
            "",
            "KitFW Package (*.kitfw)"
        )

        if filename:

            if not filename.endswith(
                ".kitfw"
            ):
                filename += ".kitfw"

            self.output_edit.setText(
                filename
            )

    # ===================================
    # Build Package
    # ===================================

    def build_package(self):
        try:
            target = self.target_combo.currentText()
            folder = self.folder_edit.text()
            name = self.name_edit.text()
            version = self.version_edit.text()
            output = self.output_edit.text()
            
            # Validate required fields
            if not all([folder, name, version, output]):
                raise ValueError("All fields are required")
            
            # Get target-specific config
            avr_config = None
            esp_config = None
            
            if target == "espressif":
                from builder.espressif import find_artifacts
                esp_config = self.get_esp_config()
            elif target == "avr":
                from builder.avr import find_artifacts
                avr_config = self.get_avr_config()
            else:
                raise ValueError(f"Unsupported target: {target}")
            
            # Find artifacts
            files = find_artifacts(folder)
            
            # Validate we found something
            if not any(files.values()):
                raise Exception(f"No firmware files found in {folder}")
            
            # Create manifest
            manifest = create_manifest(
                name,
                version,
                target,
                files,
                avr_config,
                esp_config
            )
            
            # Validate and write
            validate_manifest(manifest)
            validate_files(manifest, files)
            write_package(output, manifest, files)
            
            self.status_label.setText("Package created successfully")
            QMessageBox.information(self, "Success", "Package created successfully.")
            
        except Exception as e:
            self.status_label.setText(str(e))
            QMessageBox.critical(self, "Error", str(e))