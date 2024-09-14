import serial
import time

# Open a serial connection (adjust 'COM3' for Windows or '/dev/ttyUSB0' for Linux/macOS)
ser = serial.Serial('/dev/ttyACM0', 460800, timeout=1)

def send_command(command):
    ser.write((command + '\n').encode())  # Send the command to the ESP32
    time.sleep(0.1)  # Give the ESP32 some time to process
    response = ser.readline().decode('utf-8').strip()  # Read the response from the ESP32
    print(response)

def motor_exercise():
    # Test MOTOR_A with various commands
    send_command('MOTOR_A FORWARD 50')
    time.sleep(2)  # Let the motor run for 2 seconds
    send_command('MOTOR_A REVERSE 30')
    time.sleep(2)
    send_command('MOTOR_A BRAKE')
    time.sleep(2)
    send_command('MOTOR_A STANDBY')
    time.sleep(2)

    # Test MOTOR_B with various commands
    send_command('MOTOR_B FORWARD 70')
    time.sleep(2)
    send_command('MOTOR_B REVERSE 40')
    time.sleep(2)
    send_command('MOTOR_B BRAKE')
    time.sleep(2)
    send_command('MOTOR_B STANDBY')
    time.sleep(2)

    # Optional: Loop through a sequence of commands
    for i in range(1, 101, 10):
        pwm_value = str(i)
        send_command(f'MOTOR_A FORWARD {pwm_value}')
        time.sleep(1)
        send_command(f'MOTOR_A REVERSE {pwm_value}')
        time.sleep(1)
        send_command('MOTOR_A BRAKE')
        time.sleep(2)
        send_command('MOTOR_B BRAKE')
        time.sleep(2)

if __name__ == '__main__':
    try:
        motor_exercise()
    except KeyboardInterrupt:
        print("Exercise interrupted")
    finally:
        ser.close()  # Close the serial connection when done

