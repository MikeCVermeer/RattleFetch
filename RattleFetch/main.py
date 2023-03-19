# Create a program that allows me to download youtube videos from a gui

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube
import os

# Create a class for the gui
class RattleFetch(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RattleFetch")
        self.geometry("600x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the entry box
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(pady=10)

        # Create a label for the entry box
        self.entry_label = ttk.Label(self.entry_frame, text="Enter a youtube url: ")
        self.entry_label.pack(side=tk.LEFT, padx=5)

        # Create an entry box
        self.entry_box = ttk.Entry(self.entry_frame, width=50)
        self.entry_box.pack(side=tk.LEFT, padx=5)

        # Create a frame for the buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        # Create a button to download the video
        self.download_button = ttk.Button(self.button_frame, text="Download", command=self.download)
        self.download_button.grid(row=0, column=0, padx=5)

        # Create a button to select a download location
        self.location_button = ttk.Button(self.button_frame, text="Select Location", command=self.select_location)
        self.location_button.grid(row=0, column=1, padx=5)

        # Create a frame for the progress bar
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(pady=10)

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=300, mode="determinate")
        self.progress_bar.pack()

    def download(self):
        # Get the url from the entry box
        url = self.entry_box.get()

        # Check if the url is empty
        if url == "":
            messagebox.showerror("Error", "Please enter a youtube url")
        else:
            # Try to download the video
            try:
                # Create a youtube object
                try:
                    yt = YouTube(url)
                except Exception as e2:
                    messagebox.showerror("Error", f"Could not create YouTube object: {e2}")
                    print('error')
                    return

                # Get the highest resolution video
                video = yt.streams.get_highest_resolution()

                # Get the title of the video
                title = video.title

                # Get the file size of the video
                file_size = video.filesize

                if file_size is None:
                    file_size = video.filesize_approx

                # Get the download location
                download_location = self.location

                # Create a label to show time remaining
                self.time_remaining_label = ttk.Label(self, text="Time Remaining: Calculating...")
                self.time_remaining_label.pack(pady=10)

                # Download the video
                video.download(download_location)

                # Update while downloading
                video.register_on_progress_callback(self.progress_function)

                # Create a label to show the download is complete
                self.complete_label = ttk.Label(self, text="Download Complete")
                self.complete_label.pack(pady=10)

                # Create a label to show the location of the video
                self.location_label = ttk.Label(self, text=f"Location: {download_location}")
                self.location_label.pack(pady=10)

                # Create a label to show the title of the video
                self.title_label = ttk.Label(self, text=f"Title: {title}")
                self.title_label.pack(pady=10)

                # Create a label to show the file size of the video
                self.file_size_label = ttk.Label(self, text=f"File Size: {file_size} bytes")
                self.file_size_label.pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", e)

    def progress_function(self, stream, chunk, bytes_remaining):
        # Set the progress bar color to green
        self.progress_bar["style"] = "green.Horizontal.TProgressbar"

        # Calculate the time remaining in seconds
        time_remaining = bytes_remaining / stream.filesize * stream.duration

        # Convert the time remaining to minutes and seconds
        minutes, seconds = divmod(time_remaining, 60)

        # Convert the time remaining to hours, minutes, and seconds
        hours, minutes = divmod(minutes, 60)

        # Format the time remaining
        time_remaining_formatted = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

        # Update the time remaining label
        self.time_remaining_label.config(text=f"Time Remaining: {time_remaining_formatted}")

        # Get the percentage of the file that has been downloaded
        percent = (1 - bytes_remaining / stream.filesize) * 100

        # Update the progress bar
        self.progress_bar["value"] = percent
        self.progress_bar.update()

    def select_location(self):
        # Open a file dialog to select a download location
        self.location = filedialog.askdirectory()

        # Check if the location is empty
        if self.location == "":
            messagebox.showerror("Error", "Please select a location")
        else:
            # Create a label to show the location
            self.location_label = ttk.Label(self, text=f"Location: {self.location}")
            self.location_label.pack(pady=10)

# Create an instance of the gui
app = RattleFetch()

# Start the gui
app.mainloop()

# To make this an executable:
# Option 1:
# run the command: pyinstaller --onefile --windowed main.py
# Option 2:
# run the command: python setup.py build