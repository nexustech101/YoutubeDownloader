import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pytube import YouTube
import threading

def progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = int((bytes_downloaded / total_size) * 100)
    progress_bar['value'] = percentage
    percentage_label.config(text=f"{percentage}%")
    root.update_idletasks()

def download_video():
    url = url_entry.get()
    download_path = path_entry.get()
    quality = quality_combobox.get()
    download_audio = var_chk_audio_only.get()

    status_label.config(text="Downloading... Please wait.")
    progress_bar['value'] = 0

    try:
        yt = YouTube(url, on_progress_callback=progress_callback)

        if download_audio:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            if quality == "High":
                stream = yt.streams.get_highest_resolution()
            elif quality == "Medium":
                stream = yt.streams.filter(res="480p").first()
            else:  # Low
                stream = yt.streams.filter(res="240p").first()

        stream.download(output_path=download_path)
        status_label.config(text=f"Downloaded {yt.title} successfully!")

    except Exception as e:
        status_label.config(text=f"Error downloading: {str(e)}")
        messagebox.showerror("Error", str(e))

    download_button["state"] = "normal"

def start_download_thread():
    download_thread = threading.Thread(target=download_video)
    download_thread.start()
    download_button["state"] = "disabled"

def browse_directory():
    folder = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder)

root = tk.Tk()
root.title("Enhanced YouTube Downloader")

# Organize the layout using a grid
url_label = tk.Label(root, text="YouTube Link:")
url_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

url_entry = tk.Entry(root, width=40)
url_entry.grid(row=0, column=1, padx=10, pady=5)

download_button = tk.Button(root, text="Download", command=start_download_thread)
download_button.grid(row=0, column=2, padx=10, pady=5)

path_label = tk.Label(root, text="Download Path:")
path_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

path_entry = tk.Entry(root, width=30)
path_entry.grid(row=1, column=1, padx=10, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=2, padx=10, pady=5)

quality_label = tk.Label(root, text="Quality:")
quality_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

quality_combobox = ttk.Combobox(root, values=["High", "Medium", "Low"])
quality_combobox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
quality_combobox.set("High")

var_chk_audio_only = tk.IntVar()
chk_audio_only = tk.Checkbutton(root, text="Audio Only", variable=var_chk_audio_only)
chk_audio_only.grid(row=2, column=2, padx=10, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=4, column=1, pady=5, columnspan=2)

progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
progress_bar.grid(row=5, column=1, pady=5, padx=10, columnspan=2, sticky=tk.EW)

percentage_label = tk.Label(root, text="0%")
percentage_label.grid(row=5, column=2, pady=5)

root.mainloop()
