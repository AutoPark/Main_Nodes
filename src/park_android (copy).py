#!/usr/bin/env python
import rospy
import roslib
import tf
import sys
from std_msgs.msg import Float32
import os.path, time



def park_android():
    file = open('Parking_Info.txt', 'r')
    carname = file.read()
    value = carname[4]
    carname = carname[0:4]
    value = float(value)
    print "Carname: ", carname, "value: ", value
    file.close()

    time_initial = time.ctime(os.path.getmtime('Parking_Info.txt'))

    publisher_topic = carname + '/Park'
    pub = rospy.Publisher(publisher_topic, Float32)
    rospy.init_node('park_android')

    current_time = rospy.get_rostime();


    while not rospy.is_shutdown():
        time_modified = time.ctime(os.path.getmtime('Parking_Info.txt'))
        if (time_initial != time_modified):
            time_initial = time_modified
            time.sleep(3)
            file = open('Parking_Info.txt', 'r')
            carname = file.read()
            value = carname[4]
            carname = carname[0:4]
            value = float(value)

            rospy.loginfo(value)
            pub.publish(value)
            file.close()


if __name__ == '__main__':
    try:
        park_android()
    except rospy.ROSInterruptException:
        pass
