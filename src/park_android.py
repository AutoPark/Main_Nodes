#!/usr/bin/env python
import rospy
import roslib
import tf
import sys
from std_msgs.msg import Float32
import os.path, time
from geometry_msgs.msg import PoseStamped



def park_android():
    file = open('Parking_Info.txt', 'r')
    carname = file.read()
    value = carname[4]
    carname = carname[0:4]
    value = float(value)
    file.close()

    time_initial = time.ctime(os.path.getmtime('Parking_Info.txt'))

    ## Three Publishers for car1, car2 and car3 to tell whether to park or unpark and which car.
    publisher_topic1 =  'car1/Park'
    pub1 = rospy.Publisher(publisher_topic1, Float32)
    publisher_topic2 =  'car2/Park'
    pub2 = rospy.Publisher(publisher_topic2, Float32)
    publisher_topic3 =  'car3/Park'
    pub3 = rospy.Publisher(publisher_topic3, Float32)
    ##

    ## Publishing goals for different cars
    goal1 =  'car1/move_base_simple/goal'
    pub_goal1 = rospy.Publisher(goal1, PoseStamped)
    goal2 =  'car2/move_base_simple/goal'
    pub_goal2 = rospy.Publisher(goal2, PoseStamped)
    goal3 =  'car3/move_base_simple/goal'
    pub_goal3 = rospy.Publisher(goal3, PoseStamped)
    rospy.init_node('park_android')

    current_time = rospy.get_rostime();
    # Goal Spot
    goal_spot = PoseStamped()
    goal_spot.header.stamp = current_time;
    goal_spot.header.frame_id = "/map";
    print "CN: ", carname


    while not rospy.is_shutdown():
        time_modified = time.ctime(os.path.getmtime('Parking_Info.txt'))
        # when the file "Parking_Info.txt" is changed that means command is received from the mobile
        if (time_initial != time_modified):
            time_initial = time_modified
            time.sleep(3)
            file = open('Parking_Info.txt', 'r')
            carname = file.read()
            value = carname[4]
            carname = carname[0:4]
            value = float(value)
            print "Va: ", value
            if value == 1.0:
                print "AA"
                files = '/home/naman/Desktop/AutoParking/parkcoord.txt'
                coordinates = open(files,'r');
                px = float(coordinates.readline());
                py = float(coordinates.readline());
                pz = float(coordinates.readline());
                angle = float(coordinates.readline());
                goal_spot.pose.position.x = px;
                goal_spot.pose.position.y = py;
                goal_spot.pose.position.z = pz;
                
                if angle==0:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = -0;
                    goal_spot.pose.orientation.w = 1;
                elif angle==180:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = 1;
                    goal_spot.pose.orientation.w = -0;
                elif angle==90:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = 0.706;
                    goal_spot.pose.orientation.w = 0.709;
                elif angle==-90:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = -0.706;
                    goal_spot.pose.orientation.w = 0.709;

            if value == 0.0:
                print "BB"
                files = '/home/naman/Desktop/AutoParking/exitcoord.txt'
                coordinates = open(files,'r');
                px = float(coordinates.readline());
                py = float(coordinates.readline());
                pz = float(coordinates.readline());
                angle = float(coordinates.readline());
                
                goal_spot.pose.position.x = px;
                goal_spot.pose.position.y = py;
                goal_spot.pose.position.z = pz;

                if angle==0:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = -0;
                    goal_spot.pose.orientation.w = 1;
                elif angle==180:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = 1;
                    goal_spot.pose.orientation.w = -0;
                elif angle==90:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = 0.706;
                    goal_spot.pose.orientation.w = 0.709;
                elif angle==-90:
                    goal_spot.pose.orientation.x = 0;
                    goal_spot.pose.orientation.y = 0;
                    goal_spot.pose.orientation.z = -0.706;
                    goal_spot.pose.orientation.w = 0.709;

            print goal_spot

            if carname == "car1":
                print "X"
                rospy.loginfo(value)
                pub1.publish(value)
                rospy.sleep(5.0)
                pub_goal1.publish(goal_spot)
            if carname == "car2":
                print "Y"
                rospy.loginfo(value)
                pub2.publish(value)
                rospy.sleep(5.0)
                pub_goal2.publish(goal_spot)
            if carname == "car3":
                print "Z"
                rospy.loginfo(value)
                pub3.publish(value)
                rospy.sleep(5.0)
                pub_goal3.publish(goal_spot)    
            file.close()


if __name__ == '__main__':
    try:
        park_android()
    except rospy.ROSInterruptException:
        pass
