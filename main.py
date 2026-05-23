import ctypes

myappid = (
    "monsterchip.kitfwbuilder.1"
)

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    myappid
)

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()