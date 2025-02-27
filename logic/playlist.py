import json
import os

class Playlist:
    def __init__(self, playlist_file="playlist.json"):
        self.playlist_file = playlist_file
        self.tracks = []
        self.current_index = 0
        self.load_playlist()

    def add_track(self, file_path):
        """Adiciona uma nova música à playlist."""
        if file_path and file_path not in self.tracks:
            self.tracks.append(file_path)
            self.save_playlist()

    def remove_track(self, index):
        """Remove uma música da playlist pelo índice."""
        if 0 <= index < len(self.tracks):
            del self.tracks[index]
            self.save_playlist()

    def get_next_track(self):
        """Retorna a próxima música da playlist."""
        if self.tracks:
            self.current_index = (self.current_index + 1) % len(self.tracks)
            return self.tracks[self.current_index]
        return None

    def get_previous_track(self):
        """Retorna a música anterior da playlist."""
        if self.tracks:
            self.current_index = (self.current_index - 1) % len(self.tracks)
            return self.tracks[self.current_index]
        return None

    def load_playlist(self):
        """Carrega a playlist salva em um arquivo JSON."""
        if os.path.exists(self.playlist_file):
            with open(self.playlist_file, "r", encoding="utf-8") as file:
                self.tracks = json.load(file)

    def save_playlist(self):
        """Salva a playlist atual no arquivo JSON."""
        with open(self.playlist_file, "w", encoding="utf-8") as file:
            json.dump(self.tracks, file, indent=4)
