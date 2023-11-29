import base64
import pickle
import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")

class RedisInstance:
    def __init__(self):
        # Get Redis details from environment variables
        redis_host = os.getenv("REDIS_HOST")
        redis_port = int(os.getenv("REDIS_PORT"))
        redis_password = os.getenv("REDIS_PASSWORD")
        # Connect to Redis
        self.r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    def check_redis_connection(self):
        try:
            # Ping the server to check if the connection is alive
            response = self.r.ping()

            if response:
                print("Connection to Redis successful.")
                return self.r
            else:
                raise ConnectionRefusedError("Connected to Redis, but ping failed. Check Redis server health.")

        except ConnectionError as e:
            print(f"Error connecting to Redis: {e}")

    def add_peer(self, infohash, peer):
        # Add the peer to the set corresponding to the infohash
        print("in add peer")
        print("Peer Data:", peer)
        encoded_data = base64.b64encode(pickle.dumps(peer))

        # peer_data_bytes = pickle.dumps(peer)
        # print("Serialized Data:", peer_data_bytes)
        self.r.sadd(infohash, encoded_data)

    def remove_peer(self, infohash, peer):
        # Remove the peer from the set corresponding to the infohash
        print("in remove peer")
        peer_data = pickle.dumps(peer)
        print(peer_data)
        self.r.srem(infohash, peer_data)

    def get_peers(self, infohash):
        # Get all peers in the set corresponding to the 
        print("In get peers")

        set_members = self.r.smembers(infohash)
        decoded_data = [pickle.loads(base64.b64decode(member)) for member in set_members]
        return decoded_data

        
    def key_exists(self, key):
        # Check if the key exists in Redis
        print("in key exists")
        return self.r.exists(key)


# r= redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
# set_members = r.smembers("random_info_hash")
# decoded_data = [pickle.loads(base64.b64decode(member)) for member in set_members]

# print(decoded_data)

