from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout
from kivy.core.window import Window  # Import Window class
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, IMAGE_SOURCE  # Import settings
print(f"Loaded settings: WINDOW_WIDTH={WINDOW_WIDTH}, WINDOW_HEIGHT={WINDOW_HEIGHT}, IMAGE_SOURCE={IMAGE_SOURCE}")  # Debugging output



class LoadImageApp(App):  
    def build(self):
        layout = FloatLayout()  # Use FloatLayout for flexible positioning
        container = FloatLayout()  # Create a container layout
        background_image = Image(source=IMAGE_SOURCE, allow_stretch=True, keep_ratio=True)  # Set image as background

        container.add_widget(background_image)  # Add image to the container
        layout.add_widget(container)  # Add container to the main layout

        background_image.size_hint = (1, 1)  # Set size hint to fill the layout


        print(f"Loading image from: {IMAGE_SOURCE}")  # Debugging output
        layout.add_widget(background_image)  # Add background image to layout

    def build(self):
        self.window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)  # Set initial window size from settings
        Window.size = self.window_size  # Set the window size
        Window.bind(size=self.on_window_resize)  # Bind the resize event
    def on_window_resize(self, window, size):
        # Handle window resizing if needed
        pass

if __name__ == '__main__':
    LoadImageApp().run()
