#version 0.1 for ubuntu based linux

import os
import pygame
import threading
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from itertools import cycle

# Initialize pygame for audio
pygame.mixer.init()

def play_music(music_folder):
    for music_file in os.listdir(music_folder):
        if music_file.endswith('.mp3'):
            pygame.mixer.music.load(os.path.join(music_folder, music_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

def show_slideshow(image_folder, display_time=5):
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Set the window to full screen
    root.configure(bg='black')  # Set background color
    root.title("Slideshow")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    img_label = tk.Label(root, bg='black')
    img_label.place(relx=0.5, rely=0.5, anchor='center')

    image_files = [file for file in os.listdir(image_folder) if file.endswith('.jpg')]
    image_cycle = cycle(image_files)

    def update_image():
        image_file = next(image_cycle)
        try:
            img = Image.open(os.path.join(image_folder, image_file))
            img = ImageOps.exif_transpose(img)  # Correct the orientation

            # Resize if the image is larger than the screen
            if img.size[0] > screen_width or img.size[1] > screen_height:
                img.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo)
            img_label.image = photo  # Keep a reference!
            root.after(display_time * 1000, update_image)
        except IOError:
            print(f"Cannot open {image_file}")

    update_image()
    root.mainloop()

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the mp3s and image folders relative to the script's location
music_folder = os.path.join(script_dir, 'mp3s')
image_folder = os.path.join(script_dir, 'images')

# Run music and slideshow in separate threads
music_thread = threading.Thread(target=play_music, args=(music_folder,))
slideshow_thread = threading.Thread(target=show_slideshow, args=(image_folder,))

music_thread.start()
slideshow_thread.start()

music_thread.join()
slideshow_thread.join()
