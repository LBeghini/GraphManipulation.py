import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import numpy as np
import networkx as nx

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


class Graph(pg.GraphItem):
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()

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
        self.updateGraph()
        ev.accept()

    def clicked(self, pts):
        print("clicked: %s" % pts)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.g = Graph()
        self.pos = None
        self.adj = None
        self.transform_g6_in_graph("M????CCA?_CB_SOI?")
        self.define_graph()

        self.w = pg.GraphicsLayoutWidget(show=True)
        self.v = self.w.addViewBox()
        self.v.setAspectLocked()
        self.v.addItem(self.g)

        self.setCentralWidget(self.w)

    def transform_g6_in_graph(self, g6):
        gnx = nx.from_graph6_bytes(g6.encode('utf-8'))
        points = nx.drawing.layout.shell_layout(gnx)  # TODO: transform this to array and convert to decimal
        nx_edges = gnx.edges(data=True)

        obj_edge = []
        obj_pos = []

        for e in nx_edges:
            aux = [e[0], e[1]]
            if not reversed(aux) in obj_edge:
                obj_edge.append(aux)

        self.adj = np.array(obj_edge)

        for point in points.values():
            aux = [point[0] * 10 // 1, point[1] * 10 // 1]
            obj_pos.append(aux)

        self.pos = np.array(obj_pos, dtype=float)

    def define_graph(self):

        # # Define positions of nodes
        # pos = np.array([
        #     [0, 0],
        #     [10, 0],
        #     [0, 10],
        #     [10, 10],
        #     [5, 5],
        #     [15, 5]
        # ], dtype=float)
        #
        # # Define the set of connections in the graph
        # adj = np.array([
        #     [0, 1],
        #     [1, 3],
        #     [3, 2],
        #     [2, 0],
        #     [1, 5],
        #     [3, 5],
        # ])


        # # Define the symbol to use for each node (this is optional)
        # symbols = ['o', 'o', 'o', 'o', 't', '+']
        #
        # # Define the line style for each connection (this is optional)
        # lines = np.array([
        #     (255, 0, 0, 255, 1),
        #     (255, 0, 255, 255, 2),
        #     (255, 0, 255, 255, 3),
        #     (255, 255, 0, 255, 2),
        #     (255, 0, 0, 255, 1),
        #     (255, 255, 255, 255, 4),
        # ], dtype=[('red', np.ubyte), ('green', np.ubyte), ('blue', np.ubyte), ('alpha', np.ubyte), ('width', float)])

        # Define text to show next to each symbol
        texts = ["%d" % i for i in range(len(self.pos))]

        # Update the graph
        # self.g.setData(pos=pos, adj=adj, pen=lines, size=1, symbol=symbols, pxMode=False, text=texts)
        self.g.setData(pos=self.pos, adj=self.adj, size=1, pxMode=False, text=texts)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
