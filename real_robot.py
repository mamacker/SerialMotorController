import time
import threading


#circumstancial variables 
sideOfField = "right" #CHANGE THIS BASED ON THE SIDE OF THE FIELD


#motor speed
motorSpeed = 0.25

#drive train motor offsets
motor1 = .975
motor2 = .8725
motor3 = 1.15
motor4 = 1.25

#lift and grabber motor speeds
liftSpeed = 0.5
grabSpeed = 0.3
ARM_SPEED = 0.05 # Change this


# Device IDs
#MOTOR_SET_RIGHT =  "6_7578923042333793965" #this is the correct one
MOTOR_SET_RIGHT =  "HWMDBDDVUD" #this is the correct one
#MOTOR_SET_LEFT = "6_10834027977028241909"  #"6_18352129111267124789"
MOTOR_SET_LEFT = "AXTDAORLJE"  #"6_18352129111267124789"

MOTOR_SET_UPANDDOWN = "6_4526500323366717588" #up and down

LIMIT_SWITCH = "1_1039209217629971042"

#6_9594834332290411397

#6_8680115587439011471

ARM_MOTOR_ID = "6_2"
LINE_FOLLOWER_ID = "2_3"


# Motors
LEFT_MTR = "b"
RIGHT_MTR = "a"
ARM_MTR = "b"


# Keyboard Controls (change these to your preferences)
LEFT = "a"
RIGHT = "d"
FORWARD = "w"
BACKWARD = "s"
turnRight = "e"
turnLeft = "q"

turnLeft90 = ","
turnRight90 = "."
turn180 = "/"

grabbingLiftUp = "u"
grabbingLiftDown = "i"

grabbingOpen = "["
grabbingClose = "]"


drivingBufferTime = 0.1 #


# Arm positions
# (NOT TESTED! You need to find positions that work based on your arm and your reference encoder value)
ARM_DOWN_POS = 25
ARM_UP_POS = 75


# Motor Inversions (need to specify / change depending on your control scheme)
LEFT_MTR_INVERT = False
RIGHT_MTR_INVERT = True


# Teleop variables
invert = 0
slow = True
motor1Speed = motor2Speed = motor3Speed = motor4Speed = 0










#Autonomous
def autonomous_setup():
  Robot.set_value(MOTOR_SET_LEFT, "pid_enabled_" + LEFT_MTR, False)
  Robot.set_value(MOTOR_SET_RIGHT, "pid_enabled_" + LEFT_MTR, False)
  Robot.set_value(MOTOR_SET_LEFT, "pid_enabled_" + RIGHT_MTR, False)
  Robot.set_value(MOTOR_SET_RIGHT, "pid_enabled_" + RIGHT_MTR, False)
  Robot.set_value(MOTOR_SET_UPANDDOWN, "pid_enabled_" + LEFT_MTR, False)
  Robot.set_value(MOTOR_SET_UPANDDOWN, "pid_enabled_" + RIGHT_MTR, False)
  print("Autonomous setup complete")
  Robot.run(autonomous_actions)
  # Set motor inversions
  #Robot.set_value(MOTOR_SET_RIGHT, "invert_" + LEFT_MTR, LEFT_MTR_INVERT)
  #Robot.set_value(MOTOR_SET2, "invert_" + LEFT_MTR, LEFT_MTR_INVERT)

#autonomous variables
#autonimousTurnLeft = 0.1
autonimousTurnRight = 0.23
autonimousForward = 1
autonimousAdjust2 = 0.45
autonimousRotate = 0.2
rightAutonomousTurnRight = 1.5

def autonomous_main():
    pass


done = False

def autonomous_actions():
  # Autonomous code can go here (or, if more complex,
  # put in separate function and Robot.run() in autonomous_setup() )
  global done
  global left
  left = True
  if done == False:
      #turn right
      #set_motors_with_time(motorSpeed, motorSpeed, -motorSpeed, -motorSpeed, autonimousTurn)
      #time.sleep(autonimousTurn)
      #going forward, need to iron it out
      #set_motors_with_time(motorSpeed, motorSpeed, motorSpeed, motorSpeed, autonimousForward)
      #time.sleep(autonimousForward)
      print ()
      tempMotorSpeed = motorSpeed +.1
      if(left):
          print("what the heck")
          set_motors_with_time(-tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, 0.07)
          Robot.sleep(0.07)
          set_motors_with_time(tempMotorSpeed, tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, autonimousTurnRight)
          Robot.sleep(autonimousTurnRight)
          set_motors_with_time(-tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, autonimousForward)
          Robot.sleep(autonimousForward)
      
      else :
          print(left)
          set_motors_with_time(-tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, 0.3)
          Robot.sleep(0.3)
          set_motors_with_time(tempMotorSpeed, tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, rightAutonomousTurnRight)
          Robot.sleep(autonimousTurnRight)
          set_motors_with_time(-tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, -tempMotorSpeed, autonimousForward)
          Robot.sleep(autonimousForward)
      done = True










#teleop
def teleop_setup():
  print("teleop is working")
  Robot.set_value(MOTOR_SET_LEFT, "pid_enabled_" + LEFT_MTR, False)
  Robot.set_value(MOTOR_SET_RIGHT, "pid_enabled_" + LEFT_MTR, False)
  Robot.set_value(MOTOR_SET_LEFT, "pid_enabled_" + RIGHT_MTR, False)
  Robot.set_value(MOTOR_SET_RIGHT, "pid_enabled_" + RIGHT_MTR, False)
  Robot.set_value(MOTOR_SET_UPANDDOWN, "pid_enabled_" + LEFT_MTR, False)
  Robot.set_value(MOTOR_SET_UPANDDOWN, "pid_enabled_" + RIGHT_MTR, False)

  #Robot.set_value(MOTOR_SET_LEFT, "invert_" + LEFT_MTR, LEFT_MTR_INVERT)
  #Robot.set_value(MOTOR_SET_RIGHT, "invert_" + LEFT_MTR, LEFT_MTR_INVERT)
  #Robot.set_value(MOTOR_SET_ARM, "invert_" + LEFT_MTR, LEFT_MTR_INVERT)
  pass

motorThing = 0.2
def teleop_main():
  global motorThing
  global motorSpeed
  global invert
  global grabSpeed
  global slow
  global motor1Speed, motor2Speed, motor3Speed, motor4Speed
  
  #toggle speed
  if Gamepad.get_value("button_x"):
     motorSpeed = 0.25
  if Gamepad.get_value("button_b"):
     motorSpeed = 0.15
  
  #invert buttons
  if Gamepad.get_value("l_stick"):
      invert = 0
  if Gamepad.get_value("r_stick"):
      invert = 2
  if Gamepad.get_value("button_xbox"):
      print("I am working")
      invert = 1

  # Keyboard Drive code
  if Keyboard.get_value(LEFT) or Keyboard.get_value("left_arrow"):
      #print("left")
      set_motors_with_time(-motorSpeed, motorSpeed, -motorSpeed, motorSpeed, drivingBufferTime)
  if Keyboard.get_value(RIGHT) or Keyboard.get_value("right_arrow"):
      #print("right")
      set_motors_with_time(motorSpeed, -motorSpeed, motorSpeed, -motorSpeed, drivingBufferTime)
  if Keyboard.get_value(FORWARD) or Keyboard.get_value("up_arrow"):
      #print("forward")
      set_motors_with_time(motorSpeed, motorSpeed, motorSpeed, motorSpeed, drivingBufferTime)
  if Keyboard.get_value(BACKWARD) or Keyboard.get_value("down_arrow"):
      #print("backward")
      set_motors_with_time(-motorSpeed, -motorSpeed, -motorSpeed, -motorSpeed, drivingBufferTime)
  if Keyboard.get_value(turnRight):
      #print("turning right")
      set_motors_with_time(motorSpeed, motorSpeed, -motorSpeed, -motorSpeed, drivingBufferTime)
  if Keyboard.get_value(turnLeft):
      #print("turning left")
      set_motors_with_time(-motorSpeed, -motorSpeed, motorSpeed, motorSpeed, drivingBufferTime)
  if Keyboard.get_value(grabbingLiftUp) or Keyboard.get_value("r") or Gamepad.get_value("button_y"):
      #print("lifting up")
      set_lift_with_time(liftSpeed, 0.1)
  if Keyboard.get_value(grabbingLiftDown) or Keyboard.get_value("f") or Gamepad.get_value("button_a"):
      #print("going down")
      set_lift_with_time(-liftSpeed, 0.1)
  if Keyboard.get_value(grabbingClose) or Gamepad.get_value("l_trigger"):
      #print("closing")
      set_grab_with_time(-grabSpeed, 0.1)
  if Keyboard.get_value(grabbingOpen) or Gamepad.get_value("r_trigger"):
      #print("opening")
      set_grab_with_time(grabSpeed, 0.1)
  

  #Gamepad drive code   
  if Gamepad.get_value("dpad_right"):
      if invert == 0:
        motor1Speed += motorSpeed
        motor2Speed += motorSpeed
        motor3Speed += motorSpeed
        motor4Speed += motorSpeed
      elif invert == 1:
        motor1Speed += motorSpeed
        motor2Speed -= motorSpeed
        motor3Speed += motorSpeed
        motor4Speed -= motorSpeed
      else:
        motor1Speed -= motorSpeed
        motor2Speed -= motorSpeed
        motor3Speed -= motorSpeed
        motor4Speed -= motorSpeed
    
  if Gamepad.get_value("dpad_left"):
      if invert == 0:
        motor1Speed -= motorSpeed
        motor2Speed -= motorSpeed
        motor3Speed -= motorSpeed
        motor4Speed -= motorSpeed
      elif invert == 1:
        motor1Speed -= motorSpeed
        motor2Speed += motorSpeed
        motor3Speed -= motorSpeed
        motor4Speed += motorSpeed
      else:
        motor1Speed += motorSpeed
        motor2Speed += motorSpeed
        motor3Speed += motorSpeed
        motor4Speed += motorSpeed 
        
  if Gamepad.get_value("dpad_up"):
      if invert == 0:
        motor1Speed += motorSpeed
        motor2Speed -= motorSpeed
        motor3Speed += motorSpeed
        motor4Speed -= motorSpeed
      elif invert == 1:
        motor1Speed -= motorSpeed
        motor2Speed -= motorSpeed
        motor3Speed -= motorSpeed
        motor4Speed -= motorSpeed
      else:
        motor1Speed -= motorSpeed
        motor2Speed += motorSpeed
        motor3Speed -= motorSpeed
        motor4Speed += motorSpeed
   
  if Gamepad.get_value("dpad_down"):
      if invert == 0:
        motor1Speed -= motorSpeed
        motor2Speed += motorSpeed
        motor3Speed -= motorSpeed
        motor4Speed += motorSpeed
      elif invert == 1:
        motor1Speed += motorSpeed
        motor2Speed += motorSpeed
        motor3Speed += motorSpeed
        motor4Speed += motorSpeed
      else:
        motor1Speed += motorSpeed
        motor2Speed -= motorSpeed
        motor3Speed += motorSpeed
        motor4Speed -= motorSpeed


  
  #joystick control
  if Gamepad.get_value("joystick_left_y") != 0 or Gamepad.get_value("joystick_left_x") != 0:
      #print("left stick")
      if invert == 0:
        y = -Gamepad.get_value("joystick_left_x")
        x = Gamepad.get_value("joystick_left_y")
        motor1Speed += (y * -motorSpeed) + (x * -motorSpeed)
        motor2Speed += (y * -motorSpeed) + (x * motorSpeed)
        motor3Speed += (y * -motorSpeed) + (x * -motorSpeed)
        motor4Speed += (y * -motorSpeed) + (x * motorSpeed)
      elif invert == 2:
        x = -Gamepad.get_value("joystick_left_y")
        y = Gamepad.get_value("joystick_left_x")
        motor1Speed += (y * -motorSpeed) + (x * -motorSpeed)
        motor2Speed += (y * -motorSpeed) + (x * motorSpeed)
        motor3Speed += (y * -motorSpeed) + (x * -motorSpeed)
        motor4Speed += (y * -motorSpeed) + (x * motorSpeed)
 
  #turn left
  if Gamepad.get_value("l_bumper"):
    motor1Speed -= motorSpeed
    motor2Speed -= motorSpeed
    motor3Speed += motorSpeed
    motor4Speed += motorSpeed
 
  #turn right
  if Gamepad.get_value("r_bumper"):
    motor1Speed += motorSpeed
    motor2Speed += motorSpeed
    motor3Speed -= motorSpeed
    motor4Speed -= motorSpeed
  
  #set motor speeds
  motor1Speed *= motor1
  motor2Speed *= motor2
  motor3Speed *= motor3
  motor4Speed *= motor4
  
  set_motors_with_time(motor1Speed, motor2Speed, motor3Speed, motor4Speed, drivingBufferTime)
 
  motor1Speed = 0
  motor2Speed = 0
  motor3Speed = 0
  motor4Speed = 0
  Robot.sleep(0.08)



#Arm and claw
def arm_code():
  arm_target_pos = ARM_DOWN_POS
  while True:
      # Get the current target position of the arm
      if Keyboard.get_value(ARM_DOWN):
          arm_target_pos = ARM_DOWN_POS
      elif Keyboard.get_value(ARM_UP):
          arm_target_pos = ARM_UP_POS

      # Drive the arm motor to go to the target position USING ENCODERS (think hard about how you can use this to your advantage!)
      # Ask PiE staff what these do and refer to the student API!
      current_pos = Robot.get_value(ARM_MOTOR_ID, "enc_" + ARM_MTR) # Retrieves current position of the arm motor

      # Sets motor going in the correct direction based on whether the arm is on one side or the other side of the target position
      if current_pos < arm_target_pos:
          Robot.set_value(ARM_MOTOR_ID, "velocity_" + ARM_MTR, ARM_SPEED)
      elif current_pos > arm_target_pos:
          Robot.set_value(ARM_MOTOR_ID, "velocity_" + ARM_MTR, ARM_SPEED * -1.0)
      else:
          Robot.set_value(ARM_MOTOR_ID, "velocity_" + ARM_MTR, 0.0)


#Utility functions
timeouts = {}

def hello():
  print("hello")

def set_timeout(duration, callback, name = None):
  try:
      if (name in timeouts): #Checks if the name is in the timeout array
          timeouts[name].cancel() #
          del timeouts[name]
      t = threading.Timer(duration, callback)
      t.start()
      timeouts[name] = t
      return t
  except Exception as e:
      print(e)



#sets motor speed to parameters with time
def set_motors_with_time(left_front = 0, left_back = 0, right_front = 0, right_back = 0, duration=1):
  set_motors(left_front, left_back, right_front, right_back)
  set_timeout(duration, clear_motors, "motorsgo")


#sets motor speeds
motors_stopped = True
def set_motors(left_front = 0, left_back = 0, right_front = 0, right_back = 0):
  global motors_stopped
  Robot.set_value(MOTOR_SET_LEFT, "velocity_" + RIGHT_MTR, left_front*motor1)
  Robot.set_value(MOTOR_SET_LEFT, "velocity_" + LEFT_MTR, left_back*motor2)
  Robot.set_value(MOTOR_SET_RIGHT, "velocity_" + RIGHT_MTR, right_front*motor3)
  Robot.set_value(MOTOR_SET_RIGHT, "velocity_" + LEFT_MTR, right_back*motor4)
  # Update motors stopped variable.
  if (left_front != 0 or left_back != 0 or right_front != 0 or right_back != 0):
      if (motors_stopped):
          #print("motors started")
          motors_stopped = False


arm_motors_stopped = True
def set_lift_with_time(lift = 0, duration=1):
  global arm_motors_stopped
  Robot.set_value(MOTOR_SET_UPANDDOWN, "velocity_" + RIGHT_MTR, lift)
  #Robot.set_value(MOTOR_SET_hekkinBroke, "velocity_" + LEFT_MTR, lift)
  set_timeout(duration, clear_lift_motors, "liftgo")


def set_grab_with_time(lift = 0, duration=1):
  global arm_motors_stopped
  #Robot.set_value(MOTOR_SET_hekkinBroke, "velocity_" + RIGHT_MTR, lift)
  Robot.set_value(MOTOR_SET_UPANDDOWN, "velocity_" + LEFT_MTR, lift)
  set_timeout(duration, clear_grab_motors, "grabgo")


def clear_motors():
  global motors_stopped
  #if (not motors_stopped):
  #print("all motors stopped")
  motors_stopped = True
  Robot.set_value(MOTOR_SET_LEFT, "velocity_" + LEFT_MTR, 0)
  Robot.set_value(MOTOR_SET_LEFT, "velocity_" + RIGHT_MTR, 0)
  Robot.set_value(MOTOR_SET_RIGHT, "velocity_" + LEFT_MTR, 0)
  Robot.set_value(MOTOR_SET_RIGHT, "velocity_" + RIGHT_MTR, 0)


def clear_lift_motors():
  Robot.set_value(MOTOR_SET_UPANDDOWN, "velocity_" + RIGHT_MTR, 0)
  #Robot.set_value(MOTOR_SET_hekkinBroke, "velocity_" + LEFT_MTR, 0)


def clear_grab_motors():
  #Robot.set_value(MOTOR_SET_hekkinBroke, "velocity_" + RIGHT_MTR, 0)
  Robot.set_value(MOTOR_SET_UPANDDOWN, "velocity_" + LEFT_MTR, 0)


set_timeout(.1, hello, "hello")


from Robot import RobotClass  # Assuming Robot.py is in the same directory
from Gamepad import GamepadClass  # Assuming Gamepad.py is in the same directory
from Keyboard import KeyboardClass  # Assuming Gamepad.py is in the same directory
if __name__ == '__main__':
    Robot = RobotClass()
    Robot.find_motor_controllers()
    Gamepad = GamepadClass()
    Keyboard = KeyboardClass()
    teleop_setup()
try:
    while True:
        teleop_main();
except KeyboardInterrupt:
    print("Exiting...");
    Robot.close()
