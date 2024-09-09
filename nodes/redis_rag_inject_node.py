#!/usr/bin/env python3

import rospy
from fbot_db.plugins import RedisRAGInject

if __name__ == '__main__':
  rospy.init_node('redis_rag_inject')
  rospy.loginfo('Starting redis rag inject')
  plugin = RedisRAGInject()
  plugin.run()