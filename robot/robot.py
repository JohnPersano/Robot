import numpy as np
from copy import deepcopy

from topography.obstacles import Obstacle


class Robot:
    """
    Class handles all movement and obstacle avoidance.
    """

    class State:
        NORMAL = 'normal'
        BATTERY_LOW = 'battery_low'
        FAILURE = 'failure'

    class Movement:
        NONE = 'none'
        LEFT = 'l'
        DOWN = 'd'
        RIGHT = 'r'
        UP = 'u'

    class Direction:
        NORTH = 'north'
        SOUTH = 'south'
        EAST = 'east'
        WEST = 'west'

    ALLOWED_MOVEMENTS = [Movement.LEFT, Movement.RIGHT, Movement.UP, Movement.DOWN]

    def __init__(self, movement_plane, obstacles, current_location: list, state: State=State.NORMAL):
        self.movement_plane = movement_plane
        self.obstacles = obstacles
        self.position = current_location
        self.state = state

        self.direction = Robot.Direction.NORTH

    def update_position(self, movement: str):
        """
        Move to the next position.
        Checks for map edges and obstacles.
        """
        proposed_position, proposed_direction = self._get_proposed_position_direction(movement)

        if self._proposed_position_valid(proposed_position):
            self.position, self.direction = self._update_with_obstacles(proposed_position, proposed_direction)
            print("Movement updated to location: {} and direction: {}".format(self.position, self.direction))
        else:
            print("That movement is not valid, it will make me fall off the map.")

    def _get_proposed_position_direction(self, movement):
        """
        Private method.
        Calculates the proposed position and direction based on the current position and direction.
        """

        proposed_position = deepcopy(self.position)
        proposed_direction = self.direction

        if movement == Robot.Movement.LEFT:
            if self.direction == Robot.Direction.NORTH:
                proposed_position[0] -= 1
                proposed_direction = Robot.Direction.WEST

            elif self.direction == Robot.Direction.SOUTH:
                proposed_position[0] += 1
                proposed_direction = Robot.Direction.EAST

            elif self.direction == Robot.Direction.EAST:
                proposed_position[1] += 1
                proposed_direction = Robot.Direction.NORTH

            elif self.direction == Robot.Direction.WEST:
                proposed_position[1] -= 1
                proposed_direction = Robot.Direction.SOUTH

        elif movement == Robot.Movement.RIGHT:
            if self.direction == Robot.Direction.NORTH:
                proposed_position[0] += 1
                proposed_direction = Robot.Direction.EAST

            elif self.direction == Robot.Direction.SOUTH:
                proposed_position[0] -= 1
                proposed_direction = Robot.Direction.WEST

            elif self.direction == Robot.Direction.EAST:
                proposed_position[1] -= 1
                proposed_direction = Robot.Direction.SOUTH

            elif self.direction == Robot.Direction.WEST:
                proposed_position[1] += 1
                proposed_direction = Robot.Direction.NORTH

        elif movement == Robot.Movement.DOWN:
            if self.direction == Robot.Direction.NORTH:
                proposed_position[1] -= 1
                proposed_direction = Robot.Direction.SOUTH

            elif self.direction == Robot.Direction.SOUTH:
                proposed_position[1] += 1
                proposed_direction = Robot.Direction.NORTH

            elif self.direction == Robot.Direction.EAST:
                proposed_position[0] -= 1
                proposed_direction = Robot.Direction.WEST

            elif self.direction == Robot.Direction.WEST:
                proposed_position[0] += 1
                proposed_direction = Robot.Direction.EAST

        elif movement == Robot.Movement.UP:
            if self.direction == Robot.Direction.NORTH:
                proposed_position[1] += 1
                proposed_direction = Robot.Direction.NORTH

            elif self.direction == Robot.Direction.SOUTH:
                proposed_position[1] -= 1
                proposed_direction = Robot.Direction.SOUTH

            elif self.direction == Robot.Direction.EAST:
                proposed_position[0] += 1
                proposed_direction = Robot.Direction.EAST

            elif self.direction == Robot.Direction.WEST:
                proposed_position[0] -= 1
                proposed_direction = Robot.Direction.WEST

        return proposed_position, proposed_direction

    def _proposed_position_valid(self, proposed_position):
        """
        Private method.
        Check for map edges.
        """
        if proposed_position[0] >= np.size(self.movement_plane, 0) or proposed_position[0] < 0:
            return False
        if proposed_position[1] >= np.size(self.movement_plane, 1) or proposed_position[1] < 0:
            return False
        return True

    def _update_with_obstacles(self, proposed_position, proposed_direction):
        """
        Private method.
        Checks the proposed position for any obstacles.
        """

        def handle_obstacle_action(obstacle):
            """
            Inner method.
            Handles all obstacle actions.
            """

            resolved_position = proposed_position
            resolved_direction = proposed_direction

            no_movement = obstacle.actions.get(Obstacle.Actions.NO_MOVEMENT, False)
            direct_position = obstacle.actions.get(Obstacle.Actions.DIRECT_POSITION, None)
            position_modifier = obstacle.actions.get(Obstacle.Actions.POSITION_MODIFIER, None)
            direction_modifier = obstacle.actions.get(Obstacle.Actions.DIRECTION_MODIFIER, None)

            print("I encountered a {} at {}.".format(obstacle.ob_type, proposed_position))

            if no_movement:
                print("\tAction: I should not move to that location")
                return self.position, resolved_direction

            if direct_position:
                print("\tAction: I teleported to {}".format(direct_position))
                resolved_position = direct_position
                return resolved_position, resolved_direction

            if position_modifier:
                resolved_position[0] += position_modifier[0]
                resolved_position[1] += position_modifier[1]
                print("\tAction: I moved to {}".format(resolved_position))
                return resolved_position, resolved_direction

            if direction_modifier:
                directions = [Robot.Direction.NORTH, Robot.Direction.EAST, Robot.Direction.SOUTH, Robot.Direction.WEST]
                direction_modifier %= 360

                current_index = directions.index(resolved_direction)
                current_index += direction_modifier // 90
                current_index %= len(directions)
                resolved_direction = directions[current_index]
                print("\tAction: I changed my direction to {}".format(resolved_direction))
                return resolved_position, resolved_direction

            return resolved_direction, resolved_direction

        # Check the next position for any obstacles
        for obstacle in self.obstacles:
            if obstacle.location == proposed_position:
                return handle_obstacle_action(obstacle)

        # No obstacles were found, move to proposed position
        return proposed_position, proposed_direction
