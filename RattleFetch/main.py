# RattleFetch is a program that allows you to download YouTube videos from a simple GUI Interface

# Import the modules
import datetime
import platform
import subprocess
import sys
import time
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
        self.geometry("1920x1080")
        self.state("zoomed")
        self.resizable(True, True)
        self.create_widgets()
        self.style = ttk.Style()
        
        # Configure the styles
        self.style.configure("TFrame", background="#181818")
        self.style.configure("TLabel", background="#181818", foreground="#ff0000")
        self.style.configure("TButton", background="#181818", foreground="#ff0000")
        self.style.configure("TEntry", background="#282828", foreground="#ff0000", fieldbackground="#282828", insertcolor="#ffffff")
        self.style.configure("red.Horizontal.TProgressbar", background="#ff0000", troughcolor="#282828")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



    def create_widgets(self):
        self.container = ttk.Frame(self, padding=20)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.header_frame = ttk.Frame(self.container)
        self.header_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.title_label = ttk.Label(self.header_frame, text="RattleFetch", font=("Arial", 24), foreground="#ff0000")
        self.title_label.pack(side=tk.TOP)

        self.instructions_label = ttk.Label(
            self.header_frame,
            text="Enter a YouTube URL and select a location to download the video",
            font=("Arial", 14),
            foreground="#666",
        )
        self.instructions_label.pack(side=tk.TOP, pady=5)

        self.entry_frame = ttk.Frame(self.container, padding=20)
        self.entry_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.entry_label = ttk.Label(self.entry_frame, text="Enter a YouTube URL:")
        self.entry_label.pack(side=tk.LEFT, padx=5)

        self.entry_box = ttk.Entry(self.entry_frame, width=50, font=("Arial", 12))
        self.entry_box.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.button_frame = ttk.Frame(self.container, padding=20)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.get_video_button = ttk.Button(self.button_frame, text="Search", command=self.get_video, state=tk.DISABLED)
        self.get_video_button.pack(side=tk.LEFT, padx=5)

        self.location_button = ttk.Button(self.button_frame, text="Select Location", command=self.select_location)
        self.location_button.pack(side=tk.LEFT, padx=5)

        self.progress_frame = ttk.Frame(self.container, padding=20)
        self.progress_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, orient=tk.HORIZONTAL, length=400, mode="determinate", style="red.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=10, fill=tk.X, expand=True)

        self.footer_frame = ttk.Frame(self.container, padding=20)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.author_label = ttk.Label(self.footer_frame, text="Created by Mike Vermeer", font=("Arial", 10), foreground="#888")
        self.author_label.pack(side=tk.LEFT)

        self.version_label = ttk.Label(self.footer_frame, text="Version 0.5", font=("Arial", 10), foreground="#888")
        self.version_label.pack(side=tk.LEFT, padx=20)

        self.exit_button = ttk.Button(self.footer_frame, text="Exit", command=self.destroy)
        self.exit_button.pack(side=tk.RIGHT)

        # Set focus on the entry box
        self.entry_box.focus()

    def get_video(self):
        url = self.entry_box.get()
        if url == "":
            messagebox.showerror("Error", "Please enter a youtube url")
        else:
            try:
                yt = YouTube(url)

                self.progressive_or_non_progressive = messagebox.showinfo("Progressive or non progressive", "Do you want to download a progressive video or a non progressive video? \n\nProgressive videos are videos that are downloaded in one go. \n\nNon progressive videos are videos that are downloaded in multiple parts. The audio and video will be separate files. Nonprogressive allows for higher resolutions to be downloaded. \n\nProgressive videos only go up to 720p resolution. \n\nIf you are not sure, choose progressive.")

                # Create a label to show a video has been found
                self.video_found_label = ttk.Label(self.container, text="Video found!")
                self.video_found_label.pack(pady=10)

                # Create a frame for the video title
                self.title_frame = ttk.Frame(self.container)
                self.title_frame.pack(pady=10)

                # Create a label for the video title
                self.title_label = ttk.Label(self.title_frame, text="Video title: " + yt.title)
                self.title_label.pack(side=tk.LEFT, padx=5)

                # Ask the user if they want to progressive or non progressive video
                # Create a frame for the radio buttons
                self.radio_frame = ttk.Frame(self.container)
                self.radio_frame.pack(pady=10)

                # Create a label for the radio buttons
                self.radio_label = ttk.Label(self.radio_frame, text="Select a video type: ")
                self.radio_label.pack(side=tk.LEFT, padx=5)

                # Create a variable for the radio buttons
                self.radio_var = tk.IntVar()

                # Create the radio buttons
                self.radio_button1 = ttk.Radiobutton(self.radio_frame, text="Progressive", variable=self.radio_var, value=1)
                self.radio_button1.pack(side=tk.LEFT, padx=5)
                self.radio_button2 = ttk.Radiobutton(self.radio_frame, text="Non-Progressive", variable=self.radio_var, value=2)
                self.radio_button2.pack(side=tk.LEFT, padx=5)

                # Create a button to confirm the video type
                self.confirm_button = ttk.Button(self.radio_frame, text="Confirm", command=self.confirm)
                self.confirm_button.pack(side=tk.LEFT, padx=5)
            
            except:
                messagebox.showerror("Error", "Please enter a valid youtube url")
                

    def confirm(self):
        # Get the value of the radio button
        self.radio_var = self.radio_var.get()

        while True:
            # Check if the user selected progressive or non progressive
            if self.radio_var == 0:
                # If the user didn't select a video type, ask them to select a video type in a messagebox
                if messagebox.askquestion("Error", "You need to select a download type. \n\nDo you want to download a progressive video or a non progressive video? \n\n\nClick 'Yes' to download a progressive video. \n\nClick 'No' to download a non progressive video.") == "yes":
                    self.radio_var = 1
                    break
                else:
                    self.radio_var = 2
                    break
            elif self.radio_var == 2:
                self.progressive_or_non_progressive = "non_progressive"
                break
            elif self.radio_var == 1:
                self.progressive_or_non_progressive = "progressive"
                break

        if self.radio_var == 1 or self.radio_var == 2:
            # Destroy the radio buttons
            self.radio_frame.destroy()

            url = self.entry_box.get()

            yt = YouTube(url, on_progress_callback=self.progress_function)

            # Make a list that contains all the resolutions and fps rates of the video
            resolutions = []
            if self.progressive_or_non_progressive == "progressive":
                for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc():
                    resolutions.append(stream.resolution + " " + str(stream.fps) + "fps")
            else:
                for stream in yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc():
                    resolutions.append(stream.resolution + " " + str(stream.fps) + "fps")

            # Create a frame for the resolutions
            self.resolutions_frame = ttk.Frame(self.container)
            self.resolutions_frame.pack(pady=10)

            # Create a label for the resolutions
            self.resolutions_label = ttk.Label(self.resolutions_frame, text="Select a resolution: ")
            self.resolutions_label.pack(side=tk.LEFT, padx=5)

            # Create a combobox for the resolutions
            self.resolutions_combobox = ttk.Combobox(self.resolutions_frame, values=resolutions)
            self.resolutions_combobox.pack(side=tk.LEFT, padx=5)

            # Create a button to download the video
            self.download_button = ttk.Button(self.resolutions_frame, text="Download", command=self.download)
            self.download_button.pack(side=tk.LEFT, padx=5)

    def download(self):
        # Get the url from the entry box
        url = self.entry_box.get()

        # Get the resolution from the combobox
        resolution = self.resolutions_combobox.get()

        # Create a youtube object
        yt = YouTube(url, on_progress_callback=self.progress_function)

        # Get the video with the selected resolution
        video = yt.streams.filter(res=resolution.split(" ")[0], fps=int(resolution.split(" ")[1][:-3])).first()

        # Get the title of the video
        title = video.title

        # Get the file size of the video
        byte_size = video.filesize
        if byte_size is None:
            byte_size = video.filesize_approx

        # Convert the byte size to a human readable format
        mb_size = video.filesize / 1024 / 1024

        # Create a label to show time remaining
        self.time_remaining_label = ttk.Label(self.container, text="Your download is complete in a few seconds.")
        self.time_remaining_label.pack(pady=10)

        # Download the video, and update the progress bar while downloading
        if self.progressive_or_non_progressive == "non_progressive":
            download_location = self.location + "/" + title
            video.download(download_location, filename=title + "_video." + video.subtype)
            audio = yt.streams.get_audio_only()
            audio.download(download_location, filename=title + "_audio." + audio.subtype)
        elif self.progressive_or_non_progressive == "progressive":
            download_location = self.location
            video.download(download_location, filename=title + "." + video.subtype)
        else:
            messagebox.showerror("Error", "Something went wrong, radio_var is not 1 or 2.")

        # Destroy widgets
        self.progress_bar.destroy()
        self.time_remaining_label.destroy()
        self.download_button.destroy()
        self.resolutions_combobox.destroy()
        self.resolutions_label.destroy()
        self.resolutions_frame.destroy()
        self.entry_box.destroy()
        self.video_found_label.destroy()
        self.location_label.destroy()
        self.title_label.destroy()
        self.get_video_button.destroy()
        self.location_button.destroy()
        self.entry_label.destroy()
        
        # Destroy the frames that contain the widgets that were destroyed
        self.entry_frame.destroy()
        self.title_frame.destroy()
        self.button_frame.destroy()
        self.radio_frame.destroy()
        self.progress_frame.destroy()
        self.resolutions_frame.destroy()

        # Create a label to show the download is complete
        self.complete_label = ttk.Label(self.container, text="Download Complete")
        self.complete_label.pack(pady=10)

        # Create a label to show the location of the video
        self.location_label = ttk.Label(self.container, text=f"Location: {download_location}")
        self.location_label.pack(pady=10)

        # Create a label to show the title of the video
        self.title_label = ttk.Label(self.container, text=f"Title: {title}")
        self.title_label.pack(pady=10)

        # Create a label to show the file size of the video
        self.file_size_label = ttk.Label(self.container, text=f"File Size: {mb_size} Megabytes")
        self.file_size_label.pack(pady=10)

        # Create a button to open the location of the video and exit the program
        self.open_button = ttk.Button(self.container, text="Open Location", command=lambda: self.open_location(download_location))
        self.open_button.pack(pady=10)


    def open_location(self, download_location):
        # Open the location of the video

        # Check if the operating system is windows
        if platform.system() == "Windows":
            # Open the location of the video
            os.startfile(download_location)

            # Exit the program
            sys.exit()

        # Check if the operating system is mac
        elif platform.system() == "Darwin":
            # Open the location of the video
            subprocess.Popen(["open", download_location])

            # Exit the program
            sys.exit()

        # Check if the operating system is linux
        elif platform.system() == "Linux":
            # Open the location of the video
            subprocess.Popen(["xdg-open", download_location])

            # Exit the program
            sys.exit()


    def progress_function(self, stream, chunk, bytes_remaining):
        # Set the progress bar color to red
        self.progress_bar["style"] = "red.Horizontal.TProgressbar"

        # Calculate the time remaining without using time.duration
        # Get the file size of the video
        file_size = stream.filesize

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
            self.location_label = ttk.Label(self.container, text=f"Location: {self.location}")
            self.location_label.pack(pady=10)

        #Enable the Search button called get_video_button
        self.get_video_button["state"] = "normal"

    def destroy(self) -> None:
        return super().destroy()


if __name__ == "__main__":
    # Create an instance of the gui
    app = RattleFetch()

    # Start the gui
    app.mainloop()

# To make this an executable:
# Option 1:
# run the command: pyinstaller --onefile --windowed main.py
# Option 2:
# run the command: python setup.py build