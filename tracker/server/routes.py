from flask import Blueprint, request, jsonify
import random
import time

bp = Blueprint('tracker', __name__)

# In-memory storage for peers grouped by info_hash
torrents = {}

@bp.route('/announce', methods=['GET'])
def announce():
    print("req recedived")
    info_hash = request.args.get('info_hash')
    peer_id = request.args.get('peer_id')
    ip = request.args.get('ip')
    port = int(request.args.get('port'))
    uploaded = int(request.args.get('uploaded'))
    downloaded = int(request.args.get('downloaded'))
    left = int(request.args.get('left'))
    compact = int(request.args.get('compact', 0))

    # Create a unique identifier for the peer
    peer_key = f"{info_hash}-{peer_id}"

    # Create a new torrent entry if it doesn't exist
    if info_hash not in torrents:
        torrents[info_hash] = {'peers': {}}

    # Update the peer information or add a new peer
    torrents[info_hash]['peers'][peer_key] = {
        'ip': ip,
        'port': port,
        'uploaded': uploaded,
        'downloaded': downloaded,
        'left': left,
        'last_announce': time.time(),
    }
    

    # Select a random subset of peers from the swarm
    selected_peers = random.sample(torrents[info_hash]['peers'].keys(), min(10, len(torrents[info_hash]['peers'])))

    # Compact mode response
    if compact:
        compact_peers = []
        for peer_key in selected_peers:
            compact_peers.append(torrents[info_hash]['peers'][peer_key]['ip'].encode() + torrents[info_hash]['peers'][peer_key]['port'].to_bytes(2, 'big'))
        return jsonify({'peers': b''.join(compact_peers)})

    # Full response
    peer_list = []
    for peer_key in selected_peers:
        peer_list.append({
            'ip': torrents[info_hash]['peers'][peer_key]['ip'],
            'port': torrents[info_hash]['peers'][peer_key]['port'],
        })

    return jsonify({'peers': peer_list})

@bp.route('/scrape', methods=['GET'])
def scrape():
    info_hash = request.args.getlist('info_hash')

    # Scrape information for each torrent (info_hash)
    scrape_data = {}
    for hash_value in info_hash:
        if hash_value in torrents:
            scrape_data[hash_value] = {
                'complete': len([peer_key for peer_key in torrents[hash_value]['peers'] if torrents[hash_value]['peers'][peer_key]['left'] == 0]),
                'downloaded': len([peer_key for peer_key in torrents[hash_value]['peers'] if torrents[hash_value]['peers'][peer_key]['downloaded'] > 0]),
                'incomplete': len(torrents[hash_value]['peers']),
            }

    return jsonify({'files': scrape_data})