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
)

from PySide6.QtGui import QIcon

import builder.esp32 as esp32
import builder.esp8266 as esp8266
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
            300
        )

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        # ------------------------
        # Target
        # ------------------------

        layout.addWidget(
            QLabel("Target")
        )

        self.target_combo = QComboBox()

        self.target_combo.addItems([
            "esp32",
            "esp8266",
            "avr"
        ])

        layout.addWidget(
            self.target_combo
        )

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

            target = (
                self.target_combo.currentText()
            )

            folder = (
                self.folder_edit.text()
            )

            name = (
                self.name_edit.text()
            )

            version = (
                self.version_edit.text()
            )

            output = (
                self.output_edit.text()
            )

            # --------------------
            # Detect files
            # --------------------

            if target == "esp32":

                files = (
                    esp32.find_artifacts(
                        folder
                    )
                )

            elif target == "esp8266":

                files = (
                    esp8266.find_artifacts(
                        folder
                    )
                )

            elif target == "avr":

                files = (
                    avr.find_artifacts(
                        folder
                    )
                )

            else:

                raise Exception(
                    "Unsupported target"
                )

            # --------------------
            # Create manifest
            # --------------------

            manifest = create_manifest(
                name,
                version,
                target,
                files
            )

            # --------------------
            # Validate
            # --------------------

            validate_manifest(
                manifest
            )

            validate_files(
                manifest,
                files
            )

            # --------------------
            # Write package
            # --------------------

            write_package(
                output,
                manifest,
                files
            )

            self.status_label.setText(
                "Package created successfully"
            )

            QMessageBox.information(
                self,
                "Success",
                "Package created successfully."
            )

        except Exception as e:

            self.status_label.setText(
                str(e)
            )

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )