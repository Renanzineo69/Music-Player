import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QSlider, QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from logic.player import MusicPlayer
from logic.playlist import Playlist
from styles.style import STYLE
from ui.controls import Controls
from ui.playlist_view import PlaylistView
from ui.progress_bar import ProgressBar


class MusicPlayerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.playlist = Playlist()
        self.player = MusicPlayer()
        self.initUI()
        self.load_saved_playlist()
        self.load_default_music_folder()

    def initUI(self):
        self.setWindowTitle("Music Player")
        self.setGeometry(300, 200, 500, 400)
        self.setStyleSheet(STYLE)

        # 🔹 Layout Principal (Horizontal para incluir o slider de volume)
        main_layout = QHBoxLayout()

        # 🔹 Layout Esquerdo (Playlist e Botão de Adicionar)
        left_layout = QVBoxLayout()

        self.playlist_widget = PlaylistView(self)
        left_layout.addWidget(self.playlist_widget)

        self.load_button = QPushButton("Adicionar Música")
        self.load_button.clicked.connect(self.load_music)
        left_layout.addWidget(self.load_button)

        main_layout.addLayout(left_layout)

        # 🔹 Slider de Volume (Agora está no lado direito da Playlist)
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:vertical {
                background: #555;
                width: 6px;
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                background: #7289DA;
                height: 10px;
                border-radius: 5px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.adjust_volume)

        main_layout.addWidget(self.volume_slider)  # 🔹 Agora está do lado direito!

        # 🔹 Layout Final (Coloca Playlist + Volume dentro do layout principal)
        layout = QVBoxLayout()
        layout.addLayout(main_layout)

        # 🔹 Barra de Progresso (Tempo da música)
        self.progress = ProgressBar(self)
        layout.addLayout(self.progress.layout)

        # 🔹 Controles (⏮️ ▶️ ⏭️)
        self.controls = Controls(self)
        layout.addLayout(self.controls.layout)

        self.setLayout(layout)

    def adjust_volume(self, value):
        """ Ajusta o volume do player de música. """
        volume = value / 100.0
        self.player.set_volume(volume)

    def load_music(self):
        """Carrega músicas para a playlist."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar Músicas", "", "Arquivos de Áudio (*.mp3 *.wav)"
        )
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.playlist.tracks:
                    self.playlist.add_track(file_path)
                    self.playlist_widget.addItem(os.path.basename(file_path))

    def load_saved_playlist(self):
        """Carrega a playlist salva e exibe na interface sem duplicatas."""
        self.playlist_widget.clear()
        for track in self.playlist.tracks:
            self.playlist_widget.addItem(os.path.basename(track))

    def load_default_music_folder(self):
        """Carrega automaticamente os arquivos de áudio da pasta 'Músicas' do usuário sem duplicatas."""
        music_folder = os.path.join(os.path.expanduser("~"), "Music")
        if os.path.exists(music_folder):
            for file in os.listdir(music_folder):
                file_path = os.path.join(music_folder, file)
                if file_path.endswith((".mp3", ".wav")) and file_path not in self.playlist.tracks:
                    self.playlist.add_track(file_path)
                    self.playlist_widget.addItem(os.path.basename(file_path))

    def load_selected_track(self):
        """Toca a música selecionada."""
        selected_row = self.playlist_widget.currentRow()
        if selected_row >= 0:
            track_path = self.playlist.tracks[selected_row]
            self.play_music(track_path)

    def toggle_play_pause(self):
        """Alterna entre Play e Pause."""
        if self.player.is_playing:
            self.player.pause()
            self.controls.play_pause_button.setText("▶️")
            self.progress.timer.stop()
        else:
            if self.player.current_track is None and self.playlist.tracks:
                self.play_music(self.playlist.tracks[0])
                self.playlist_widget.setCurrentRow(0)
            else:
                self.player.resume()
            self.controls.play_pause_button.setText("⏸️")
            self.progress.timer.start(1000)

    def play_music(self, track_path):
        """Reproduz a música especificada."""
        self.player.load_music(track_path)
        self.player.play()
        self.controls.play_pause_button.setText("⏸️")
        self.progress.progress_bar.setValue(0)
        self.progress.timer.start(1000)

    def set_music_position(self):
        """Permite avançar ou retroceder na música pela barra de progresso."""
        if self.player.current_track:
            position = self.progress.progress_bar.value() / 100
            new_time = int(self.player.track_length * position)
            self.player.set_position(new_time)
            self.progress.timer.start(1000)

    def stop_timer(self):
        """Para temporariamente a atualização do timer ao mexer no slider."""
        self.progress.timer.stop()

    def update_progress_bar(self):
        """Atualiza a barra de progresso conforme a música toca."""
        if self.player.current_track:
            current_time, total_time = self.player.get_time_info()
            self.progress.time_label.setText(f"{current_time} / {total_time}")

            if self.player.track_length > 0:
                position = self.player.get_position() / self.player.track_length
                self.progress.progress_bar.setValue(int(position * 100))

    def play_next(self):
        """Reproduz a próxima música da playlist."""
        next_track = self.playlist.get_next_track()
        if next_track:
            self.play_music(next_track)
            self.playlist_widget.setCurrentRow(self.playlist.current_index)

    def play_previous(self):
        """Reproduz a música anterior da playlist."""
        prev_track = self.playlist.get_previous_track()
        if prev_track:
            self.play_music(prev_track)
            self.playlist_widget.setCurrentRow(self.playlist.current_index)
