from PyQt5 import QtCore, QtGui, QtWidgets
import os
import numpy as np
from qimage2ndarray import recarray_view
from psnr import calculate_psnr


class Ui_MainWindow(object):
    def __init__(self):
        self.default_images_paths = os.listdir('test-images')

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.image_layout = QtWidgets.QGridLayout()
        self.image_layout.setObjectName("image layout")
        self.gridLayout.addLayout(self.image_layout, 0, 0)

        self.psnr_table = QtWidgets.QTableWidget(5, 2)
        self.set_default_psnr_table_values()
        self.resize_psnr_table()
        self.gridLayout.addWidget(self.psnr_table, 0, 1)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        # первая колонка с изображением
        self.image1 = QtGui.QImage('./test-images/image_Baboon512rgb.png')
        self.pixmap1 = QtGui.QPixmap(self.image1)
        self.label1 = QtWidgets.QLabel()
        self.select1 = QtWidgets.QComboBox()
        self.setup_image_columns(self.image1, self.pixmap1, self.label1, self.select1, 0)

        # вторая колонка с изображением
        self.image2 = QtGui.QImage('./test-images/image_Baboon512rgb.png')
        self.pixmap2 = QtGui.QPixmap(self.image2)
        self.label2 = QtWidgets.QLabel()
        self.select2 = QtWidgets.QComboBox()
        self.setup_image_columns(self.image2, self.pixmap2, self.label2, self.select2, 1)

        save_image_btn2 = QtWidgets.QPushButton("Сохранить изображение")
        save_image_btn2.clicked.connect(lambda: self.handle_save_image())
        self.image_layout.addWidget(save_image_btn2, 4, 1)

        calculate_psnr_btn = QtWidgets.QPushButton("Посчитать PSNR")
        calculate_psnr_btn.clicked.connect(self.calculate_psnr)
        self.image_layout.addWidget(calculate_psnr_btn, 5, 1)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        MainWindow.setCentralWidget(self.centralwidget)

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_image_columns(self, image, pixmap, label, select, column_num):
        pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio)

        label.setText("")
        label.setPixmap(self.pixmap1)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMaximumSize(512, 512)
        self.image_layout.addWidget(label, 0, column_num)

        select_label = QtWidgets.QLabel()
        select_label.setText('Выбрать предзагруженное изображение')

        self.image_layout.addWidget(select_label, 1, column_num)

        select.insertItems(0, self.default_images_paths)
        select.currentTextChanged.connect(
            lambda file: self.handle_change_selected_file(file, image, pixmap, label, column_num))
        self.image_layout.addWidget(select, 2, column_num)

        load_image_btn = QtWidgets.QPushButton('Загрузить изображение')
        load_image_btn.clicked.connect(lambda: self.handle_load_image(image, pixmap, label, 0))
        self.image_layout.addWidget(load_image_btn, 3, column_num)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def handle_load_image(self, image, pixmap, label, column_num):
        fname = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Выбрать картинку', '')[0]
        self.load_image_by_filename(fname, image, pixmap, label, column_num)

    def load_image_by_filename(self, filename, image, pixmap, label, column_num):
        image.load(filename)
        label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.image_layout.addWidget(label, 0, column_num)

    def handle_save_image(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Сохранить модифицированное изображение', '', 'Изображения (*.png)')[0]
        self.image2.save(fname, "PNG")

    def handle_change_selected_file(self, selected_file, image, pixmap, label, column_number):
        filename = 'test-images/{}'.format(selected_file)
        self.load_image_by_filename(filename, image, pixmap, label, column_number)

    def calculate_psnr(self):
        format1 = self.image1.format()
        format2 = self.image2.format()

        if format1 != format2:
            self.statusbar.showMessage('Нельзя вычислить psnr: разные цветовые форматы у изображений', msecs=5000)
            return

        height1 = self.image1.height()
        width1 = self.image1.width()

        height2 = self.image2.height()
        width2 = self.image2.width()

        if height1 != height2 or width1 != width2:
            self.statusbar.showMessage('Нельзя вычислить psnr: разные размеры у изображений', msecs=5000)
            return

        ptr1 = self.image1.bits()
        ptr1.setsize(height1 * width1 * 4)
        arr1 = np.frombuffer(ptr1, np.uint8).reshape((height1, width1, 4))

        ptr2 = self.image2.bits()
        ptr2.setsize(height1 * width2 * 4)
        arr2 = np.frombuffer(ptr2, np.uint8).reshape((height2, width2, 4))

        psnr, psnr_red, psnr_green, psnr_blue = calculate_psnr(arr1, arr2)
        self.set_psnr_table_values(psnr, psnr_red, psnr_green, psnr_blue)

    def set_default_psnr_table_values(self):
        self.psnr_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.psnr_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.psnr_table.setItem(0, 1, QtWidgets.QTableWidgetItem("PSNR"))
        self.psnr_table.setItem(1, 0, QtWidgets.QTableWidgetItem("Red"))
        self.psnr_table.setItem(2, 0, QtWidgets.QTableWidgetItem("Green"))
        self.psnr_table.setItem(3, 0, QtWidgets.QTableWidgetItem("Blue"))
        self.psnr_table.setItem(4, 0, QtWidgets.QTableWidgetItem("Full"))
        for i in range(1, 5):
            self.psnr_table.setItem(i, 1, QtWidgets.QTableWidgetItem("0"))

    def set_psnr_table_values(self, psnr, psnr_red, psnr_green, psnr_blue):
        values = [psnr_red, psnr_green, psnr_blue, psnr]
        for i in range(1, 5):
            self.psnr_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(values[i-1])))
        self.resize_psnr_table()

    def resize_psnr_table(self):
        self.psnr_table.resizeColumnsToContents()
        w = self.psnr_table.verticalHeader().width()
        h = self.psnr_table.horizontalHeader().height()
        for i in range(self.psnr_table.columnCount()):
            w += self.psnr_table.columnWidth(i)
        for i in range(self.psnr_table.rowCount()):
            h += self.psnr_table.rowHeight(i)
        self.psnr_table.setMinimumSize(w, h)
        self.psnr_table.setMaximumSize(w, h)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())