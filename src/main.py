#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, numpy, PIL
from PySide2 import QtCore, QtGui, QtWidgets
from PIL import Image, ImagePalette

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setAcceptDrops(True)
        self.widget = Widget(self)
        self.setCentralWidget(self.widget)

        menu = QtWidgets.QMenu('Save', self)
        menu.addAction(self.widget.GraphicsView.Scene.Drawable.SaveAction)
        self.menuBar().addMenu(menu)

        self.show()
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        self.widget.update()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        self.widget.update()
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragEnterEvent(event)
        self.widget.update()
    def dragMoveEvent(self, event):
        super(self.__class__, self).dragMoveEvent(event)
    def dropEvent(self, event):
        super(self.__class__, self).dropEvent(event)

class Widget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setAcceptDrops(True)
        self.view = GraphicView()
        scroller = QtWidgets.QScrollArea()
        scroller.setWidget(self.view)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(scroller, 0, 0)

        self.setLayout(layout)
        self.resize(self.view.width(), self.view.height())
        self.setWindowTitle("QAction")
        self.show()
    @property
    def GraphicsView(self): return self.view
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        self.view.update()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        self.view.update()
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragEnterEvent(event)
        self.view.dragEnterEvent(event)
        self.view.update()
    def dragMoveEvent(self, event):
        super(self.__class__, self).dragMoveEvent(event)
    def dropEvent(self, event):
        super(self.__class__, self).dropEvent(event)

class GraphicView(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)
        self.setAcceptDrops(True)
        self.setWindowTitle("QGraphicsScene draw Grid")
        self.__editorScene = EditorScene(self)
        self.setScene(self.__editorScene)
    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        self.scene().update()
    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        self.scene().update()
    @property
    def Scene(self): return self.__editorScene
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragEnterEvent(event)
        self.scene().update()
    def dragEnterEvent(self, event):
        super(self.__class__, self).dragMoveEvent(event)
        self.scene().update()
    def dropEvent(self, event):
        super(self.__class__, self).dropEvent(event)
        self.scene().update()

class EditorScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
        self.setSceneRect(0, 0, self.size*self.scale, self.size*self.scale)

        self.grid = GridItem()
        self.addItem(self.grid)

        self.background = BackgroundItem()
        self.addItem(self.background)

        self.drawable = DrawableItem()
        self.addItem(self.drawable)

        self.background.setZValue(0)
        self.drawable.setZValue(1)
        self.grid.setZValue(9999)

    def mousePressEvent(self, event):
        for item in self.items():
            item.mousePressEvent(event)
        super(self.__class__, self).mousePressEvent(event)
    def mouseMoveEvent(self, event):
        for item in self.items():
            item.setAcceptHoverEvents(True)
            item.mouseMoveEvent(event)
        super(self.__class__, self).mouseMoveEvent(event)
    def dragEnterEvent(self, event):
        for item in self.items():
            item.setAcceptDrops(True)
            if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
                item.dragEnterEvent(event)
        if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
            super(self.__class__, self).dragEnterEvent(event)
    def dragMoveEvent(self, event):
        for item in self.items():
            item.setAcceptDrops(True)
            if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
                item.dragEnterEvent(event)
        if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
            super(self.__class__, self).dragEnterEvent(event)
    def dropEvent(self, event):
        for item in self.items():
            item.setAcceptDrops(True)
#            print(item, event)
            item.dropEvent(event)
        if event is type(QtWidgets.QGraphicsSceneDragDropEvent):
            super(self.__class__, self).dropEvent(event)
    @property
    def Grid(self): return self.grid
    @property
    def Background(self): return self.background
    @property
    def Drawable(self): return self.drawable

class DrawableItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.size = 16
        self.scale = 32
        self.pixels = Pixcels()
        self.actions = {}
        self.__create_save_action()

    def __create_save_action(self):
        a = QtWidgets.QAction('Save')
        a.setObjectName('Save')
        a.setShortcut('Ctrl+S')
        a.triggered.connect(self.Pixels.save)
        self.actions['Save'] = a

    def paint(self, painter, option, widget):
        painter.fillRect(widget.rect(), QtGui.QBrush( QtGui.QColor(0,0,0,0), QtCore.Qt.SolidPattern))
        for y in range(self.pixels.Height):
            for x in range(self.pixels.Width):
                if 1 == self.pixels.Pixels[y][x]:
                    painter.fillRect(x*self.scale, y*self.scale, self.scale, self.scale, QtGui.QBrush( QtGui.QColor(255,0,0,128), QtCore.Qt.SolidPattern))
 
    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.pixels.Pixels[y][x] = 1
#            print('L DRAG!!', x, y)
        if event.buttons() & QtCore.Qt.RightButton:
            self.pixels.Pixels[y][x] = 0
#            print('R DRAG!!', x, y)
    def mousePressEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
#        print('Press', str(pos.x()//self.scale), str(pos.y()//self.scale))
        if event.buttons() & QtCore.Qt.LeftButton:
            self.pixels.Pixels[y][x] = 1
        if event.buttons() & QtCore.Qt.RightButton:
            self.pixels.Pixels[y][x] = 0
    def mouseReleaseEvent(self, event):
        pass
    def mouseDoubleClickEvent(self, event):
        pass
    @property
    def Pixels(self): return self.pixels
    @property
    def SaveAction(self): return self.actions['Save']
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_name = url.toLocalFile()
            print("Dropped file: " + file_name)
            self.Pixels.load(file_name)

class BackgroundItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
        self.colors = [QtGui.QColor(196,196,196,255), QtGui.QColor(232,232,232,255)]
    def paint(self, painter, option, widget):
        for i in range(self.size*self.size):
            x = (i % self.size)
            y = (i // self.size)
            color = QtGui.QColor(128,128,128,255) if 0 == (i % 2) and 0 == (x % 2) else QtGui.QColor(196,196,196,255)
            painter.fillRect(x * (self.scale),               y * (self.scale),               self.scale//2, self.scale//2, self.colors[0])
            painter.fillRect(x * (self.scale)+self.scale//2, y * (self.scale)+self.scale//2, self.scale//2, self.scale//2, self.colors[0])
            painter.fillRect(x * (self.scale)+self.scale//2, y * (self.scale),               self.scale//2, self.scale//2, self.colors[1])
            painter.fillRect(x * (self.scale),               y * (self.scale)+self.scale//2, self.scale//2, self.scale//2, self.colors[1])

class GridItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
    def paint(self, painter, option, widget):
        painter.fillRect(widget.rect(), QtGui.QBrush(QtGui.QColor(0,0,0,0), QtCore.Qt.SolidPattern))
        lines = []
        for y in range(self.size+1):
            lines.append(QtCore.QLine(0, y*self.scale, self.size*self.scale, y*self.scale))
        for x in range(self.size+1):
            lines.append(QtCore.QLine(x*self.scale, 0, x*self.scale, self.size*self.scale))
        painter.drawLines(lines)

class Pixcels:
    def __init__(self):
        self.width = 16
        self.height = 16
        self.pixels = numpy.zeros(self.width*self.height, dtype=int).reshape(self.height, self.width)
    @property
    def Pixels(self): return self.pixels
    @property
    def Width(self): return self.width
    @property
    def Height(self): return self.height
    def save(self):
        self.save_txt()
        self.save_png()
    def load(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()[1:]
        if 'txt' == ext: self.load_txt(file_path)
        elif 'png' == ext: self.load_png(file_path)
    def save_txt(self):
        with open('pixels.txt', 'w') as f:
            f.write('\n'.join([''.join(map(str, self.pixels[y].tolist())) for y in range(self.height)]))
    def load_txt(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.read().split('\n')
            self.height = len(lines)
            self.width = len(lines[0])
            self.pixels = numpy.zeros(self.width*self.height, dtype=int).reshape(self.height, self.width)
            x = 0; y = 0;
            for line in lines:
                for c in line:
                    self.pixels[y][x] = int(c, 16)
                    x += 1
                y += 1
                x = 0
    def save_png(self):
        image = Image.new('1', (self.width, self.height))
        image.putdata(self.pixels.reshape(self.width * self.height).tolist())
        image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pixels.png'))
    def load_png(self, file_path):
        image = Image.open(file_path)
        self.width, self.height = image.size
        self.pixels = numpy.array(image).reshape(self.height, self.width)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

