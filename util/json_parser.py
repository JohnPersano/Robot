import json
from topography.obstacles import Obstacle


class JSONParser:
    """
    Parses JSON data and returns objects.
    """

    @staticmethod
    def get_obstacles(file_name='obstacles.json'):
        json_string = open(file_name, mode='r').read()
        json_data = json.loads(json_string)

        obstacles = []
        for obstacle_data in json_data:
            obstacles.append(Obstacle(**obstacle_data))
        return obstacles
