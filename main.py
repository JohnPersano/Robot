from robot.robot import Robot
from util.json_generator import generate_sample_obstacles
from util.json_parser import JSONParser
import numpy as np

# Generate the JSON file needed for obstacles
generate_sample_obstacles()

map_axis_size = 50
map_plane = np.zeros([map_axis_size, map_axis_size])
starting_location = [map_axis_size/2, map_axis_size/2]

robot = Robot(map_plane, JSONParser.get_obstacles(), starting_location)

# Human input movement
while (True):

    user_input = input('Enter a movement command')
    if user_input.lower() not in Robot.ALLOWED_MOVEMENTS:
        print("Error: {} is not a recognized movement".format(user_input))
        print("The allowed movements are {}.".format(Robot.ALLOWED_MOVEMENTS))
        continue

    robot.update_position(user_input)






