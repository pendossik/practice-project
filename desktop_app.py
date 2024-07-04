import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, \
    QPushButton, QFileDialog, QDialog, QInputDialog, QScrollArea, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 800, 600)

        # Виджет для отображения изображений
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        # Диалоговые окна для сообщений
        self.create_photo_msg_box = QMessageBox()
        self.create_photo_msg_box.setIcon(QMessageBox.Information)
        self.create_photo_msg_box.setText('Веб-камера запускается, подождите.')
        self.create_photo_msg_box.setWindowTitle('Загрузка')
        self.create_photo_msg_box.setStandardButtons(QMessageBox.NoButton)

        self.warning_msg_box = QMessageBox()
        self.warning_msg_box.setIcon(QMessageBox.Warning)
        self.warning_msg_box.setText('Проверьте работу веб-камеры и повторите еще раз.')
        self.warning_msg_box.setWindowTitle('Ошибка!')

        self.information_msg_box = QMessageBox()
        self.information_msg_box.setIcon(QMessageBox.Information)
        self.information_msg_box.setText('Фото успешно создано!')
        self.information_msg_box.setWindowTitle('Информация')

        # Кнопки управления
        self.load_button = QPushButton("Загрузить изображение")
        self.load_button.clicked.connect(self.load_image)

        self.web_button = QPushButton("Сделать изображение с помощью веб-камеры")
        self.web_button.clicked.connect(self.create_photo_msg_box.show)
        self.web_button.clicked.connect(self.web_image)

        self.show_button = QPushButton("Показать оригинальное изображение")
        self.show_button.clicked.connect(self.show_image)
        self.show_button.setEnabled(False)

        self.channel_button = QPushButton("Показать канал изображения")
        self.channel_button.clicked.connect(self.choose_channel)
        self.channel_button.setEnabled(False)

        self.rotate_button = QPushButton("Повернуть изображение")
        self.rotate_button.clicked.connect(self.rotate_image)
        self.rotate_button.setEnabled(False)

        self.negative_button = QPushButton("Негативное изображение")
        self.negative_button.clicked.connect(self.negative_image)
        self.negative_button.setEnabled(False)

        self.circle_button = QPushButton("Нарисовать круг")
        self.circle_button.clicked.connect(self.draw_circle)
        self.circle_button.setEnabled(False)

        # Компоновка кнопок
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.web_button)
        button_layout.addWidget(self.show_button)
        button_layout.addWidget(self.channel_button)
        button_layout.addWidget(self.rotate_button)
        button_layout.addWidget(self.negative_button)
        button_layout.addWidget(self.circle_button)

        # Основная компоновка
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(button_layout)

        central_widget = QDialog()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.img = None  # Переменная для хранения изображения

    # Метод загрузки изображения
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Загрузить изображение",
                                                   "",
                                                   "Image Files (*.jpg *.jpeg *.png)")
        if file_path:
            file_path = os.path.normpath(file_path)
            self.img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if self.img is not None:
                self.show_button.setEnabled(True)
                self.channel_button.setEnabled(True)
                self.rotate_button.setEnabled(True)
                self.negative_button.setEnabled(True)
                self.circle_button.setEnabled(True)

    # Метод для работы с веб-камерой
    def web_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.warning_msg_box.exec()
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                self.create_photo_msg_box.accept()
                self.warning_msg_box.exec()
                break
            self.create_photo_msg_box.accept()
            cv2.imshow("Нажмите на SPACE, чтобы сделать фото или ESCAPE, чтобы выйти из окна", frame)
            key = cv2.waitKey(1)
            if key == 27:
                cv2.destroyAllWindows()
                break
            elif key == 32:
                self.img = frame
                self.show_button.setEnabled(True)
                self.channel_button.setEnabled(True)
                self.rotate_button.setEnabled(True)
                self.negative_button.setEnabled(True)
                self.circle_button.setEnabled(True)
                self.display_image(self.img)
                self.information_msg_box.exec()
                cv2.destroyAllWindows()
                break

    # Метод для показа изображения
    def show_image(self):
        if self.img is not None:
            self.display_image(self.img)

    # Метод для выбора канала изображения
    def choose_channel(self):
        if self.img is not None:
            channels = ["Синий", "Зеленый", "Красный"]
            channel, ok = QInputDialog.getItem(self,
                                               "Выбрать канал",
                                               "Канал:",
                                               channels,
                                               0,
                                               False)
            if ok:
                if channel == "Синий":
                    img_blue = self.img.copy()
                    img_blue[:, :, 1] = 0
                    img_blue[:, :, 2] = 0
                    self.display_image(img_blue)
                elif channel == "Зеленый":
                    img_green = self.img.copy()
                    img_green[:, :, 0] = 0
                    img_green[:, :, 2] = 0
                    self.display_image(img_green)
                elif channel == "Красный":
                    img_red = self.img.copy()
                    img_red[:, :, 0] = 0
                    img_red[:, :, 1] = 0
                    self.display_image(img_red)

    # Метод для поворота изображения
    def rotate_image(self):
        if self.img is not None:
            angle, ok = QInputDialog.getInt(self,
                                            "Повернуть изображение",
                                            "Угол:",
                                            0,
                                            -360,
                                            360,
                                            1)
            if ok:
                height, width = self.img.shape[:2]
                center = (width / 2, height / 2)
                M = cv2.getRotationMatrix2D(center, angle, 1)
                rotated_img = cv2.warpAffine(self.img, M, (width, height))
                self.display_image(rotated_img)

    # Метод для создания негативного изображения
    def negative_image(self):
        if self.img is not None:
            negative_img = cv2.bitwise_not(self.img)
            self.display_image(negative_img)

    # Метод для рисования круга на изображении
    def draw_circle(self):
        if self.img is not None:
            height, width = self.img.shape[:2]
            x, ok = QInputDialog.getInt(self,
                                        "Нарисовать круг",
                                        "Координата X:",
                                        0,
                                        0,
                                        width,
                                        1)
            if ok:
                y, ok = QInputDialog.getInt(self,
                                            "Нарисовать круг",
                                            "Координата Y:",
                                            0,
                                            0,
                                            height,
                                            1)
                if ok:
                    max_radius = min(x, y, width - x, height - y)
                    radius, ok = QInputDialog.getInt(self,
                                                     "Нарисовать круг",
                                                     f"Радиус (макс {max_radius}):",
                                                     0,
                                                     1,
                                                     max_radius, 1)
                    if ok:
                        circled_img = self.img.copy()
                        cv2.circle(circled_img, (x, y),
                                   radius, (0, 0, 255), -1)
                        self.display_image(circled_img)

    # Метод для отображения изображения в QLabel
    def display_image(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            qformat = QImage.Format_RGB888
        out_image = QImage(img, img.shape[1],
                           img.shape[0], img.strides[0], qformat)
        out_image = out_image.rgbSwapped()

        self.image_label.setPixmap(QPixmap.fromImage(out_image))
        self.image_label.setAlignment(Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())
