import tkinter as tk
from tkinter import ttk
import requests

def get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0):
    request_url = (
        f"{tracker_url}?info_hash={info_hash}&peer_id={peer_id}&ip={ip}&port={port}"
        f"&uploaded={uploaded}&downloaded={downloaded}&left={left}&compact={compact}"
    )

    response = requests.get(request_url)

    if response.status_code == 200:
        peer_list = response.content
        return peer_list
    else:
        print(f"Error: Unable to get peer list. Status Code: {response.status_code}")
        return None

def on_submit():
    tracker_url = tracker_entry.get()
    info_hash = info_hash_entry.get()
    peer_id = peer_id_entry.get()
    ip = ip_entry.get()
    port = int(port_entry.get())
    uploaded = int(uploaded_entry.get())
    downloaded = int(downloaded_entry.get())
    left = int(left_entry.get())

    peer_list = get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left)
    if peer_list:
        result_label.config(text=f"Peer list from tracker: {peer_list.decode('utf-8')}")

# Create the main window
window = tk.Tk()
window.title("Peer Client GUI")

# Create and place widgets
tracker_label = ttk.Label(window, text="Tracker URL:")
tracker_entry = ttk.Entry(window)

info_hash_label = ttk.Label(window, text="Info Hash:")
info_hash_entry = ttk.Entry(window)

peer_id_label = ttk.Label(window, text="Peer ID:")
peer_id_entry = ttk.Entry(window)

ip_label = ttk.Label(window, text="IP:")
ip_entry = ttk.Entry(window)

port_label = ttk.Label(window, text="Port:")
port_entry = ttk.Entry(window)

uploaded_label = ttk.Label(window, text="Uploaded:")
uploaded_entry = ttk.Entry(window)

downloaded_label = ttk.Label(window, text="Downloaded:")
downloaded_entry = ttk.Entry(window)

left_label = ttk.Label(window, text="Left:")
left_entry = ttk.Entry(window)

submit_button = ttk.Button(window, text="Submit", command=on_submit)

result_label = ttk.Label(window, text="")

# Grid layout
tracker_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
tracker_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

info_hash_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
info_hash_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

peer_id_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
peer_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

ip_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
ip_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

port_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
port_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

uploaded_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
uploaded_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

downloaded_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
downloaded_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

left_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
left_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

submit_button.grid(row=8, column=0, columnspan=2, pady=10)
result_label.grid(row=9, column=0, columnspan=2)

# Run the main loop
window.mainloop()
