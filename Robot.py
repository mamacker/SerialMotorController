import socket
import subprocess
import serial.tools.list_ports
import time
import platform
import select

class MotorController:
    def __init__(self, connection, baudrate=460800, timeout=1, name=None):
        self.name = name or connection
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = connection
        self.is_serial = isinstance(connection, str) and (connection.startswith('/dev/') or connection.startswith('COM'))
        self.is_tcp = isinstance(connection, str) and ':' in connection
        # Inversion flags for motors A and B
        self.invert_motor_a = False
        self.invert_motor_b = False
        self.last_command_a = None
        self.last_command_b = None

        if self.is_serial:
            self.ser = serial.Serial(connection, baudrate, timeout=timeout, write_timeout=timeout)
            self.ser.flush()
        elif self.is_tcp:
            address, port = connection.split(':')
            self._connect_tcp()

    def _connect_tcp(self):
        """Helper method to establish a TCP connection."""
        address, port = self.connection.split(':')
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.settimeout(self.timeout)
        self.tcp_socket.connect((address, int(port)))

    def send_command(self, command):
        print(f"[{self.name}] Sending command: {command.strip()}")

        if self.is_serial:
            self.ser.write(command.encode('utf-8'))
            return self.ser.readline().decode('utf-8').strip()
        elif self.is_tcp:
            try:
                ready_to_write = select.select([], [self.tcp_socket], [], self.timeout)
                if ready_to_write[1]:
                    self.tcp_socket.sendall(command.encode('utf-8'))
                    ready_to_read = select.select([self.tcp_socket], [], [], self.timeout)
                    if ready_to_read[0]:
                        return self.tcp_socket.recv(1024).decode('utf-8').strip()
                    else:
                        return "No response received within timeout"
                else:
                    return "Socket not ready for writing within timeout"
            except (socket.error, socket.timeout) as e:
                print(f"Connection error: {e}. Attempting to reconnect...")
                self._connect_tcp()
                return self.send_command(command)

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

        #Check to see if this command should actually be sent
        #This is to prevent sending the same command multiple times 
        if ( motor == "MOTOR_A" ):
            if ( self.last_command_a == command ):
                return
            self.last_command_a = command
        else:
            if ( self.last_command_b == command ):
                return
            self.last_command_b = command 
        send_res = self.send_command(command)
        print(f"[{self.name}] Response: {send_res}")

    def set_invert(self, motor, invert):
        """Sets the inversion flag for the specified motor."""
        if motor == "MOTOR_A" or motor == "velocity_a":
            self.invert_motor_a = invert
            print(f"[{self.name}] Invert MOTOR_A set to {invert}")
        elif motor == "MOTOR_B" or motor == "velocity_b":
            self.invert_motor_b = invert
            print(f"[{self.name}] Invert MOTOR_B set to {invert}")

    def close(self):
        if self.is_serial:
            self.ser.close()
        elif self.is_tcp:
            self.tcp_socket.close()

class RobotClass:
    def __init__(self):
        self.controllers = {}

    def find_motor_controllers(self, baudrate=460800, timeout=.2, serial_only=True):
        """
        Scans all available serial ports and network for motor controllers.
        If a valid motor controller is found, it stores the controller and its name.
        """
        # Scan serial ports
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

        # Scan network using avahi-browse or dns-sd
        if not serial_only:
            try:
                if platform.system() == 'Windows':
                    result = subprocess.run(['dns-sd', '-B', '_motor._tcp'], capture_output=True, text=True, timeout=5)
                else:
                    result = subprocess.run(['timeout', '15', 'avahi-browse', '-r', '_motor._tcp'], capture_output=True, text=True)
                
                print(result.stdout)
                lines = result.stdout.split('\n')
                print("---------------------------------")
                print(lines)
                print("---------------------------------")
                service_name, address, port = None, None, None
                for line in lines:
                    print(line)
                    if 'hostname' in line:
                        service_name = line.split('=')[-1].strip().strip('[]')
                    elif 'address' in line:
                        address = line.split('=')[-1].strip().strip('[]')
                    elif 'port' in line:
                        port = line.split('=')[-1].strip().strip('[]')
                        if service_name and address and port:
                            print(f"Motor controller found on {address}:{port}, name: {service_name}")
                            self.add_motor_controller(service_name, f"{address}:{port}", baudrate, 15)
                            service_name, address, port = None, None, None
            except subprocess.TimeoutExpired:
                return
            except Exception as e:
                print(f"Error scanning network for motor controllers: {e}")

    def add_motor_controller(self, controller_id, connection, baudrate=460800, timeout=1, name=None):
        """
        Adds a new motor controller to the robot.

        Parameters:
        - controller_id: Unique ID for the motor controller.
        - connection: Serial port or TCP address for the controller.
        - baudrate: Baudrate for the serial connection (default is 460800).
        - timeout: Timeout for the connection (default is 1 second).
        - name: Optional name to give the motor controller (default is connection).
        """
        self.controllers[controller_id] = MotorController(connection, baudrate, timeout, name)
        print("Added motor controller:", controller_id, " controller ct: ", len(self.controllers))

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
        Maps the velocity values from the range of -1 to 1 to PWM values (1 to 100).
        """
        if (value > 1):
            value = 1
        elif (value < -1):
            value = -1

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
            robot.set_value(controller_id, "velocity_a", -1)  # MOTOR_A forward with 50% power
            time.sleep(2)
            robot.set_value(controller_id, "velocity_b", -1)  # MOTOR_B reverse with 30% power
            robot.set_value(controller_id, "invert_velocity_a", 1)  # Invert MOTOR_A direction
            robot.set_value(controller_id, "velocity_a", 1)  # MOTOR_A now reversed

    except KeyboardInterrupt:
        print("Exercise interrupted")
    finally:
        robot.close()  # Ensure all serial connections are closed



        # Now you can set values for controllers that were automatically found
        for controller_id in robot.controllers:
            print(f"Setting values for {controller_id}")