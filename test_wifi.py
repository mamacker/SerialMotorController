import time
import os
from Robot import RobotClass  # Import the Robot class from Robot.py
from Keyboard import KeyboardClass  # Import the Keyboard class from Keyboard.py

CONFIG_FILE = "motor_controllers.txt"

def save_motor_controllers(controller_1, controller_2):
    with open(CONFIG_FILE, 'w') as file:
        file.write(f"{controller_1}\n")
        file.write(f"{controller_2}\n")

def load_motor_controllers():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            controllers = file.read().splitlines()
            if len(controllers) == 2:
                return controllers
    return None

if __name__ == '__main__':
    try:
        robot = RobotClass()  # Create an instance of the Robot class
        robot.find_motor_controllers(serial_only=False)  # Find motor controllers

        # Get the list of motor controller names
        motor_controllers = list(robot.controllers.keys())

        # Display the list of found motor controllers
        print("Found motor controllers:")
        for i, controller in enumerate(motor_controllers):
            print(f"{i + 1}: {controller}")
        print(f"{len(motor_controllers) + 1}: Same as before")

        # Ask the user to pick two motor controllers
        choice = int(input("Enter the number of the first motor controller: ")) - 1

        if choice == len(motor_controllers):
            controllers = load_motor_controllers()
            if controllers:
                controller_1, controller_2 = controllers
            else:
                print("No previous controllers found. Please select new controllers.")
                index_1 = int(input("Enter the number of the first motor controller: ")) - 1
                index_2 = int(input("Enter the number of the second motor controller: ")) - 1
                controller_1 = motor_controllers[index_1]
                controller_2 = motor_controllers[index_2]
                save_motor_controllers(controller_1, controller_2)
        else:
            index_1 = choice
            index_2 = int(input("Enter the number of the second motor controller: ")) - 1
            controller_1 = motor_controllers[index_1]
            controller_2 = motor_controllers[index_2]
            save_motor_controllers(controller_1, controller_2)

        # Example usage of the motor controllers
        robot.set_value(controller_1, 'invert_velocity_a', 1)
        robot.set_value(controller_1, 'invert_velocity_b', 0)
        robot.set_value(controller_2, 'invert_velocity_a', 0)
        robot.set_value(controller_2, 'invert_velocity_b', 1)

        c1_a = 0
        c1_b = 0
        c2_a = 0
        c2_b = 0
        keyPressed = False

        Keyboard = KeyboardClass()

        while True:
            keyPressed = False
            if Keyboard.get_value('w'):
                keyPressed = True
                c1_a = 1
                c1_b = 1
                c2_a = -1
                c2_b = -1
            elif Keyboard.get_value('s'):
                keyPressed = True
                c1_a = -1
                c1_b = -1
                c2_a = 1
                c2_b = 1

            if Keyboard.get_value('a'):
                if keyPressed:
                    c1_a = (1 * .5) + c1_a
                    c1_b = (-1 * .5) + c1_b
                    c2_a = (1 * .5) + c2_a
                    c2_b = (-1 * .5) + c2_b
                else:
                    c1_a = 1
                    c1_b = -1
                    c2_a = 1
                    c2_b = -1

                keyPressed = True
            elif Keyboard.get_value('d'):
                if keyPressed:
                    c1_a = (-1 * .5) + c1_a
                    c1_b = (1 * .5) + c1_b
                    c2_a = (-1 * .5) + c2_a
                    c2_b = (1 * .5) + c2_b
                else:
                    c1_a = -1
                    c1_b = 1
                    c2_a = -1
                    c2_b = 1
                keyPressed = True

            if keyPressed:
                robot.set_value(controller_1, 'velocity_a', c1_a)
                robot.set_value(controller_1, 'velocity_b', c1_b)
                robot.set_value(controller_2, 'velocity_a', c2_a)
                robot.set_value(controller_2, 'velocity_b', c2_b)
            else:
                robot.set_value(controller_1, 'velocity_b', 0)
                robot.set_value(controller_1, 'velocity_a', 0)
                robot.set_value(controller_2, 'velocity_b', 0)
                robot.set_value(controller_2, 'velocity_a', 0)

    except KeyboardInterrupt:
        print("Exercise interrupted")
    finally:
        robot.close()  # Ensure all serial connections are closed

