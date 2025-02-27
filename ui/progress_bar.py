from PyQt5.QtWidgets import QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

class ProgressBar:
    def __init__(self, parent):
        self.parent = parent
        self.layout = QVBoxLayout()

        # 🔹 Exibição do tempo atual
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        # 🔹 Barra de progresso
        self.progress_bar = QSlider(Qt.Horizontal)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QSlider::groove:horizontal { background: #555; height: 5px; border-radius: 3px; }
            QSlider::handle:horizontal { background: white; width: 10px; border-radius: 5px; }
        """)
        self.progress_bar.sliderPressed.connect(self.parent.stop_timer)
        self.progress_bar.sliderReleased.connect(self.parent.set_music_position)
        self.layout.addWidget(self.progress_bar)

        # 🔹 Timer para atualizar a barra
        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.parent.update_progress_bar)
