from time import sleep
from PySide6.QtGui import QImage
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
)
from PySide6 import QtCore
import sys

import numpy as np
import qimage2ndarray
from pyadbauto.client import Client
from pyadbauto.ide.canvas import DrawState, PhoneCanvas


class IDE(QWidget):
    def __init__(self):
        super().__init__()
        self.client = Client(max_width=1080, max_fps=60)
        self.client.start(daemon_threaded=True)
        sleep(1)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh_image)
        self.timer.start(1000 // self.client.client.max_fps)

        self.initUI()

    def __del__(self):
        if hasattr(self, "client"):
            self.client.stop()

    def initUI(self):
        frame = self.client.last_frame()

        image: QImage = array2qimage(frame)

        if image.isNull():
            print("Failed to load image.")
            return

        # Convert QImage to QPixmap for display
        # pixmap = QPixmap.fromImage(image)

        # Create a QLabel to display the image
        self.phone_label = PhoneCanvas(image, self)
        # self.phone_label.setPixmap(pixmap)

        self.pausebutton = QPushButton("Pause", self)
        self.pausebutton.setCheckable(True)
        self.pausebutton.setChecked(False)
        self.pausebutton.clicked.connect(self.togglePause)

        self.selectbutton = QPushButton("Select", self)
        self.selectbutton.clicked.connect(
            lambda: self.phone_label.set_draw_mode(DrawState.SELECT)
        )

        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.pausebutton)
        buttonlayout.addWidget(self.selectbutton)
        buttonlayout.addStretch(1)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addLayout(buttonlayout)
        layout.addWidget(self.phone_label)
        self.setLayout(layout)

        self.setWindowTitle("QImage Example")
        self.resize(
            QtCore.QSize(
                self.phone_label.size().width() + 16,
                self.phone_label.size().height() + 64,
            )
        )

    def togglePause(self):
        if self.pausebutton.isChecked():
            self.pausebutton.setText("Resume")
            self.pause()
        else:
            self.pausebutton.setText("Pause")
            self.resume()

    def pause(self):
        self.timer.stop()

    def resume(self):
        self.timer.start(1000 // self.client.client.max_fps)

    def refresh_image(self):
        frame = self.client.last_frame()
        if frame is not None:
            image: QImage = array2qimage(frame)
            if not image.isNull():
                self.phone_label.set_image(image)


def array2qimage(array: np.ndarray, normalize: bool = True) -> QImage:
    ret = QImage(array.shape[1], array.shape[0], QImage.Format.Format_RGB32)
    qimage2ndarray._normalize255(array, normalize)
    qimage2ndarray.rgb_view(ret, "little")[:] = array[..., :3]
    return ret


def main():
    app = QApplication(sys.argv)
    window = IDE()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
