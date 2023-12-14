import os
import sys
from flask import Blueprint, request, jsonify
import random
import time

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(project_root)

from server.redisServer import RedisInstance

redis_client= RedisInstance()
bp = Blueprint('tracker', __name__)

# In-memory storage for peers grouped by info_hash
torrents = {}

@bp.route('/announce', methods=['GET'])
def announce():
    #print("req received")
    info_hash = request.args.get('info_hash')
    ip = request.args.get('ip')
    port = int(request.args.get('port'))
    # uploaded = int(request.args.get('uploaded'))
    # downloaded = int(request.args.get('downloaded'))
    # left = int(request.args.get('left'))
    # compact = int(request.args.get('compact', 0))

    peer_id=str(ip)+''+ str(port)
    # Create a new torrent entry if it doesn't exist
    if not redis_client.key_exists(info_hash):
        print("info_hash not found in Redis.")
    
    peers = redis_client.get_peers(info_hash)
    #print("out")
    #print(peers)

    # Update the peer information or add a new peer
    peer_data = {
        'peer_id':peer_id,
        'ip': ip,
        'port': port,
        # 'uploaded': uploaded,
        # 'downloaded': downloaded,
        # 'left': left,
        'last_announce': time.time(),
    }
    # Check if the peer already exists in the list
    if peers==None:
        peers=[]
        
    existing_peer = next((p for p in peers if p['peer_id'] == peer_id), None)
    if existing_peer:
        # Update the existing peer data
        existing_peer.update(peer_data)
    else:
        # Add a new peer to the list
        print("peer error")
        peers.append(frozenset(peer_data.items()))
        redis_client.add_peer(info_hash,peer_data)
    
    #print("gay")
    peers_list = [dict(peer_set) for peer_set in peers]


    # Select a random subset of peers from the swarm
    selected_peers = random.sample(peers, min(10, len(peers)))
    print(selected_peers)

    # # Compact mode response
    # if compact:
    #     compact_peers = []
    #     for peer in selected_peers:
    #         compact_peers.append(peer['ip'].encode() + peer['port'].to_bytes(2, 'big'))
    #     return jsonify({'peers': b''.join(compact_peers)})

    # Full response
    # peer_list = []
    # for peer in selected_peers:
    #     peer_list.append({
    #         'ip': peer['ip'],
    #         'port': peer['port'],
    #     })
    # print("here")
    return jsonify({'peers': peers_list})

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

@bp.route('/get_peers', methods=['GET'])
def get_peers():
    info_hash = request.args.get('info_hash')
    if(redis_client.key_exists(info_hash)):
        peers = redis_client.get_peers(info_hash)
        peers_list = [dict(peer_set) for peer_set in peers]
        return jsonify({'peers': peers_list})
    else:
        return jsonify({'error': 'Info hash not found'})
