import requests

def get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left, compact=0):
    # Build the request URL with all parameters
    request_url = (
        f"{tracker_url}?info_hash={info_hash}&peer_id={peer_id}&ip={ip}&port={port}"
        f"&uploaded={uploaded}&downloaded={downloaded}&left={left}&compact={compact}"
    )

    # Make the HTTP GET request to the tracker
    response = requests.get(request_url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the response content to get the peer list
        peer_list = response.content
        return peer_list
    else:
        print(f"Error: Unable to get peer list. Status Code: {response.status_code}")
        return None

# Example usage
tracker_url = "http://127.0.0.1:6969/announce"
info_hash = "another_random_hash"  # Replace with the actual info hash
peer_id = "abcdefghij0123456789"  # Replace with the actual peer ID
ip = "127.0.0.1"  # Replace with the actual IP address of your client
port = 6881  # Replace with the actual port number
uploaded = 0  # Replace with the actual amount uploaded by your client
downloaded = 0  # Replace with the actual amount downloaded by your client
left = 1024  # Replace with the actual amount left to download by your client

peer_list = get_peer_list(tracker_url, info_hash, peer_id, ip, port, uploaded, downloaded, left)
if peer_list:
    print(f"Peer list from tracker: {peer_list.decode('utf-8')}")
