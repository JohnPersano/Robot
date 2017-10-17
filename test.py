from robot.robot import Robot
from util.json_generator import generate_sample_obstacles
from util.json_parser import JSONParser
import numpy as np

# Generate the JSON file needed for obstacles
generate_sample_obstacles()

map_axis_size = 50
map_plane = np.zeros([map_axis_size, map_axis_size])
starting_location = [map_axis_size/2, map_axis_size/2]

# Spinner
print("Find the Spinner----------------------------------------------------------")
robot = Robot(map_plane, JSONParser.get_obstacles(), starting_location)
movement_string = 'd'
for movement in movement_string:
    robot.update_position(movement)
print('\n\n')

# Unknown
print("Find the Unknown----------------------------------------------------------")
robot = Robot(map_plane, JSONParser.get_obstacles(), starting_location)
movement_string = 'll'
for movement in movement_string:
    robot.update_position(movement)
print('\n\n')

# Rock
print("Find the Rock----------------------------------------------------------")
robot = Robot(map_plane, JSONParser.get_obstacles(), starting_location)
movement_string = 'luuuuuuuuu'
for movement in movement_string:
    robot.update_position(movement)
print('\n\n')

# Hole
print("Find the Hole----------------------------------------------------------")
robot = Robot(map_plane, JSONParser.get_obstacles(), starting_location)
movement_string = 'rur'
for movement in movement_string:
    robot.update_position(movement)
print('\n\n')




