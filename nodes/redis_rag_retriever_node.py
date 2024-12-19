#!/usr/bin/env python3

import rclpy
from fbot_db.plugins import RedisRAGRetriever

def main(args=None):
    rclpy.init(args=args)
    redis_rag_retriever = RedisRAGRetriever()
    rclpy.spin(redis_rag_retriever)
    redis_rag_retriever.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()