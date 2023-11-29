import pickle
import redis
import os
from dotenv import load_dotenv

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
        peer_data = pickle.dumps(peer)
        self.r.sadd(infohash, peer_data)

    def remove_peer(self, infohash, peer):
        # Remove the peer from the set corresponding to the infohash
        peer_data = pickle.dumps(peer)
        self.r.srem(infohash, peer_data)

    def get_peers(self, infohash):
        # Get all peers in the set corresponding to the infohash
        return [pickle.loads(peer_data) for peer_data in self.r.smembers(infohash)]
        #return self.r.smembers(infohash)
    
    def key_exists(self, key):
        # Check if the key exists in Redis
        return self.r.exists(key)

load_dotenv()
r=RedisInstance()
r.check_redis_connection()
