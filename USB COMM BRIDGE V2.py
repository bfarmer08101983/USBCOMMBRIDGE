import logging
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import json

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoadSpecificImageApp(App):
    selected_value = StringProperty("Select an option")
    submenu = None  # Initialize submenu variable

    def build(self): 
        # Initialize BoxLayout for main layout
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))  # Use relative sizing for main layout
        
        # Load image source from settings
        image_source = "5845e1997733c3558233c0f0-2552579276.png"  # Placeholder for image source
        self.background_image = Image(source=image_source, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})  # Center the image
        self.background_image.bind(size=self.update_image_size)  # Bind image size to window size

        main_layout.add_widget(self.background_image)  # Add background image to layout

        self.content_area = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=10, spacing=10)  # Create content area with relative height and spacing

        main_layout.add_widget(self.content_area)  # Add content area to the main layout
        
        # Initialize BoxLayout for spinner layout
        layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)  # Center spinners

        main_layout.add_widget(layout)  # Add the horizontal spinner layout to the main layout

        # Define the Settings spinner
        settings_spinner = Spinner(
            text="Settings",
            values=(
                'Load Settings',
                'Save Settings',
                'Clear Settings',
                'Change Background',
                'Comm Settings',
            ),
            size_hint=(0.2, None),
            height=40
        )
        settings_spinner.bind(text=self.on_settings_spinner_select)  # Bind the settings spinner selection
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
            size_hint=(0.2, None),
            height=40
        )
        self.serial_spinner.bind(text=self.on_serial_spinner_select)  # Bind the serial spinner selection
        layout.add_widget(self.serial_spinner)  # Add Serial Protocols spinner to the layout

        # Define the ODB-II spinner
        self.odb_spinner = Spinner(
            text="ODB-II",
            values=(
                'USB Connection',
                'Bluetooth Connection',
            ),
            size_hint=(0.2, None),
            height=40
        )
        self.odb_spinner.bind(text=self.on_odb_spinner_select)  # Bind the ODB-II spinner selection
        layout.add_widget(self.odb_spinner)  # Add ODB-II spinner to the layout

        # Define the TCP Protocols spinner
        self.tcp_spinner = Spinner(
            text="TCP Protocols",
            values=(
                'FINS/TCP',
                'Ethernet/IP',
                'Modbus TCP',
                'TCP',
            ),
            size_hint=(0.2, None),
            height=40
        )
        self.tcp_spinner.bind(text=self.on_tcp_spinner_select)  # Bind the TCP spinner selection
        layout.add_widget(self.tcp_spinner)  # Add TCP Protocols spinner to the layout

        # Define the UDP Protocols spinner
        self.udp_spinner = Spinner(
            text="UDP Protocols",
            values=(
                'FINS/UDP',
                'Modbus UDP',
                'UDP',
            ),
            size_hint=(0.2, None),
            height=40
        )
        self.udp_spinner.bind(text=self.on_udp_spinner_select)  # Bind the UDP spinner selection
        layout.add_widget(self.udp_spinner)  # Add UDP Protocols spinner to the layout

        # Set the window size
        Window.size = (800, 600)  # Set a fixed window size
        Window.bind(size=self.on_window_size)  # Bind the window size change event
        self.on_window_size(Window, Window.size)  # Call the method to set initial size

        return main_layout  # Return the layout with the background image

    def on_window_size(self, window, size):  # Define the window size change method
        self.background_image.size = size  # Update the image size to match the window size
        self.background_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Center the image

    def update_image_size(self, instance, value):  # Define the method to update image size
        instance.size = (Window.width, Window.height)  # Update image size to match window size

    def on_settings_spinner_select(self, spinner, text): 
        if text == "Load Settings":
            self.load_settings()  # Load settings from the settings.py file
        elif text == "Save Settings":
            self.save_settings()  # Save current settings to the settings.py file
        elif text == "Clear Settings":
            self.clear_settings()  # Clear user-typed settings

    def load_settings(self):
        try:
            with open('settings.py', 'r') as f:
                settings = json.load(f)
                # Load settings into the application
                logging.info("Settings loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading settings: {e}")

    def save_settings(self):
        settings = {
            'baud_rate': self.baud_rate_input.text,
            'port': self.port_input.text,
            # Add other settings as needed
        }
        try:
            with open('settings.py', 'w') as f:
                json.dump(settings, f)
                logging.info("Settings saved successfully.")
        except Exception as e:
            logging.error(f"Error saving settings: {e}")

    def clear_settings(self):
        self.baud_rate_input.text = ''
        self.port_input.text = ''
        logging.info("Settings cleared.")

    def on_serial_spinner_select(self, spinner, text):  # Handle serial spinner selection
        self.header_label.text = f"Current Selection: {text}"  # Update header with selected option
        # Clear previous content
        if self.content_area.children:
            self.content_area.clear_widgets()  
        if self.submenu:
            self.content_area.remove_widget(self.submenu)  # Remove previous submenu if it exists
        # Create a new submenu layout only if it doesn't exist
        if not self.submenu:
            self.submenu = BoxLayout(orientation='vertical')  

        self.submenu.add_widget(Label(text=f"You selected: {text}"))  # Update content area
        connect_button = Button(text="Connect")
        connect_button.bind(on_press=self.connect)  # Bind connect function
        self.submenu.add_widget(connect_button)  # Add Connect button
        disconnect_button = Button(text="Disconnect")
        disconnect_button.bind(on_press=self.disconnect)  # Bind disconnect function
        self.submenu.add_widget(disconnect_button)  # Add Disconnect button
        settings_button = Button(text="Settings")
        settings_button.bind(on_press=self.open_settings)  # Bind open settings function
        self.submenu.add_widget(settings_button)  # Add Settings button
        self.content_area.add_widget(self.submenu)  # Add the submenu to the content area

        # Log the change in serial protocol selection
        logging.info(f'Serial protocol changed to: {text}')  

    def connect(self, instance):  # Handle connect button press
        selected_protocol = self.serial_spinner.text  # Get the selected protocol from the spinner
        logging.info(f"Connect button pressed for protocol: {selected_protocol}")  # Log the action

    def disconnect(self, instance):  # Handle disconnect button press
        logging.info("Disconnect button pressed.")

    def on_odb_spinner_select(self, spinner, text):  # Handle ODB-II spinner selection
        self.header_label.text = f"Current ODB-II Selection: {text}"  # Update header with selected option

    def on_tcp_spinner_select(self, spinner, text):  # Handle TCP spinner selection
        self.header_label.text = f"Current TCP Selection: {text}"  # Update header with selected option

    def on_udp_spinner_select(self, spinner, text):  # Handle UDP spinner selection
        self.header_label.text = f"Current UDP Selection: {text}"  # Update header with selected option

if __name__ == '__main__':
    LoadSpecificImageApp().run()
