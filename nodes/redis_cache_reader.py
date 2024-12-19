#!/usr/bin/env python3

import rclpy
from fbot_db.plugins import RedisCacheReader

def main(args=None):
    rclpy.init(args=args)
    redis_cache_reader = RedisCacheReader()
    rclpy.spin(redis_cache_reader)
    redis_cache_reader.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
  main()