#!/usr/bin/env python3

import rclpy
from fbot_db.plugins import RedisRAGInjector

def main(args=None):
    rclpy.init(args=args)
    redis_rag_injector = RedisRAGInjector()
    rclpy.spin(redis_rag_injector)
    redis_rag_injector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()