import rclpy
from rclpy.node import Node
from fbot_vision_msgs.msg import FaceEncoding, FaceDescription
from std_msgs.msg import Header
from fbot_db.srv import RedisCacheReaderSrv

from .world_plugin import WorldPlugin

class RedisCacheReader(WorldPlugin, Node):

    def __init__(self):
        WorldPlugin.__init__(self, 'reader_world_plugin')
        Node.__init__(self, 'redis_cache_reader')
        self.cache = {}
        self.srv = self.create_service(RedisCacheReaderSrv, 'redis_cache_reader_srv', self.get_from_redis_cache)
        self.get_logger().info('Cache is being updated')
        
    def get_from_redis_cache(self, request, response):
        data = self._get_data_from_redis()
        response.data = data
        return response
    
    def _get_data_from_redis(self, pattern='faces:*'):
        cursor = 0
        # Scan keys matching the pattern "faces:*"
        while True:
            count, keys = self.r.scan(cursor, match=pattern)
            for key in keys:
                hash_value = self.r.hgetall(key)
                self.cache[key] = hash_value
            cursor = count
            if cursor == 0:
                break
        data = self.encapsulate_data()
        return data
    
    def encapsulate_data(self):
        redis_cache = FaceEncoding()
        h = Header()
        h.stamp = self.get_clock().now().to_msg()
        redis_cache.header = h
        
        for key, item in self.cache.items():
            item_str = {k.decode('utf-8'): v for k, v in item.items()}
            content_dict = eval(item_str['content'])  # Convert string to dictionary
            label = content_dict['label']
            encodings = content_dict['face_encode']
            
            h = Header()
            h.stamp = self.get_clock().now().to_msg()
            h.frame_id = key.decode('utf-8')
            
            for encoding in encodings:
                description = FaceDescription()
                description.header = h
                description.global_id = key.decode('utf-8')
                description.label = label
                description.encoding = encoding
                redis_cache.descriptions.append(description)
            
        return redis_cache