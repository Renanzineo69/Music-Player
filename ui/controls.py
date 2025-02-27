from PyQt5.QtWidgets import QPushButton, QHBoxLayout

class Controls:
    def __init__(self, parent):
        self.parent = parent
        self.layout = QHBoxLayout()

        # 🔹 Botão Anterior
        self.prev_button = QPushButton("⏮️")
        self.prev_button.clicked.connect(self.parent.play_previous)
        self.layout.addWidget(self.prev_button)

        # 🔹 Botão Play/Pause
        self.play_pause_button = QPushButton("▶️")
        self.play_pause_button.clicked.connect(self.parent.toggle_play_pause)
        self.layout.addWidget(self.play_pause_button)

        # 🔹 Botão Próxima
        self.next_button = QPushButton("⏭️")
        self.next_button.clicked.connect(self.parent.play_next)
        self.layout.addWidget(self.next_button)
