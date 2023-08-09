import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

class SliderExample(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QSlider Example")
        self.setGeometry(100, 100, 300, 150)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.value_label = QLabel("Slider Value: 50")

        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)

        self.setLayout(layout)

    def slider_value_changed(self, value):
        self.value_label.setText(f"Slider Value: {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SliderExample()
    window.show()
    sys.exit(app.exec_())
