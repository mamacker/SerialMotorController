import time
from Robot import RobotClass  # Import the Robot class from Robot.py
from Keyboard import KeyboardClass  # Import the Keyboard class from Keyboard.py

if __name__ == '__main__':
    try:
        robot = RobotClass()  # Create an instance of the Robot class
        robot.find_motor_controllers(serial_only=False);
        Keyboard = KeyboardClass();
        controller_1 = "DT255GKCYS.local"
        robot.set_value(controller_1, 'invert_veloctiy_a', 1)
        robot.set_value(controller_1, 'invert_velocity_b', 0)
        controller_2 = "LUPNORMQDC.local"
        robot.set_value(controller_2, 'invert_velocity_a', 0)
        robot.set_value(controller_2, 'invert_veolcity_b', 1)
        c1_a = 0
        c1_b = 0
        c2_a = 0
        c2_b = 0
        keyPressed = False
        while(True):
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

