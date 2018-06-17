#!/usr/bin/env python

import rospy

from testpy.msg import Dynamixelcontrol 
from testpy.srv	import Dynamixelcontrolarray,DynamixelcontrolarrayResponse

def count_words(request):
	return DynamixelcontrolarrayResponse(True)

rospy.init_node('dynamixel_writer')

service = rospy.Service('dynamixel_command', Dynamixelcontrolarray, count_words)

rospy.spin()
