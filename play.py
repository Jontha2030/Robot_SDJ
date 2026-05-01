"""
play.py - Stjórnar speaker spilun
Notkun:
    python3 play.py          # Sýnir lista og velur lag (Enter = random)
    python3 play.py random   # Random lag án að spyrja
    python3 play.py stop     # Stöðvar spilun
"""

import sys
import os
import time
import random
import signal
import subprocess

# Slóð á PID skrá og log
PID_FILE = "/tmp/speaker.pid"
LOG_FILE = "/tmp/speaker.log"

# Slóð á songs möppu (sama mappa og þetta skjal)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SONGS_DIR = os.path.join(SCRIPT_DIR, "songs")


def get_songs():
    """Sækja lista yfir öll lög í songs möppunni."""
    if not os.path.exists(SONGS_DIR):
        print(f"Mappan {SONGS_DIR} er ekki til!")
        return []
    
    songs = sorted([
        f for f in os.listdir(SONGS_DIR)
        if f.lower().endswith(('.mp3', '.wav'))
    ])
    return songs


def stop_playing():
    """Stöðva núverandi spilun."""
    stopped = False
    
    # Aðferð 1: Lesa PID úr skrá
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGKILL)
            print(f"Drap PID {pid}")
            stopped = True
        except (ProcessLookupError, ValueError):
            pass
        os.remove(PID_FILE)
    
    # Aðferð 2: Drepa öll python ferli sem keyra play.py
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'play.py.*play_song'],
            capture_output=True, text=True
        )
        for pid in result.stdout.strip().split('\n'):
            if pid:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"Drap PID {pid} (pgrep)")
                    stopped = True
                except ProcessLookupError:
                    pass
    except Exception:
        pass
    
    if stopped:
        print("Lagið stöðvað.")
    else:
        print("Engin lög í gangi.")


def play_song(song_path):
    """Spila eitt lag (þessi keyrir í bakgrunni)."""
    import pygame
    
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)


def start_playing(song_name):
    """Hefja spilun á völdu lagi (í bakgrunni)."""
    # Stöðva fyrri spilun
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGKILL)
        except (ProcessLookupError, ValueError):
            pass
        os.remove(PID_FILE)
    
    song_path = os.path.join(SONGS_DIR, song_name)
    
    # Ræsa nýtt python ferli í bakgrunni
    proc = subprocess.Popen(
        ['python3', __file__, 'play_song', song_path],
        stdout=open(LOG_FILE, 'w'),
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    
    # Vista PID
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    print(f"Spilar: {song_name}")
    print(f"(PID: {proc.pid})")


def show_menu_and_play():
    """Sýna lista yfir lög og leyfa notenda að velja."""
    songs = get_songs()
    
    if not songs:
        print("Engin lög fundust!")
        return
    
    print("\n=== Lög í boði ===")
    for i, song in enumerate(songs, 1):
        print(f"{i:2d}) {song}")
    print()
    
    choice = input("Sláðu inn númer á lagi (eða Enter fyrir random): ").strip()
    
    if not choice:
        # Random
        chosen = random.choice(songs)
        print(f"Random val: {chosen}")
    elif choice.isdigit() and 1 <= int(choice) <= len(songs):
        chosen = songs[int(choice) - 1]
    else:
        print("Vitlaus inntak.")
        return
    
    start_playing(chosen)


def play_random():
    """Spila random lag án að spyrja."""
    songs = get_songs()
    if not songs:
        print("Engin lög fundust!")
        return
    
    chosen = random.choice(songs)
    print(f"Random val: {chosen}")
    start_playing(chosen)


# Aðal kóði
if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stop":
            stop_playing()
        elif command == "random":
            play_random()
        elif command == "play_song":
            # Innra command, ekki notað beint
            if len(sys.argv) > 2:
                play_song(sys.argv[2])
        else:
            print(f"Óþekkt skipun: {command}")
            print("Notkun: python3 play.py [stop|random]")
    else:
        # Sjálfgefið — sýna lista
        show_menu_and_play()