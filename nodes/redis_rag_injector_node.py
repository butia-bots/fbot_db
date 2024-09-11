#!/usr/bin/env python3

import rospy
from fbot_db.plugins import RedisRAGInjector

if __name__ == '__main__':
  rospy.init_node('redis_rag_injector')
  rospy.loginfo('Starting redis rag inject')
  plugin = RedisRAGInjector()
  plugin.run()