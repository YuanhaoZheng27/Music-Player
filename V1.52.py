import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
from PIL import Image, ImageTk
import os
import glob

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x400")

        mixer.init()

        self.bg_image = Image.open(r"background1.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.playing = False

        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_music, font=("Helvetica", 12), bg="blue", fg="white")
        self.prev_button.place(relx=0.40, rely=0.1, anchor=tk.CENTER)

        self.next_button = tk.Button(root, text="Next", command=self.next_music, font=("Helvetica", 12), bg="orange", fg="white")
        self.next_button.place(relx=0.60, rely=0.1, anchor=tk.CENTER)

        self.play_button = tk.Button(root, text="Replay", command=self.play_music, font=("Helvetica", 12), bg="green", fg="white")
        self.play_button.place(relx=0.40, rely=0.25, anchor=tk.CENTER)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_music, font=("Helvetica", 12), bg="red", fg="white")
        self.stop_button.place(relx=0.60, rely=0.25, anchor=tk.CENTER)

        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume, label="Volumn", font=("Helvetica", 10))
        self.volume_scale.set(50)
        self.volume_scale.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.music_file_label = tk.Label(root, text="Current Music: ", font=("Helvetica", 10), anchor="w")
        self.music_file_label.place(relx=0.07, rely=0.75, anchor=tk.W)

        self.browse_button = tk.Button(root, text="Select Music Folder", command=self.browse_music_folder, font=("Helvetica", 10), bg="lightgray")
        self.browse_button.place(relx=0.07, rely=0.67, anchor=tk.W)

        self.music_list = []  
        self.current_index = 0

    def play_music(self):
        if self.music_list:
            self.stop_music()
            self.load_and_play_music(self.music_list[self.current_index])
            self.playing = True

    def stop_music(self):
        mixer.music.stop()
        self.playing = False

    def set_volume(self, val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)

    def browse_music_folder(self):
        try:
            folder_path = filedialog.askdirectory()
            if folder_path:
                self.music_list = glob.glob(os.path.join(folder_path, "*.mp3"))
                if not self.music_list:
                    messagebox.showwarning("Warning", "No MP3 file in selected folder.")
                else:
                    self.current_index = 0
                    self.load_and_play_music(self.music_list[self.current_index])
        except Exception as e:
            messagebox.showerror("Error", f"Error occurs: {str(e)}")

    def load_and_play_music(self, music_file):
        if music_file:
            mixer.music.load(music_file)
            mixer.music.play()
            self.music_file_label.config(text="Current Music: " + os.path.basename(music_file))
            self.current_index = self.music_list.index(music_file)

    def prev_music(self):
        if self.music_list:
            self.current_index = (self.current_index - 1) % len(self.music_list)
            self.play_music()

    def next_music(self):
        if self.music_list:
            self.current_index = (self.current_index + 1) % len(self.music_list)
            self.play_music()

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
