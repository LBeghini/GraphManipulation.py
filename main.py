import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
import numpy as np
import networkx as nx
from graph import Graph
import pyqtgraph as pg


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.pos = []
        self.adj = []
        self.texts = []

        self.graph = Graph()

        self.nx_graph = None

        self.w = pg.GraphicsLayoutWidget(show=True)
        self.v = self.w.addViewBox()

        self.connect_events()
        self.set_up()

    def connect_events(self):
        self.graph.remove_signal.connect(self.remove)
        self.graph.change_position_signal.connect(self.update_pos)

    def update_pos(self, pos):
        for i in range(len(pos)):
            self.pos[i][0] = pos[i][0]
            self.pos[i][1] = pos[i][1]

    def set_up(self):
        self.v.setAspectLocked()
        self.v.addItem(self.graph)

        self.setCentralWidget(self.w)

        self.transform_g6_in_graph("L??????????^~@")
        self.get_pos()
        self.get_adj()
        self.define_graph()

    def remove(self, id_pos, id_edge):
        if len(self.pos) == 1:
            return
        self.pos.pop(id_pos)
        for i in reversed(id_edge):
            self.adj.pop(i)
        self.nx_graph.remove_node(self.texts[id_pos])
        self.texts.pop(id_pos)
        self.update_graph_index(id_pos)
        print(self.texts)
        print(id_pos)
        self.define_graph()

    def update_graph_index(self, id_pos):
        for i in range(0, len(self.adj)):
            if self.adj[i][0] > id_pos:
                self.adj[i][0] -= 1

            if self.adj[i][1] > id_pos:
                self.adj[i][1] -= 1

    def get_pos(self):
        points = nx.drawing.layout.spring_layout(self.nx_graph)

        for i, point in enumerate(points.values()):
            aux = [point[0] * 10 // 1, point[1] * 10 // 1]
            self.pos.append(aux)
            self.texts.append(i)

    def get_adj(self):
        nx_edges = self.nx_graph.edges(data=True)
        for e in nx_edges:
            aux = [e[0], e[1]]
            if not reversed(aux) in self.adj:
                self.adj.append(aux)

    def transform_g6_in_graph(self, g6):
        self.nx_graph = nx.from_graph6_bytes(g6.encode('utf-8'))

    def define_graph(self):
        pos = np.array(self.pos, dtype=float)
        adj = np.array(self.adj)

        texts = ["%d" % i for i in self.texts]

        self.graph.setData(pos=pos, adj=adj, size=1, pxMode=False, text=texts)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
