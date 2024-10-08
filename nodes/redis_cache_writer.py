#!/usr/bin/env python3

import rospy
from fbot_db.plugins import RedisCacheWriter

if __name__ == '__main__':
  rospy.init_node('redis_cache_writer')
  rospy.loginfo('Starting redis cache writer')
  plugin = RedisCacheWriter()
  plugin.run()