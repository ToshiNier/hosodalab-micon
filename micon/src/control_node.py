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

DXL_ID_BODY = 1
DXL_ID_TAIL = 2
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
                body_motor_controller.set_goal_position(request.data[x].value)

            elif request.data[x].mode == "velocity":
                body_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)  
                body_motor_controller.set_goal_velocity(request.data[x].value)

        if request.data[x].motor == "tail":
            if request.data[x].mode == "positon":
                tail_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_POSITION_CONTROL_MODE)  
                tail_motor_controller.set_goal_position(request.data[x].value)

            elif request.data[x].mode == "velocity":
                tail_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)  
                tail_motor_controller.set_goal_velocity(request.data[x].value)
def main():
    print "start node."
    rospy.init_node("servomotor_writer")
    service = rospy.Service('servo_rewrite', WordCount, count_words)

    timer = rospy.Rate(0.5)


   
    #Now initialising the motors 
    body_motor_controller = DynamixelServomotorController(device_name = DEVICENAME, protocol_version = PROTOCOL_VERSION,\
                    baudrate = BAUDRATE, motor_config = XLConfig())
    body_motor_controller.current_id = DXL_ID_BODY

    tail_motor_controller = DynamixelServomotorController(device_name = DEVICENAME, protocol_version = PROTOCOL_VERSION,\
                    baudrate = BAUDRATE, motor_config = XLConfig())
    tail_motor_controller.current_id = DXL_ID_TAIL


    body_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_POSITION_CONTROL_MODE)
    tail_motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)

    #Enabling torque
    print "torque_enable: "
    body_motor_controller.set_torque_enable(1)
    tail_motor_controller.set_torque_enable(1) 


    #print "id: " + str(motor_controller.id())
    #print "baudrate: " + str(motor_controller.baudrate())
    #print "torque_enable: " + str(motor_controller.torque_enable())



    # speed = 0.0
    # dir = 0.2
    # max_speed = 0.5



    # sw = False

    # getch = Getch()

    while not rospy.is_shutdown():
        # sw ^= True

        # motor_controller.set_led(int(sw))

        # motor_controller.set_goal_position(0 if sw else 180)
        # motor_controller.set_goal_position(0.0)


        #print "present_position: " + str(motor_controller.present_position())

        # print getch()
        # continue

        print "cmd << ",
        cmd = raw_input()

        isAccepted = True
        if(cmd == "exit"):
            print "program is now to end..."
            break
        else:
            try:
                speed = float(cmd)
                print "speed: " + str(speed)
                # motor_controller.set_goal_velocity(speed)
            except:
                isAccepted = False


        if not isAccepted:
            print "[Error] command parse error!"

        print "OK"

        # print "loop"

        # motor_controller.set_goal_velocity(speed)
        # print "max_position: " +  str(motor_controller.max_position_limit())
        # print "min_position: " +  str(motor_controller.min_position_limit())

        # speed += dir
        # if speed > max_speed:
        #     speed = max_speed
        #     dir *= -1

        # if speed < -max_speed:
        #     speed = -max_speed
        #     dir *= -1

        # print str(speed)

        timer.sleep()

    motor_controller.set_led(0)
    motor_controller.set_goal_velocity(0.0)
    motor_controller.end()


if __name__ == "__main__":
    main()
