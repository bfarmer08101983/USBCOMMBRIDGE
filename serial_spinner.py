from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import logging
import os

class SerialSpinnerApp(App):
    selected_value = StringProperty("Select an option")

    def build(self):
        # Initialize BoxLayout for main layout
        main_layout = BoxLayout(orientation='vertical')  
        
        main_layout.width = 800  # Initialize width
        main_layout.height = 600  # Initialize height

        with main_layout.canvas.before:
            Color(1, 1, 1, 1)  # White background color
            self.background_loader = Rectangle(pos=(0, 0), size=(main_layout.width, main_layout.height))  # Dynamic white rectangle

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Create a header label to display the current selection
        self.header_label = Label(
            text="Current Selection: None",
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)  # White text color
        )
        with self.header_label.canvas.before:
            Color(0.2, 0.2, 0.8, 1)  # Dark blue background color
            self.header_background = Rectangle(pos=self.header_label.pos)  # Removed size attribute

        self.header_label.bind(size=self.update_header_background, pos=self.update_header_background)
        main_layout.add_widget(self.header_label)  # Add header to the main layout

        # Initialize BoxLayout for spinner layout
        layout = BoxLayout(orientation='horizontal')

        # Define the Settings spinner
        settings_spinner = Spinner(
            text="Settings",
            values=(
                'Settings',
                'Load Settings',
                'Save Settings',
                'Clear Settings',
                'Change Background',
            ),
            size_hint=(None, None),
            text_size=(100, None),
            halign='center',  # Center the text
            valign='middle'   # Center the text vertically
        )
        settings_spinner.bind(text=self.on_settings_spinner_select)
        settings_spinner.size_hint = (None, None)  # Set size hint for the spinner
        settings_spinner.size = (150, 40)  # Set a fixed size for the spinner
        layout.add_widget(settings_spinner)  # Add Settings spinner to the layout

        # Define the Serial Protocols spinner
        self.serial_spinner = Spinner(
            text="Serial Protocols",
            values=(
                'FINS',
                'Modbus RTU',
                'CANOpen',
                'Text/ASCII',
                'I2C',
                'SPI',
                'RS232',
                'RS485',
                'TTL',
                'CTRL CMD',
            ),
            size_hint=(None, None),
            text_size=(150, None),
            halign='center',  # Center the text
            valign='middle'   # Center the text vertically
        )
        self.serial_spinner.bind(text=self.on_serial_spinner_select)
        self.serial_spinner.size_hint = (None, None)  # Set size hint for the spinner
        self.serial_spinner.size = (150, 40)  # Set a fixed size for the spinner
        layout.add_widget(self.serial_spinner)  # Add Serial Protocols spinner to the layout

        # Define the TCP Protocols spinner
        self.tcp_spinner = Spinner(
            text="TCP Protocols",
            values=(
                'FINS/TCP',
                'Ethernet/IP',
                'Modbus TCP',
                'TCP',
            ),
            size_hint=(None, None),
            text_size=(150, None),
            halign='center',  # Center the text
            valign='middle'   # Center the text vertically
        )
        self.tcp_spinner.bind(text=self.on_tcp_spinner_select)
        self.tcp_spinner.size_hint = (None, None)  # Set size hint for the spinner
        self.tcp_spinner.size = (150, 40)  # Set a fixed size for the spinner
        layout.add_widget(self.tcp_spinner)  # Add TCP Protocols spinner to the layout

        # Define the UDP Protocols spinner
        self.udp_spinner = Spinner(
            text="UDP Protocols",
            values=(
                'FINS/UDP',
                'Modbus UDP',
                'UDP',
            ),
            size_hint=(None, None),
            text_size=(150, None),
            halign='center',  # Center the text
            valign='middle'   # Center the text vertically
        )
        self.udp_spinner.bind(text=self.on_udp_spinner_select)
        self.udp_spinner.size_hint = (None, None)  # Set size hint for the spinner
        self.udp_spinner.size = (150, 40)  # Set a fixed size for the spinner
        layout.add_widget(self.udp_spinner)  # Add UDP Protocols spinner to the layout

        main_layout.add_widget(layout)  # Add the horizontal spinner layout to the main layout

        return main_layout

    def update_header_background(self, instance, value):
        self.header_background.pos = instance.pos
        self.header_background.size = instance.size

    def on_settings_spinner_select(self, spinner, text):
        if text == 'Load Settings':
            self.load_settings()
        elif text == 'Save Settings':
            self.save_settings()
        elif text == 'Clear Settings':
            self.clear_settings()
        elif text == 'Change Background':
            self.change_background()
        logging.info(f'Selected Settings option: {text}')

    def load_settings(self):
        filechooser = FileChooserIconView()
        filechooser.filters = ['*.json', '*.ini', '*.txt']
        popup = Popup(title="Load Settings", content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=self.on_file_selected)
        popup.open()

    def on_file_selected(self, filechooser, selection, touch):
        if selection:
            logging.info(f'Loading settings from: {selection[0]}')

    def save_settings(self):
        logging.info('Saving settings...')

    def clear_settings(self):
        logging.info('Clearing settings...')

    def change_background(self):
        filechooser = FileChooserIconView()
        filechooser.filters = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
        popup = Popup(title="Select Background Image", content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=self.on_image_selected)
        popup.open()

    def on_image_selected(self, filechooser, selection, touch):
        if selection:
            image_path = selection[0]
            logging.info(f'Changing background to image: {image_path}')
            with self.root.canvas.before:
                Color(1, 1, 1, 1)  # Set background color to white
            self.background_loader.canvas.clear()  # Clear previous background
            self.background_loader = Rectangle(source=image_path, pos=(0, 0), size=self.root.size)  # Update background with selected image



    def on_image_selected(self, filechooser, selection, touch):
        if selection:
            image_path = selection[0]
            logging.info(f'Changing background to image: {image_path}')

    def on_serial_spinner_select(self, spinner, text):
        if hasattr(self, 'last_serial_selection'):
            self.last_serial_selection.background_color = (1, 1, 1, 1)  # Reset previous selection
        spinner.background_color = (1, 0.5, 0, 1)  # Highlight selected option
        self.last_serial_selection = spinner
        self.update_header_text(text)  # Update header with the selected option

        logging.info(f'Selected Serial Protocol option: {text}')

    def on_tcp_spinner_select(self, spinner, text):
        if hasattr(self, 'last_tcp_selection'):
            self.last_tcp_selection.background_color = (1, 1, 1, 1)  # Reset previous selection
        spinner.background_color = (1, 0.5, 0, 1)  # Highlight selected option
        self.last_tcp_selection = spinner
        self.update_header_text(text)  # Update header with the selected option

        logging.info(f'Selected TCP Protocol option: {text}')

    def on_udp_spinner_select(self, spinner, text):
        if hasattr(self, 'last_udp_selection'):
            self.last_udp_selection.background_color = (1, 1, 1, 1)  # Reset previous selection
        spinner.background_color = (1, 0.5, 0, 1)  # Highlight selected option
        self.last_udp_selection = spinner
        self.update_header_text(text)  # Update header with the selected option

        logging.info(f'Selected UDP Protocol option: {text}')

    def update_header_text(self, text):
        self.header_label.text = f"Current Selection: {text}"  # Update header with the selected option

if __name__ == '__main__':
    try:
        SerialSpinnerApp().run()
    except Exception as e:
        logging.error(f'An error occurred: {e}')
