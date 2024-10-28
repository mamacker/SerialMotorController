import time
from Robot import RobotClass  # Import the Robot class from Robot.py

def motor_exercise(robot, controller):
    # Test MOTOR_A with various commands
    robot.set_value(controller, 'velocity_a', 1)  # Forward
    robot.set_value(controller, 'velocity_b', 1)  # Forward
    time.sleep(2)
    robot.set_value(controller, 'velocity_a', -1)  # Reverse
    robot.set_value(controller, 'velocity_b', -1)  # Reverse
    time.sleep(2)
    robot.set_value(controller, 'velocity_a', 0)  # Brake
    robot.set_value(controller, 'velocity_b', 0)  # Brake
    time.sleep(2)

if __name__ == '__main__':
    try:
        while True:
            robot = RobotClass()  # Create an instance of the Robot class
            robot.find_motor_controllers();
            # Now you can set values for controllers that were automatically found
            for controller_id in robot.controllers:
                print(f"Setting values for {controller_id}")
                robot.set_value(controller_id, "invert_velocity_a", 1)
                robot.set_value(controller_id, "invert_velocity_b", 1)
                motor_exercise(robot, controller_id);

    except KeyboardInterrupt:
        print("Exercise interrupted")
    finally:
        robot.close()  # Ensure all serial connections are closed


