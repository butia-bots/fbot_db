from abc import abstractmethod

import rclpy
from rclpy.node import Node
import redis

class WorldPlugin(Node):

    def __init__(self, node_name):
        super().__init__(node_name)
        redis_params = self.get_parameter('/fbot_db/redis').value
        self.r = redis.Redis(**redis_params)
        self.fixed_frame = self.get_parameter('/fbot_db/fixed_frame').value

    @abstractmethod
    def run(self):
        raise NotImplementedError