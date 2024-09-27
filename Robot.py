import serial
import time
import serial.tools.list_ports

class MotorController:
    def __init__(self, serial_port, baudrate=460800, timeout=1, name=None):
        self.name = name or serial_port  # Assign a name or default to the serial port
        self.ser = serial.Serial(serial_port, baudrate, timeout=timeout)
        self.ser.flush()
        # Inversion flags for motors A and B
        self.invert_motor_a = False
        self.invert_motor_b = False
        self.last_command_a = None
        self.last_command_b = None

    def send_command(self, command):
        """Sends a command to the motor controller via serial."""
        print(f"[{self.name}] Sending command: {command.strip()}")
        self.ser.write(command.encode('utf-8'))

    def set_value(self, motor, action, pwm_value=None):
        """Builds and sends a motor command string with inversion handling."""
        if motor == "MOTOR_A" and self.invert_motor_a:
            # Invert actions for MOTOR_A if the invert flag is set
            if action == "FORWARD":
                action = "REVERSE"
            elif action == "REVERSE":
                action = "FORWARD"
        elif motor == "MOTOR_B" and self.invert_motor_b:
            # Invert actions for MOTOR_B if the invert flag is set
            if action == "FORWARD":
                action = "REVERSE"
            elif action == "REVERSE":
                action = "FORWARD"

        # Send the command
        if pwm_value is not None:
            command = f"{motor} {action} {pwm_value}\n"
        else:
            command = f"{motor} {action}\n"
        
        if ( motor == "MOTOR_A" ):
            if ( self.last_command_a == command ):
                return
            self.last_command_a = command
        else:
            if ( self.last_command_b == command ):
                return
            self.last_command_b = command 
        self.send_command(command)

    def set_invert(self, motor, invert):
        """Sets the inversion flag for the specified motor."""
        if motor == "MOTOR_A" or motor == "velocity_a":
            self.invert_motor_a = invert
            print(f"[{self.name}] Invert MOTOR_A set to {invert}")
        elif motor == "MOTOR_B" or motor == "velocity_b":
            self.invert_motor_b = invert
            print(f"[{self.name}] Invert MOTOR_B set to {invert}")

    def close(self):
        """Closes the serial connection."""
        self.ser.close()

class RobotClass:
    def __init__(self):
        self.controllers = {}

    def find_motor_controllers(self, baudrate=460800, timeout=.2):
        """
        Scans all available serial ports and checks if a motor controller is connected.
        If a valid motor controller is found, it stores the controller and its name.
        """
        available_ports = list(serial.tools.list_ports.comports())
        for port in available_ports:
            try:
                print(f"Checking port {port.device}...")
                ser = serial.Serial(port.device, baudrate, timeout=timeout, write_timeout=timeout)
                ser.flush()

                # Send a GET_NAME command to check if it's a motor controller
                ser.write(b"GET_NAME\n")
                time.sleep(0.1)  # Allow time for the controller to respond

                if ser.in_waiting > 0:
                    response = ser.readline().decode('utf-8').strip()
                    if "Board Name:" in response:
                        # Extract the name from the response
                        name = response.split(":")[-1].strip()
                        print(f"Motor controller found on {port.device}, name: {name}")
                        ser.close()
                        # Store the controller
                        self.add_motor_controller(name, port.device, baudrate, timeout)
                ser.close()
            except Exception as e:
                print(f"Error checking port {port.device}: {e}")

    def add_motor_controller(self, controller_id, serial_port, baudrate=460800, timeout=1, name=None):
        """
        Adds a new motor controller to the robot.

        Parameters:
        - controller_id: Unique ID for the motor controller.
        - serial_port: Serial port for the controller.
        - baudrate: Baudrate for the serial connection (default is 460800).
        - timeout: Timeout for the serial connection (default is 1 second).
        - name: Optional name to give the motor controller (default is serial port).
        """
        self.controllers[controller_id] = MotorController(serial_port, baudrate, timeout, name)

    def set_value(self, controller_id, property_name, value):
        """
        Sets the value for the motor identified by the property_name.
        This sends a command to the appropriate motor controller.
        """
        if controller_id not in self.controllers:
            print(f"Controller with ID {controller_id} not found.")
            return

        motor_controller = self.controllers[controller_id]
        motor = None
        action = None
        pwm_value = None
        
        # Handle inversion settings
        if "invert_" in property_name:
            motor = property_name.split("_")[1] + "_" + property_name.split("_")[2]
            motor_controller.set_invert(motor, bool(value))
            print("Inverted ", motor, " ", value)
            return

        # Parse the property name and determine the motor and action
        if "velocity_a" in property_name:
            motor = "MOTOR_A"
        elif "velocity_b" in property_name:
            motor = "MOTOR_B"
    
        # Interpret the velocity values to actions and PWM values
        if motor:
            if value > 0:
                action = "FORWARD"
                pwm_value = int(self.map_pwm(abs(value)))
            elif value < 0:
                action = "REVERSE"
                pwm_value = int(self.map_pwm(abs(value)))
            else:
                action = "BRAKE"
    
            # Send the command via the motor controller
            motor_controller.set_value(motor, action, pwm_value)
    
        else:
            print(f"Invalid motor property: {property_name}")

    def map_pwm(self, value, min_pwm=1, max_pwm=100):
        """
        Maps the velocity values from the range of -1 to 1 to PWM values (1 to 255).
        """
        return value * 100

    def close(self):
        """Closes all motor controllers' serial connections."""
        for controller in self.controllers.values():
            controller.close()

    def sleep(self, duration):
        time.sleep(duration)

# Example usage:
if __name__ == '__main__':
    robot = RobotClass()
    
    # Find motor controllers automatically
    robot.find_motor_controllers()

    try:
        # Now you can set values for controllers that were automatically found
        for controller_id in robot.controllers:
            print(f"Setting values for {controller_id}")
            robot.set_value(controller_id, "velocity_a", 50)  # MOTOR_A forward with 50% power
            time.sleep(2)
            robot.set_value(controller_id, "velocity_b", -30)  # MOTOR_B reverse with 30% power
            robot.set_value(controller_id, "invert_velocity_a", 1)  # Invert MOTOR_A direction
            robot.set_value(controller_id, "velocity_a", 50)  # MOTOR_A now reversed

    except KeyboardInterrupt:
        print("Exercise interrupted")
    finally:
        robot.close()  # Ensure all serial connections are closed


