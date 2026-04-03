#!/usr/bin/env python3
import rospy
from visualization_msgs.msg import Marker, MarkerArray

def publish_grid_markers():
    rospy.init_node('grid_indexer_node', anonymous=True)
    marker_pub = rospy.Publisher('/grid_indices', MarkerArray, queue_size=10)
    rate = rospy.Rate(1) # Publish once per second

    while not rospy.is_shutdown():
        marker_array = MarkerArray()
        id_counter = 0

        for i in range(10):
            for j in range(10):
                marker = Marker()
                marker.header.frame_id = "odom"  # Tie to the standard fixed frame
                marker.header.stamp = rospy.Time.now()
                marker.ns = "grid_indices"
                marker.id = id_counter
                marker.type = Marker.TEXT_VIEW_FACING
                marker.action = Marker.ADD
                
                # Use the coordinate math
                marker.pose.position.x = 0.15 + (i * 0.3)
                marker.pose.position.y = 0.15 + (j * 0.3)
                marker.pose.position.z = 0.05 # Hover slightly above the floor
                
                marker.pose.orientation.w = 1.0
                
                # Scale dictates the text size
                marker.scale.z = 0.08 
                
                # Text Color (Yellow for visibility)
                marker.color.r = 1.0
                marker.color.g = 1.0
                marker.color.b = 0.0
                marker.color.a = 1.0 
                
                marker.text = f"[{i},{j}]"
                marker_array.markers.append(marker)
                
                id_counter += 1

        marker_pub.publish(marker_array)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_grid_markers()
    except rospy.ROSInterruptException:
        pass