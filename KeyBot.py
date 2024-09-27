import time
from Robot import RobotClass  # Import the Robot class from Robot.py
from Keyboard import KeyboardClass  # Import the Keyboard class from Keyboard.py

def motor_exercise(robot, controller):
    # Test MOTOR_A with various commands
    robot.set_value(controller, 'velocity_a', 1)  # Forward
    time.sleep(2)
    robot.set_value(controller, 'velocity_a', -1)  # Reverse
    time.sleep(2)
    robot.set_value(controller, 'velocity_a', 0)  # Brake
    time.sleep(2)
    
    # Standby isn't handled in the class, assuming it is the same as brake for now
    robot.set_value(controller, 'velocity_a', 0)
    time.sleep(2)

    # Test MOTOR_B with various commands
    robot.set_value(controller, 'velocity_b', 1)  # Forward
    time.sleep(5)
    robot.set_value(controller, 'velocity_b', -1)  # Reverse
    time.sleep(5)
    robot.set_value(controller, 'velocity_b', 0)  # Brake
    time.sleep(2)

    # Optional: Loop through a sequence of commands
    for i in range(-1, 1, 10):
        pwm_value = i / 100.0  # Assuming velocity is from -1 to 1
        robot.set_value(controller, 'velocity_a', pwm_value)
        time.sleep(5)
        robot.set_value(controller, 'velocity_a', -pwm_value)
        time.sleep(5)
        robot.set_value(controller, 'velocity_a', 0)  # Brake
        time.sleep(2)
        robot.set_value(controller, 'velocity_b', 0)  # Brake
        time.sleep(2)

if __name__ == '__main__':
    robot = RobotClass()  # Create an instance of the Robot class
    Keyboard = KeyboardClass()
    robot.find_motor_controllers();
    try:
        controller_id = list(robot.controllers.keys())[0]
        while(True):
            if Keyboard.get_value('w'):
                robot.set_value(controller_id, 'velocity_a', 1)
                robot.set_value(controller_id, 'velocity_b', 1)
            elif Keyboard.get_value('s'):
                robot.set_value(controller_id, 'velocity_a', -1)
                robot.set_value(controller_id, 'velocity_b', -1)
            elif Keyboard.get_value('a'):
                robot.set_value(controller_id, 'velocity_b', 1)
                robot.set_value(controller_id, 'velocity_a', -1)
            elif Keyboard.get_value('d'):
                robot.set_value(controller_id, 'velocity_b', -1)
                robot.set_value(controller_id, 'velocity_a', 1)
            else:
                robot.set_value(controller_id, 'velocity_b', 0)
                robot.set_value(controller_id, 'velocity_a', 0)

    except KeyboardInterrupt:
        print("Exercise interrupted")
    finally:
        robot.close()  # Ensure all serial connections are closed

