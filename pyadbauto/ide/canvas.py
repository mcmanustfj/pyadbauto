from enum import Enum, auto
from PySide6 import QtWidgets, QtGui, QtCore


class DrawState(Enum):
    NONE = auto()
    SELECT = auto()
    SELECT_DRAWING = auto()


class PhoneCanvas(QtWidgets.QLabel):
    image: QtGui.QImage

    def __init__(self, image: QtGui.QImage, parent=None):
        super().__init__(parent)

        self.draw_mode: DrawState = DrawState.NONE
        self.start_point = None
        self.end_point = None
        self.box = None
        self.selections = []

        self.set_image(image)

    def set_image(self, image: QtGui.QImage) -> None:
        self.image = image
        self.resize(image.size())
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        if self.image:
            painter.drawImage(self.rect(), self.image)
        if self.start_point and self.end_point:
            self.box = QtCore.QRect(self.start_point, self.end_point)
        else:
            self.box = None

        pen = QtGui.QPen(QtGui.QColor("RED"), 2, QtCore.Qt.PenStyle.DashDotLine)

        painter.setPen(pen)
        if self.box:
            painter.drawRect(self.box)

        painter.setPen(
            QtGui.QPen(QtGui.QColor("WHITE"), 2, QtCore.Qt.PenStyle.SolidLine)
        )
        for selection in self.selections:
            painter.drawRect(selection)

    def sizeHint(self) -> QtCore.QSize:
        return self.image.size() if self.image else QtCore.QSize(0, 0)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.draw_mode == DrawState.SELECT_DRAWING:
            if self.start_point is not None:  # currently drawing rectangle
                self.end_point = event.pos()
                self.update()
            else:
                raise RuntimeError("Drawing mode is not set correctly.")

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            # clear
            self.start_point = None
            self.end_point = None
            self.box = None
            self.selections = []
            self.draw_mode = DrawState.NONE
            self.update()
        if self.draw_mode == DrawState.SELECT:
            if self.start_point is None:
                self.start_point = event.pos()
                self.draw_mode = DrawState.SELECT_DRAWING
                self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.draw_mode == DrawState.SELECT_DRAWING:
            if self.start_point and self.end_point:
                # Rectangle is complete, do something with it
                print(f"Selected area: {self.box}")
                self.start_point = None
                self.end_point = None
                self.selections.append(self.box)
                self.box = None
                self.draw_mode = DrawState.NONE
                self.update()
            else:
                raise RuntimeError("Drawing mode is not set correctly.")

    def set_draw_mode(self, mode: DrawState) -> None:
        self.draw_mode = mode
        if mode == DrawState.SELECT:
            self.start_point = None
            self.end_point = None
            self.update()
