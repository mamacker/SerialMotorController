import time
from Gamepad import GamepadClass  # Import the Gamepad class from Gamepad.py

def watch_gamepad():
    gamepad = GamepadClass()

    while True:
        try:
            # Watch and print relevant gamepad inputs
            print("Left joystick (x, y):", gamepad.get_value("joystick_left_x"), gamepad.get_value("joystick_left_y"))
            print("Right joystick (x, y):", gamepad.get_value("joystick_right_x"), gamepad.get_value("joystick_right_y"))
            print("A button pressed:", gamepad.get_value("button_a"))
            print("Left trigger:", gamepad.get_value("l_trigger"))
            print("Right trigger:", gamepad.get_value("r_trigger"))
            print("D-pad up pressed:", gamepad.get_value("dpad_up"))
            print("D-pad right pressed:", gamepad.get_value("dpad_right"))
            print("---------------------")
            
            # Sleep to prevent too many outputs
            time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("Gamepad monitoring stopped.")
            break

# Run the watch function
if __name__ == "__main__":
    watch_gamepad()

