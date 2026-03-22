import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.dashboard.dashboard import Dashboard

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()