"""Left Wall follower e-puck Webots python controller."""
# Author Łukasz Kała

from controller import Robot
from controller import Motor
from controller import DistanceSensor
from controller import PositionSensor
from enum import Enum


class Direction(Enum):
    FORWARD = 1
    BACK = 2
    LEFT = 3
    RIGHT = 4


# crete the Robot instance.
robot = Robot()

# get the time step of the current world.
time_step = int(robot.getBasicTimeStep())

maxMotorVelocity = 6.28

left_motor = Motor('left wheel motor')
right_motor = Motor('right wheel motor')

ds_front_right = DistanceSensor('ps0')
ds_front_left = DistanceSensor('ps7')
ds_front_right_right = DistanceSensor('ps1')
ds_front_left_left = DistanceSensor('ps6')
ds_left = DistanceSensor('ps2')
ds_right = DistanceSensor('ps5')

# initialization
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0)
right_motor.setVelocity(0)

ds_front_right.enable(time_step)
ds_front_left.enable(time_step)
ds_front_right_right.enable(time_step)
ds_front_left_left.enable(time_step)
ds_left.enable(time_step)
ds_right.enable(time_step)

direction = Direction.FORWARD
collide_area = 175
right_collide_area = 100
turning_right_dest = 88
turning_right = turning_right_dest
force_forward_value = 20
force_forward = 0
wall_value = 9
wall = -1

while robot.step(time_step) != -1:
    # Read the sensors:
    ds_front_right_value = ds_front_right.getValue()
    ds_front_right_right_value = ds_front_right_right.getValue()
    ds_front_left_value = ds_front_left.getValue()
    ds_front_left_left_value = ds_front_left_left.getValue()
    ds_right_value = ds_right.getValue()
    ds_left_value = ds_left.getValue()
    # Process sensor data:
    if direction == Direction.FORWARD:
        if force_forward > 0:
            left_motor.setVelocity(maxMotorVelocity)
            right_motor.setVelocity(maxMotorVelocity)
            force_forward -= 1
        elif wall >= 0:
            if wall == 0:
                direction = Direction.LEFT
            else:
                left_motor.setVelocity(maxMotorVelocity)
                right_motor.setVelocity(maxMotorVelocity)
            wall -= 1
        elif ds_right_value < right_collide_area:
            wall = wall_value
        elif ds_front_left_value >= collide_area and ds_front_right_value >= collide_area:
            direction = Direction.RIGHT
        else:
            left_motor.setVelocity(maxMotorVelocity)
            right_motor.setVelocity(maxMotorVelocity)
    elif direction == Direction.RIGHT:
        if turning_right > 0:
            left_motor.setVelocity(maxMotorVelocity / 8)
            right_motor.setVelocity(-maxMotorVelocity / 8)
            turning_right -= 1
        else:
            turning_right = turning_right_dest
            direction = Direction.FORWARD
    elif direction == Direction.LEFT:
        if turning_right > 0:
            left_motor.setVelocity(-maxMotorVelocity / 8)
            right_motor.setVelocity(maxMotorVelocity / 8)
            turning_right -= 1
        else:
            turning_right = turning_right_dest
            direction = Direction.FORWARD
            force_forward = force_forward_value
