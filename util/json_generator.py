import simplejson
from topography.obstacles import Obstacle


def generate_sample_obstacles(file_path='obstacles.json'):
    """
    Generates sample data for testing/demonstration purposes.
    """
    obstacles = [Obstacle(location=(27, 24), ob_type=Obstacle.Type.HOLE,
                          actions={Obstacle.Actions.DIRECT_POSITION: (10, 10)}),
                 Obstacle(location=(15, 25), ob_type=Obstacle.Type.ROCK,
                          actions={Obstacle.Actions.NO_MOVEMENT: True}),
                 Obstacle(location=(25, 24), ob_type=Obstacle.Type.SPINNER,
                          actions={Obstacle.Actions.DIRECTION_MODIFIER: 90}),
                 Obstacle(location=(24, 24), ob_type='unknown',
                          actions={Obstacle.Actions.NO_MOVEMENT: True})]
    # Save obstacles to JSON file
    ob_file = open(file_path, mode='w')
    ob_file.write(simplejson.dumps(obstacles))
    ob_file.close()
