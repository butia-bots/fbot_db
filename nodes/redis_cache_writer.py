#!/usr/bin/env python3

import rclpy
from fbot_db.plugins import RedisCacheWriter

def main(args=None):
    rclpy.init(args=args)
    redis_cache_writer = RedisCacheWriter()
    rclpy.spin(redis_cache_writer)
    redis_cache_writer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()