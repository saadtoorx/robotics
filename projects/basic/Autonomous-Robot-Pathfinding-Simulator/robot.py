
# My First Virtual Robot
# Project 01 - Robotics Portfolio

# Robot's starting position
robot_position = 0

print("Robot started!")
print("Starting position:", robot_position)

# Move the robot forward ten steps
for step in range(1, 11):
    robot_position = robot_position + 1
    print("Step", step, "- Position:", robot_position)

print("Robot stopped!")
print("Final position:", robot_position)
