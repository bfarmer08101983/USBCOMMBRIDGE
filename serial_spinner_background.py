from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
import logging

class BackgroundLoader(BoxLayout):
    def __init__(self, background_image, **kwargs):
        super().__init__(**kwargs)
        self.default_background_image = background_image
        self.background = Rectangle(source=self.default_background_image, pos=(0, 0), size=(1, 1))  # Placeholder size

        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background color
            self.canvas.add(self.background)

    def update_background_size(self, width, height):
        if width > 0 and height > 0:  # Check for valid dimensions
            self.background.size = (width, height)  # Update background size
            logging.info(f'Updated background size to: {self.background.size}')  # Log the updated size
