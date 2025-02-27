import sys
from PyQt5.QtWidgets import QApplication
from ui.interface import MusicPlayerUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayerUI()
    window.show()
    sys.exit(app.exec_())
