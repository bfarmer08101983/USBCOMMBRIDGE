from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import logging  # Import logging

IMAGE_SOURCE = "5845e1997733c3558233c0f0-2552579276.png"  # Define the image source

class SettingsScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        logging.info("SettingsScreen initialized")  # Log when the settings screen is created

        self.orientation = 'vertical'

        # Set a background color for the settings screen
        with self.canvas.after:  # Change to 'after' to ensure the settings screen is on top
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add a label for the settings screen
        self.add_widget(Label(text="Settings Screen", size_hint_y=None, height=40, color=(0, 0, 1, 1)))  # Blue text
        self.add_widget(Label(text="This is the settings area.", size_hint_y=None, height=40, color=(0, 0, 1, 1)))  # Blue text

        # Example input fields for settings
        self.add_widget(Label(text="Setting 1:", color=(1, 1, 1, 1)))  # White text
        self.setting1_input = TextInput(multiline=False)
        self.add_widget(self.setting1_input)

        self.add_widget(Label(text="Setting 2:", color=(1, 1, 1, 1)))  # White text
        self.setting2_input = TextInput(multiline=False)
        self.add_widget(self.setting2_input)

        # Add buttons for saving and canceling
        save_button = Button(text="Save", size_hint_y=None, height=40)
        save_button.bind(on_press=self.save_settings)
        self.add_widget(save_button)

        cancel_button = Button(text="Cancel", size_hint_y=None, height=40)
        cancel_button.bind(on_press=self.cancel_settings)
        self.add_widget(cancel_button)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def save_settings(self, instance):
        # Logic to save settings goes here
        print("Settings saved!")  # Placeholder for actual save logic
        # Navigate back to the main screen (to be implemented)

    def cancel_settings(self, instance):
        # Logic to cancel changes and navigate back to the main screen
        print("Settings changes canceled!")  # Placeholder for actual cancel logic
        # Navigate back to the main screen (to be implemented)
