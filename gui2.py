from PyQt5 import QtCore, QtGui, QtWidgets
import os


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

        table_label = QtWidgets.QLabel(self.centralwidget)
        table_label.setText("Тут таблица mse, psnr")
        self.gridLayout.addWidget(table_label, 0, 1)

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
        image = QtGui.QImage(filename)
        pixmap = QtGui.QPixmap(image)
        label.setPixmap(pixmap)
        self.image_layout.addWidget(label, 0, column_num)

    def handle_save_image(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(MainWindow, 'Сохранить модифицированное изображение', '', 'Изображения (*.png)')[0]
        self.image2.save(fname, "PNG")

    def handle_change_selected_file(self, selected_file, image, pixmap, label, column_number):
        filename = 'test-images/{}'.format(selected_file)
        self.load_image_by_filename(filename, image, pixmap, label, column_number)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())