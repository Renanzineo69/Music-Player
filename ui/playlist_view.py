from PyQt5.QtWidgets import QListWidget

class PlaylistView(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #23272A; color: white; border-radius: 5px; padding: 5px;")
        self.itemDoubleClicked.connect(self.parent.load_selected_track)
