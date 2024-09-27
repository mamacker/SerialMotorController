import pygame

class GamepadClass:
    def __init__(self):
        # Initialize pygame's joystick support
        pygame.init()
        pygame.joystick.init()
        
        # Check if a gamepad is connected
        if pygame.joystick.get_count() == 0:
            raise ValueError("No gamepad detected.")
        
        # Assuming only one gamepad is connected
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
    
    def get_value(self, name_of_input):
        pygame.event.pump()  # Process internal event queue
        
        input_map = {
            # Joysticks axes
            "joystick_left_x": self.joystick.get_axis(0),
            "joystick_left_y": self.joystick.get_axis(1),
            "joystick_right_x": self.joystick.get_axis(4),
            "joystick_right_y": self.joystick.get_axis(3),
            
            # Buttons
            "button_a": self.joystick.get_button(0),
            "button_b": self.joystick.get_button(1),
            "button_x": self.joystick.get_button(2),
            "button_y": self.joystick.get_button(3),
            "l_bumper": self.joystick.get_button(4),
            "r_bumper": self.joystick.get_button(5),
            "l_stick": self.joystick.get_button(9),
            "r_stick": self.joystick.get_button(10),
            "button_back": self.joystick.get_button(6),
            "button_start": self.joystick.get_button(7),
            "button_xbox": self.joystick.get_button(8),
            
            # Triggers (treated as axes in some controllers)
            "l_trigger": self.joystick.get_axis(2),
            "r_trigger": self.joystick.get_axis(5),
            
            # D-pad
            "dpad_up": self.joystick.get_hat(0)[1] == 1,
            "dpad_down": self.joystick.get_hat(0)[1] == -1,
            "dpad_left": self.joystick.get_hat(0)[0] == -1,
            "dpad_right": self.joystick.get_hat(0)[0] == 1,
        }
        
        if name_of_input not in input_map:
            raise ValueError(f"Invalid input name: {name_of_input}")
        
        return input_map[name_of_input]
    
# Example usage:
# gamepad = GamepadClass()
# print(gamepad.get_value("joystick_left_x"))
# print(gamepad.get_value("button_a"))

