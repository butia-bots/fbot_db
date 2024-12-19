import rclpy
from rclpy.node import Node
import uuid
from fbot_db.srv import RedisCacheWriterSrv

from .world_plugin import WorldPlugin

class RedisCacheWriter(WorldPlugin, Node):

    def __init__(self):
        WorldPlugin.__init__(self, 'writer_world_plugin')
        Node.__init__(self, 'redis_cache_writer')
        self.cache = {}
        self.srv = self.create_service(RedisCacheWriterSrv, 'redis_cache_writer_srv', self._on_recognition)
        
    def _generate_uid(self):
        return str(uuid.uuid4())
    
    def _toCompose(self, request):
        composed = {}
        data = request.description
        composed['face_encode'] = []
        for item in data.descriptions:
            composed['label'] = item.label
            composed['face_encode'].append(item.encoding)
        return composed
    
    def _pushToRedis(self, data):
        description_id = '{label}:{id}'.format(
                label='faces',
                id=self._generate_uid()
            ).encode('utf-8')
        try:
            self.r.hset(description_id, 'content', str(data))
        except Exception as e:
            self.get_logger().error(str(e))
        return 
  
    def _on_recognition(self, request, response):
        try:
            composed = self._toCompose(request)
            self._pushToRedis(composed)
            self.get_logger().info('Data pushed to Redis')
            response.success = True
        except Exception as e:
            self.get_logger().error(str(e))
            response.success = False
        return response