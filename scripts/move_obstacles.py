#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

def move_obstacles():
    rospy.init_node('obstacle_mover', anonymous=True)
    
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    
    rate = rospy.Rate(50) 
    
    # Initialize Orange Model
    orange_msg = ModelState()
    orange_msg.model_name = 'dynamic_orange'
    orange_msg.reference_frame = 'world' # Explicitly lock to the world frame
    orange_msg.pose.orientation.w = 1.0

    # Initialize Purple Model
    purple_msg = ModelState()
    purple_msg.model_name = 'dynamic_purple'
    purple_msg.reference_frame = 'world'
    purple_msg.pose.orientation.w = 1.0

    speed = 0.2 
    travel_distance = 2.7 # Distance to travel before resetting

    while not rospy.is_shutdown():
        # Calculate the distance to subtract
        movement_offset = (rospy.get_time() * speed) % travel_distance
        
        # Because the world file already placed the link at [9,0] and [9,9],
        # we just apply a negative movement offset to the base model!
        
        # Orange moves strictly in the negative X direction
        orange_msg.pose.position.x = -movement_offset
        orange_msg.pose.position.y = 0.0
        orange_msg.pose.position.z = 0.0
        
        # Purple moves strictly in the negative Y direction
        purple_msg.pose.position.x = 0.0
        purple_msg.pose.position.y = -movement_offset
        purple_msg.pose.position.z = 0.0
        
        # Send commands to Gazebo
        try:
            set_state(orange_msg)
            set_state(purple_msg)
        except rospy.ServiceException as e:
            rospy.logwarn(f"Service call failed: {e}")
            
        rate.sleep()

if __name__ == '__main__':
    try:
        move_obstacles()
    except rospy.ROSInterruptException:
        pass