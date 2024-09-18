from pynput import keyboard

class KeyboardClass:
    def __init__(self):
        self.keys_pressed = set()

        # Start listener for key presses and releases
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            if isinstance(key, keyboard.Key):
                # Handle special keys like arrows
                key_name = self._translate_special_key(key)
            else:
                key_name = key.char
            self.keys_pressed.add(key_name)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if isinstance(key, keyboard.Key):
                key_name = self._translate_special_key(key)
            else:
                key_name = key.char
            if key_name in self.keys_pressed:
                self.keys_pressed.remove(key_name)
        except AttributeError:
            pass

    def get_value(self, name_of_key):
        return name_of_key in self.keys_pressed

    def _translate_special_key(self, key):
        special_keys = {
            keyboard.Key.left: 'left_arrow',
            keyboard.Key.right: 'right_arrow',
            keyboard.Key.up: 'up_arrow',
            keyboard.Key.down: 'down_arrow'
        }
        return special_keys.get(key, None)

# Example usage:
if __name__ == "__main__":
    kb = Keyboard()

    print("Press keys on the keyboard. Use Ctrl+C to exit.")
    try:
        while True:
            print("Left Arrow:", kb.get_value("left_arrow"))
            print("Right Arrow:", kb.get_value("right_arrow"))
            print("a:", kb.get_value("a"))
            print("1:", kb.get_value("1"))
    except KeyboardInterrupt:
        print("Exiting.")

