import time
from Robot import RobotClass  # Assuming Robot.py is in the same directory
from Gamepad import GamepadClass  # Assuming Gamepad.py is in the same directory

front_left_mod = .8 
front_right_mod = 1
rear_left_mod = 1
rear_right_mod = 1

# Initialize the gamepad and robot
gamepad = GamepadClass()
robot = RobotClass()

# Find motor controllers automatically
robot.find_motor_controllers()

# Ensure at least two motor controllers are found
if len(robot.controllers) < 2:
    print("At least two motor controllers required. Exiting.")
    exit()

# Assuming we're controlling the first two found motor controllers
controller_ids = list(robot.controllers.keys())[:2]
controller_id_1 = controller_ids[0]  # Controls two motors (MOTOR_A and MOTOR_B)
print("Controller 1", controller_id_1);
controller_id_1 = "HWMDBDDVUD"
controller_id_2 = controller_ids[1]  # Controls two motors (MOTOR_C and MOTOR_D)
controller_id_2 = "AXTDAORLJE";

print("Controller 2", controller_id_2);

# Optionally invert motor directions for specific wheels
robot.set_value(controller_id_1, "invert_velocity_a", 1)  # Front left wheel
robot.set_value(controller_id_1, "invert_velocity_b", 1)  # Front right wheel
robot.set_value(controller_id_2, "invert_velocity_a", 0)  # Rear left wheel
robot.set_value(controller_id_2, "invert_velocity_b", 0)  # Rear right wheel

# Function to map joystick values (-1 to 1) to PWM values (-1 to 1)
def map_joystick_to_pwm(value):
    return max(min(value, 1), -1)

try:
    while True:
        # Get the joystick values
        left_y = gamepad.get_value("joystick_left_y")  # Forward/backward
        left_x = gamepad.get_value("joystick_left_x")  # Strafing left/right
        right_x = gamepad.get_value("joystick_right_x")  # Rotation

        # Map joystick values to motor power (-1 to 1)
        forward_backward = map_joystick_to_pwm(left_y)  # Forward/backward motion
        strafe = map_joystick_to_pwm(right_x)            # Strafing motion
        rotation = map_joystick_to_pwm(left_x)         # Rotational motion

        # Calculate motor speeds for holonomic drive
        front_left_pwm = (forward_backward + strafe - rotation) * front_left_mod  # Front left wheel
        front_right_pwm = (forward_backward - strafe + rotation)  * front_right_mod # Front right wheel
        rear_left_pwm = (forward_backward - strafe + rotation) * rear_left_mod  # Rear left wheel
        rear_right_pwm = (forward_backward + strafe - rotation) * rear_right_mod  # Rear right wheel

        # Ensure the motor power values are within the range (-1, 1)
        front_left_pwm = max(min(front_left_pwm, 1), -1)
        front_right_pwm = max(min(front_right_pwm, 1), -1)
        rear_left_pwm = max(min(rear_left_pwm, 1), -1)
        rear_right_pwm = max(min(rear_right_pwm, 1), -1)

        # Set motor velocities for both motor controllers
        # Front left (MOTOR_A of controller_id_1) and front right (MOTOR_B of controller_id_1)
        robot.set_value(controller_id_1, "velocity_a", front_left_pwm)
        robot.set_value(controller_id_1, "velocity_b", front_right_pwm)

        # Rear left (MOTOR_A of controller_id_2) and rear right (MOTOR_B of controller_id_2)
        robot.set_value(controller_id_2, "velocity_a", rear_left_pwm)
        robot.set_value(controller_id_2, "velocity_b", rear_right_pwm)

        print(front_left_pwm, " ----- ", front_right_pwm);
        print(rear_right_pwm, " ----- ", rear_left_pwm);

        # Sleep to avoid spamming the serial connection
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")
finally:
    # Ensure robot resources are cleaned up
    robot.close()

