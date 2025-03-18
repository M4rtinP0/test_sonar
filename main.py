import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Nastavení GUI
        self.setWindowTitle("SonarQube Test Aplikace")
        self.setGeometry(100, 100, 400, 300)

        # Vytvoření UI prvků
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.button = QPushButton("Zobrazit Text", self)
        self.button.clicked.connect(self.display_text)
        self.layout.addWidget(self.button)

        # Nastavení layoutu
        self.setLayout(self.layout)

    def display_text(self):
        # Funkce pro zobrazení textu z textového pole
        text = self.text_edit.toPlainText()
        print(f"Zadaný text: {text}")
        self.text_edit.setText(f"Zadal(a) jsi: {text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())
