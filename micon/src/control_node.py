#!/usr/bin/python

# import os

import rospy

from dynamixel_servomotor_controller import *
from micon.msg import Dynamixelcontrol 
from micon.srv  import Dynamixelcontrolarray,DynamixelcontrolarrayResponse
from xl_config import *
from getch import Getch


#from time import sleep


PROTOCOL_VERSION = 2.0

DXL_ID_BODY = 2
DXL_ID_TAIL = 1
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'

#The callback function for the service
def overwrite(request):

    motors = len(request.data)

    if motors != request.number_of_motors:
        print "Error: The number of motors is off"
        return DynamixelcontrolarrayResponse(False)

#This for loop will change the values for each motor as required
    for x in xrange(0,motors+1):
        if request.data[x].motor == "body":
            if request.data[x].mode == "positon":
                body_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_POSITION_CONTROL_MODE)  
                body_motor_controller.set_goal_position(request.data[x].angle)

            elif request.data[x].mode == "velocity":

            	intial_position = body_motor_controller.present_position()
                body_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)  
                body_motor_controller.set_goal_velocity(request.data[x].ang_velo)

                if request.data[x].angle > 0:
                	if intial_position < request.data[x].angle:
                		flag = -1
                	else:
                		flag = 1

                	while flag*(init_position - body_motor_controller.present_position()) > 0:
                	
                	body_motor_controller.set_goal_velocity(0.0)		

        if request.data[x].motor == "tail":
            if request.data[x].mode == "positon":
                tail_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_POSITION_CONTROL_MODE)  
                tail_motor_controller.set_goal_position(request.data[x].angle)

            elif request.data[x].mode == "velocity":

            	intial_position = tail_motor_controller.present_position()
                tail_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)  
                tail_motor_controller.set_goal_velocity(request.data[x].ang_velo)

                if request.data[x].angle > 0:
                	if intial_position < request.data[x].angle:
                		flag = -1
                	else:
                		flag = 1

                	while flag*(init_position - tail_motor_controller.present_position()) > 0:
                	
                	tail_motor_controller.set_goal_velocity(0.0)


print "start node."
rospy.init_node("servomotor_writer")


timer = rospy.Rate(0.5)



#Now initialising the motors 
body_motor_controller = DynamixelServomotorController(device_name = DEVICENAME, protocol_version = PROTOCOL_VERSION,\
                baudrate = BAUDRATE, motor_config = XLConfig())
body_motor_controller.current_id = DXL_ID_BODY

tail_motor_controller = DynamixelServomotorController(device_name = DEVICENAME, protocol_version = PROTOCOL_VERSION,\
                baudrate = BAUDRATE, motor_config = XLConfig())
tail_motor_controller.current_id = DXL_ID_TAIL

print "torque_enable: "
body_motor_controller.set_torque_enable(1)
tail_motor_controller.set_torque_enable(1) 

service = rospy.Service('servo_rewrite', Dynamixelcontrolarray, overwrite)


#body_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_POSITION_CONTROL_MODE)
#tail_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)

#Enabling torque



# while not rospy.is_shutdown():

rospy.spin()