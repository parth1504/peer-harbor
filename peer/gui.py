import tkinter as tk
from tkinter import filedialog

def upload_file():
    file_path = filedialog.askopenfilename()

def search_file():
    query = search_entry.get()

root = tk.Tk()
root.title("Peer-to-Peer File Sharing")

search_label = tk.Label(root, text="Search for a file:")
search_label.pack(pady=10)

search_entry = tk.Entry(root, width=30)
search_entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=search_file)
search_button.pack(pady=10)

upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

root.mainloop()
