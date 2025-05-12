from PyQt5.QtCore import Qt

class Input:
    def __init__(self):
        print("creating input handler")
        self.quit = False
        self.key_queue = []
        self.key_pressed_list = []
        self.key_held_list = []
        self.key_released_list = []
        self.mouse_buttons = []

    def key_press_event(self, event):
        """Handle key press events."""
        key = event.key()
        if key not in self.key_pressed_list:
            self.key_pressed_list.append(key)
            self.key_queue.append(key)

        if key == Qt.Key_Escape:
            self.quit = True

    def key_release_event(self, event):
        """Handle key release events."""
        key = event.key()
        if key in self.key_pressed_list:
            self.key_pressed_list.remove(key)
            self.key_released_list.append(key)

    def mouse_press_event(self, event):
        """Handle mouse button press events."""
        button = event.button()
        if button not in self.mouse_buttons:
            self.mouse_buttons.append(button)

    def mouse_release_event(self, event):
        """Handle mouse button release events."""
        button = event.button()
        if button in self.mouse_buttons:
            self.mouse_buttons.remove(button)

    def is_key_pressed(self, key):
        """Check if a key is currently pressed."""
        return key in self.key_pressed_list

    def is_key_held(self, key):
        """Check if a key is being held down."""
        return key in self.key_held_list

    def is_key_released(self, key):
        """Check if a key was just released."""
        return key in self.key_released_list