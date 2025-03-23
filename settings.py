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
        with self.canvas.before:  # Change to 'before' to ensure the settings screen is on top
            Color(0.9, 0.9, 0.9, 1)  # Light gray background

            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add a label for the settings screen
        self.add_widget(Label(text="Settings", size_hint_y=None, height=40, color=(0, 0, 0, 1)))  # Black text

        self.add_widget(Label(text="This is the settings area.", size_hint_y=None, height=40, color=(0, 0, 1, 1)))  # Blue text

        # Input fields for advanced IP settings
        self.add_widget(Label(text="IP Address:", color=(1, 1, 1, 1)))  # White text
        self.ip_input = TextInput(multiline=False)
        self.add_widget(self.ip_input)

        self.add_widget(Label(text="Gateway:", color=(1, 1, 1, 1)))  # White text
        self.gateway_input = TextInput(multiline=False)
        self.add_widget(self.gateway_input)

        self.add_widget(Label(text="Subnet:", color=(1, 1, 1, 1)))  # White text
        self.subnet_input = TextInput(multiline=False)
        self.add_widget(self.subnet_input)

        self.add_widget(Label(text="Station:", color=(1, 1, 1, 1)))  # White text
        self.station_input = TextInput(multiline=False)
        self.add_widget(self.station_input)

        self.add_widget(Label(text="Timeout:", color=(1, 1, 1, 1)))  # White text
        self.timeout_input = TextInput(multiline=False)
        self.add_widget(self.timeout_input)

        self.add_widget(Label(text="Retries:", color=(1, 1, 1, 1)))  # White text
        self.retries_input = TextInput(multiline=False)
        self.add_widget(self.retries_input)

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
        ip_value = self.ip_input.text  # Get the value from ip_input
        gateway_value = self.gateway_input.text  # Get the value from gateway_input
        subnet_value = self.subnet_input.text  # Get the value from subnet_input
        station_value = self.station_input.text  # Get the value from station_input
        timeout_value = self.timeout_input.text  # Get the value from timeout_input
        retries_value = self.retries_input.text  # Get the value from retries_input
        print(f"Settings saved: IP = {ip_value}, Gateway = {gateway_value}, Subnet = {subnet_value}, Station = {station_value}, Timeout = {timeout_value}, Retries = {retries_value}")  # Placeholder for actual save logic

        # Navigate back to the main screen (to be implemented)

    def cancel_settings(self, instance):
        # Logic to cancel changes and navigate back to the main screen
        print("Settings changes canceled!")  # Placeholder for actual cancel logic
        # Close the settings screen (to be implemented)

        # Navigate back to the main screen (to be implemented)
