import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class MusicPlayer:

    AUDIO_EXTENSIONS = (".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a")

    def __init__(self, music_dir):
        pygame.init()
        self.files = self.scan_audio_files(music_dir)
        self.index = 0
        self.paused = False
        self.loop = False
        self.volume = 0.7

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)

    def scan_audio_files(self, start_path):
        audio_files = []
        for root, _, files in os.walk(start_path):
            for file in files:
                if file.lower().endswith(self.AUDIO_EXTENSIONS):
                    audio_files.append(os.path.join(root, file))
        return sorted(audio_files)

    def play(self):
        pygame.mixer.music.load(self.files[self.index])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(self.SONG_END)
        print(f"\n▶ Playing: {os.path.basename(self.files[self.index])}")

    def pause_resume(self):
        if self.paused:
            pygame.mixer.music.unpause()
            print("▶ Resumed")
        else:
            pygame.mixer.music.pause()
            print("⏸ Paused")
        self.paused = not self.paused

    def next_song(self, auto=False):
        self.index += 1
        if self.index >= len(self.files):
            if self.loop:
                self.index = 0
            else:
                if auto:
                    print("⛔ Playlist finished")
                self.index -= 1
                return
        self.play()

    def prev_song(self):
        self.index -= 1
        if self.index < 0:
            if self.loop:
                self.index = len(self.files) - 1
            else:
                self.index = 0
                return
        self.play()

    def toggle_loop(self):
        self.loop = not self.loop
        print(f"🔁 Loop {'ON' if self.loop else 'OFF'}")

    def set_volume(self, value):
        self.volume = max(0.0, min(1.0, value))
        pygame.mixer.music.set_volume(self.volume)
        print(f"🎚 Volume: {int(self.volume * 100)}%")

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("⏹ Player stopped")


# ---------------- MAIN ----------------

path = "/Users/abhinav/Abhinav/Mini Project/Music_Player/Assets"
player = MusicPlayer(path)

if not player.files:
    print("❌ No audio files found.")
    exit()

print("\n🎵 Playlist:")
for i, song in enumerate(player.files, start=1):
    print(f"{i}. {os.path.basename(song)}")

player.play()

print("""
Controls:
p  → Pause / Resume
n  → Next song
b  → Previous song
l  → Toggle loop
+  → Volume up
-  → Volume down
q  → Quit
""")

while True:
    for event in pygame.event.get():
        if event.type == player.SONG_END:
            player.next_song(auto=True)

    cmd = input("Command: ").lower()

    if cmd == "p":
        player.pause_resume()
    elif cmd == "n":
        player.next_song()
    elif cmd == "b":
        player.prev_song()
    elif cmd == "l":
        player.toggle_loop()
    elif cmd == "+":
        player.set_volume(player.volume + 0.1)
    elif cmd == "-":
        player.set_volume(player.volume - 0.1)
    elif cmd == "q":
        player.stop()
        break
    else:
        print("❓ Unknown command")
