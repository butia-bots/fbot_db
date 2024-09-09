#!/usr/bin/env python3

import rospy
from fbot_db.plugins import RedisRAGRetriever

if __name__ == '__main__':
  rospy.init_node('redis_rag_retriever')
  rospy.loginfo('Starting redis rag retriever')
  plugin = RedisRAGRetriever()
  plugin.run()