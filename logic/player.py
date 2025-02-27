import pygame

class MusicPlayer:
    def __init__(self):
        """Inicializa o player de música usando Pygame"""
        pygame.mixer.init()
        self.current_track = None
        self.is_playing = False
        self.paused = False
        self.track_length = 0  # Armazena a duração total da música

    def load_music(self, file_path):
        """Carrega uma nova música para reprodução"""
        pygame.mixer.music.load(file_path)
        self.current_track = file_path
        self.track_length = pygame.mixer.Sound(file_path).get_length()  # Obtém a duração total da música

    def play(self):
        """Inicia ou continua a reprodução da música"""
        if self.current_track:
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.is_playing = True
            self.paused = False

    def pause(self):
        """Pausa a reprodução da música"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.paused = True

    def stop(self):
        """Para completamente a reprodução da música"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.paused = False

    def set_volume(self, volume):
        """Define o volume da música (0.0 a 1.0)"""
        pygame.mixer.music.set_volume(volume)

    def get_position(self):
        """Obtém a posição atual da música em segundos"""
        return pygame.mixer.music.get_pos() / 1000  # Retorna a posição em segundos

    def get_time_info(self):
        """Retorna o tempo atual e a duração total da música no formato MM:SS"""
        current_time = int(self.get_position())
        total_time = int(self.track_length)
        return self.format_time(current_time), self.format_time(total_time)

    def format_time(self, seconds):
        """Converte segundos para o formato MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def set_position(self, position):
        """Define um novo ponto na música"""
        new_time = int(self.track_length * position)
        pygame.mixer.music.play(start=new_time)

    def resume(self):
        """Continua a música de onde parou."""
        pygame.mixer.music.unpause()
        self.is_playing = True

    def set_position(self, time):
        """Define um novo tempo para a música."""
        pygame.mixer.music.play(start=time)
