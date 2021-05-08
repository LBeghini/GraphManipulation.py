from PyQt5.QtWidgets import *
from components.action_button import ActionButton
from PyQt5.QtGui import QIcon


class ToolBar(QToolBar):
    def __init__(self):
        super().__init__()

        self.filtered_graphs_label = QLabel("List of graphs filtered")

        self.add_node = ActionButton("Add node", Icon("addNodeIcon"))
        self.add_edge = ActionButton("Add edge", Icon("connectIcon"))
        self.remove_node = ActionButton("Remove node", Icon("deleteIcon"))
        self.remove_edge = ActionButton("Remove node", Icon("deleteIcon"))

        self.set_content_attributes()
        self.set_up_layout()

    def set_content_attributes(self):
        self.layout().setSpacing(30)
        self.layout().setContentsMargins(15, 10, 20, 20)
        self.setMovable(True)

        self.add_node.setDisabled(False)
        self.add_edge.setDisabled(True)
        self.remove_node.setDisabled(False)
        self.remove_edge.setDisabled(True)

    def set_up_layout(self):
        self.addWidget(self.add_node)
        self.addWidget(self.add_edge)
        self.addWidget(self.remove_node)
        self.addWidget(self.remove_edge)


class Icon(QIcon):
    def __init__(self, name):
        super().__init__()
        self.addFile(f"resources/{name}.png")
