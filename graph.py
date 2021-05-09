import pyqtgraph as pg
from pyqtgraph import ScatterPlotItem
from components.custom_scatter_plot_item import CustomScatterPlotItem
from pyqtgraph.Qt import QtCore
import numpy as np

pg.setConfigOptions(antialias=True)


class Graph(pg.GraphItem):
    remove_signal = QtCore.pyqtSignal(int, list)
    change_position_signal = QtCore.pyqtSignal(np.ndarray)
    canvas_clicked_signal = QtCore.pyqtSignal(float, float)

    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        self.click_under_cursor = False
        self.custom_pen = []

        pg.GraphItem.__init__(self)

        self.scatter = CustomScatterPlotItem()
        self.scatter.setParentItem(self)

        self.scatter.sigClicked.connect(self.clicked)
        self.scatter.sigClickedCanvas.connect(self.clickedCanvas)

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
            self.createPen()
        self.setTexts(self.text)
        self.updateGraph()

    def createPen(self):
        for i in range(0, len(self.data['pos'])):
            self.custom_pen.append({"width": 1})

    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):
        pg.GraphItem.setData(self, **self.data)
        for i, item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])

    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return

        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.change_position_signal.emit(self.data['pos'])
        self.updateGraph()
        ev.accept()

    def clicked(self, pts: ScatterPlotItem, ev):
        # print("clicked: %s" % pts.data['x'])
        self.click_under_cursor = True
        id_pos = ev[0]._index
        current_pen = self.custom_pen.copy()
        current_pen[id_pos] = {"color": "#164aba", "width": 2}
        self.scatter.setPen(current_pen)
        id_edge = []
        for i, edge in enumerate(self.data['adj']):
            if id_pos in edge:
                id_edge.append(i)
        self.remove_signal.emit(id_pos, id_edge)

    def clickedCanvas(self, pts: ScatterPlotItem, x, y):
        self.canvas_clicked_signal.emit(x, y)
