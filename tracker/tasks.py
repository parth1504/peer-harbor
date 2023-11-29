# tasks.py

from celery import Celery
from flask import Flask
import time
import random

app = Flask(__name__)

# Set up Celery
celery = Celery(
    app.import_name,
    broker='pyamqp://guest:guest@localhost:5672//',
    include=['tasks']
)
celery.conf.update(app.config)

# In-memory storage for peers grouped by info_hash
torrents = {}

@celery.task
def update_active_peers():
    # This function will be periodically executed
    print("Checking and updating active peers...")

    # Adjust the logic to check and update the active peers
    for info_hash, torrent_data in torrents.items():
        active_peers = []
        for peer in torrent_data['peers']:
            # Assuming last_announce is the timestamp of the last announcement
            # Adjust the threshold as needed
            if time.time() - peer['last_announce'] <= 30:
                active_peers.append(peer)
        torrent_data['peers'] = active_peers

        print(f"Active peers for {info_hash}: {active_peers}")

if __name__ == '__main__':
    celery.start()
