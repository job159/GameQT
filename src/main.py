import sys
from PyQt5.QtWidgets import QApplication
from app import create_main_window

def main():
    app = QApplication(sys.argv)
    w = create_main_window()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
