from flask import Blueprint, request, jsonify
import random
import time

bp = Blueprint('tracker', __name__)

# In-memory storage for peers grouped by info_hash
torrents = {}

@bp.route('/announce', methods=['GET'])
def announce():
    print("req received")
    info_hash = request.args.get('info_hash')
    ip = request.args.get('ip')
    port = int(request.args.get('port'))
    uploaded = int(request.args.get('uploaded'))
    downloaded = int(request.args.get('downloaded'))
    left = int(request.args.get('left'))
    compact = int(request.args.get('compact', 0))

    peer_id=str(ip)+''+ str(port)
    # Create a new torrent entry if it doesn't exist
    if info_hash not in torrents:
        print("in")
        torrents[info_hash] = {'peers': []}

    # Update the peer information or add a new peer
    peer_data = {
        'peer_id':peer_id,
        'ip': ip,
        'port': port,
        'uploaded': uploaded,
        'downloaded': downloaded,
        'left': left,
        'last_announce': time.time(),
    }
    # Check if the peer already exists in the list
    existing_peer = next((p for p in torrents[info_hash]['peers'] if p['peer_id'] == peer_id), None)
    if existing_peer:
        # Update the existing peer data
        existing_peer.update(peer_data)
    else:
        # Add a new peer to the list
        torrents[info_hash]['peers'].append(peer_data)
    
    print(torrents[info_hash]['peers'])

    # Select a random subset of peers from the swarm
    selected_peers = random.sample(torrents[info_hash]['peers'], min(10, len(torrents[info_hash]['peers'])))
    print(selected_peers)

    # Compact mode response
    if compact:
        compact_peers = []
        for peer in selected_peers:
            compact_peers.append(peer['ip'].encode() + peer['port'].to_bytes(2, 'big'))
        return jsonify({'peers': b''.join(compact_peers)})

    # Full response
    peer_list = []
    for peer in selected_peers:
        peer_list.append({
            'ip': peer['ip'],
            'port': peer['port'],
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