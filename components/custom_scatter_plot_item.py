from pyqtgraph import ScatterPlotItem
from pyqtgraph.Qt import QtCore


class CustomScatterPlotItem(ScatterPlotItem):
    sigClickedCanvas = QtCore.Signal(object, float, float)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def mouseClickEvent(self, ev):
        self.sigClickedCanvas.emit(self, ev.pos()[0], ev.pos()[1])
        if ev.button() == QtCore.Qt.LeftButton:
            pts = self.pointsAt(ev.pos())
            if len(pts) > 0:
                self.ptsClicked = pts
                ev.accept()
                self.sigClicked.emit(self, self.ptsClicked, ev)
        else:
            ev.ignore()
