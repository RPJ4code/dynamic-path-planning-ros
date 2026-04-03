#!/usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

def move_obstacles():
    rospy.init_node('obstacle_mover', anonymous=True)
    
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    
    rate = rospy.Rate(50) 
    
    # Initialize Models
    models = {
        'orange': ModelState(),
        'purple': ModelState(),
        'blue': ModelState(),
        'green': ModelState()
    }

    # Setup base references
    for name, msg in models.items():
        msg.model_name = f'dynamic_{name}'
        msg.reference_frame = 'world'
        msg.pose.orientation.w = 1.0

    speed = 0.2 
    travel_distance = 2.7 

    while not rospy.is_shutdown():
        # Calculate the base offset
        movement_offset = (rospy.get_time() * speed) % travel_distance
        
        # Orange: Starts at [9,0], moves -X
        models['orange'].pose.position.x = -movement_offset
        models['orange'].pose.position.y = 0.0
        
        # Purple: Starts at [9,9], moves -Y
        models['purple'].pose.position.x = 0.0
        models['purple'].pose.position.y = -movement_offset

        # Green: Starts at [9,5], moves -X
        models['green'].pose.position.x = -movement_offset
        models['green'].pose.position.y = 0.0 
        
        # Blue: Starts at [5,0], moves +Y (Notice this is positive!)
        models['blue'].pose.position.x = 0.0
        models['blue'].pose.position.y = movement_offset
        
        # Send commands to Gazebo
        try:
            for msg in models.values():
                set_state(msg)
        except rospy.ServiceException as e:
            rospy.logwarn(f"Service call failed: {e}")
            
        rate.sleep()

if __name__ == '__main__':
    try:
        move_obstacles()
    except rospy.ROSInterruptException:
        pass