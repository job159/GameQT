from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.resize(640, 480)

        self.label = QLabel("No image")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self._pix = None

    def set_image(self, path: str):
        pix = QPixmap(path)
        if pix.isNull():
            self.label.setText("Failed to load image.")
            self._pix = None
            return
        self._pix = pix
        self._update_scaled()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._update_scaled()

    def _update_scaled(self):
        if self._pix is None:
            return
        scaled = self._pix.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled)
