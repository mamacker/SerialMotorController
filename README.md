
# Robot Motor Controller Library

This library is the first step in creating a small robot using an API similar to the one used by Pioneers at Berkeley.

## Getting Started

### 1. Install Dependencies
Make sure you have the following installed:

- **Python 3**
- **Pygame**
- **PySerial**
- **Pynput**

You can install the required Python packages using pip:

```bash
pip install pygame pyserial pynput
```

### 2. Determine the COM Port

1. Open **Device Manager** by right-clicking on the Windows Start menu and selecting **Device Manager**.
2. In Device Manager, expand the **Ports (COM & LPT)** section.
3. Look for a device labeled **USB Serial Device**. Note the COM port number (e.g., COM3).

This is the COM port you’ll need to use in your code.

### 3. Test Simple Communications

1. Open `test.py` in your code editor.
2. Replace the COM port (or `/dev/tty***` on Linux/Mac) with the appropriate COM port for your device.
3. Save `test.py`.
4. Run the test script to verify communication with the motor controller:

   ```bash
   python3 ./test.py
   ```

If everything is set up correctly, you should see messages coming back from the motor controller.

## Communicating with Motor Controllers

Each motor controller has a unique name. You can find out the name by sending the following serial command:

```
GET_NAME
```

This will return a string that identifies the motor controller, like: `TLAWIEESYT`.

### 4. Update the Code with Motor Controller Names

Make sure to enter these names in the code wherever necessary to identify and control each motor controller correctly.
