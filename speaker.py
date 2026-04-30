import pygame
import os
import random

class Speaker:
    def __init__(self, songs_folder="songs"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.songs_folder = os.path.join(script_dir, songs_folder)
        pygame.mixer.init()
        print(f"Speaker tilbúinn. Lög í möppu: {self.songs_folder}")
    
    def get_random_song(self):
        if not os.path.exists(self.songs_folder):
            print(f"Mappan {self.songs_folder} er ekki til!")
            return None
        songs = [f for f in os.listdir(self.songs_folder) 
                 if f.lower().endswith(('.mp3', '.wav'))]
        if not songs:
            print(f"Engin lög í möppunni {self.songs_folder}")
            return None
        chosen = random.choice(songs)
        return os.path.join(self.songs_folder, chosen)
    
    def play(self):
        song_path = self.get_random_song()
        if song_path is None:
            return
        song_name = os.path.basename(song_path)
        print(f"Spila: {song_name}")
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
    
    def stop(self):
        pygame.mixer.music.stop()
        print("Stöðvaði lagið")
    
    def is_playing(self):
        return pygame.mixer.music.get_busy()


if __name__ == "__main__":
    import time
    speaker = Speaker()
    speaker.play()
    for i in range(30):
        if not speaker.is_playing():
            break
        time.sleep(1)
    print("Búið!")