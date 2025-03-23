import logging
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from settings import IMAGE_SOURCE, SettingsScreen  # Import SettingsScreen from settings
from kivy.uix.label import Label
from kivy.uix.popup import Popup  # Import Popup for creating a new window
from kivy.uix.button import Button  # Import Button for actions
from kivy.graphics import Color, Rectangle

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoadSpecificImageApp(App):
    selected_value = StringProperty("Select an option")
    submenu = None  # Initialize submenu variable

    def build(self): 
        # Initialize BoxLayout for main layout
        main_layout = BoxLayout(orientation='vertical')  
        
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

        # Load image source from settings
        image_source = IMAGE_SOURCE  # Load image source from settings
        background_image = Image(source=image_source, allow_stretch=True, keep_ratio=True, size_hint=(None, None), size=(800, 600), pos_hint={'center_x': 0.5, 'center_y': 0.5})  # Center the image
        background_image.bind(size=self.update_image_size)  # Bind image size to window size
        main_layout.add_widget(background_image)  # Add background image to layout

        self.content_area = BoxLayout(orientation='vertical', size_hint=(1, 1))  # Create content area
        main_layout.add_widget(self.content_area)  # Add content area to the main layout
        
        # Initialize BoxLayout for spinner layout
        layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)  # Center spinners
        main_layout.add_widget(layout)  # Add the horizontal spinner layout to the main layout

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

        # Set the window size
        Window.size = (800, 600)  # Set a fixed window size
        return main_layout  # Return the layout with the background image

    def update_header_background(self, instance, value):
        self.header_background.pos = instance.pos
        self.header_background.size = instance.size

    def update_image_size(self, instance, value):
        instance.size = (Window.width, Window.height)  # Update image size to match window size

    def on_settings_spinner_select(self, spinner, text): 
        self.header_label.text = f"Current Selection: {text}"  # Update header with selected option
        self.content_area.clear_widgets()  # Clear previous content
        
        if text == "Settings":
            logging.info("Loading SettingsScreen")  # Log when loading the settings screen
            settings_screen = SettingsScreen()  # Create an instance of the settings screen
            popup = Popup(title="Settings", content=settings_screen, size_hint=(0.8, 0.8))  # Create a Popup for the settings screen
            popup.open()  # Open the popup

    def on_serial_spinner_select(self, spinner, text): 
        self.header_label.text = f"Current Selection: {text}"  # Update header with selected option
        self.content_area.clear_widgets()  # Clear previous content
        if self.submenu:
            self.content_area.remove_widget(self.submenu)  # Remove previous submenu if it exists
        self.submenu = BoxLayout(orientation='vertical')  # Create a new submenu layout
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


        logging.info(f'Serial protocol changed to: {text}')  # Log the change

    def connect(self, instance):
        # Logic to connect based on selected protocol
        print("Connecting...")  # Placeholder for actual connection logic

    def disconnect(self, instance):
        # Logic to disconnect based on selected protocol
        print("Disconnecting...")  # Placeholder for actual disconnection logic

    def open_settings(self, instance):
        logging.info("Opening SettingsScreen in a new window")  # Log when opening the settings screen
        settings_screen = SettingsScreen()  # Create an instance of the settings screen
        popup = Popup(title="Settings", content=settings_screen, size_hint=(0.8, 0.8))  # Create a Popup for the settings screen
        popup.open()  # Open the popup

    def on_tcp_spinner_select(self, spinner, text): 
        self.header_label.text = f"Current Selection: {text}"  # Update header with selected option
        self.content_area.clear_widgets()  # Clear previous content
        self.content_area.add_widget(Label(text=f"You selected: {text}"))  # Update content area
        self.content_area.add_widget(Label(text="Connect"))  # Add connect option
        self.content_area.add_widget(Label(text="Disconnect"))  # Add disconnect option
        self.content_area.add_widget(Label(text="Settings"))  # Add settings option
        self.content_area.add_widget(Label(text="Status"))  # Add status option
        logging.info(f'TCP protocol changed to: {text}')  # Log the change

    def on_udp_spinner_select(self, spinner, text): 
        self.header_label.text = f"Current Selection: {text}"  # Update header with selected option
        self.content_area.clear_widgets()  # Clear previous content
        self.content_area.add_widget(Label(text=f"You selected: {text}"))  # Update content area
        self.content_area.add_widget(Label(text="Connect"))  # Add connect option
        self.content_area.add_widget(Label(text="Disconnect"))  # Add disconnect option
        self.content_area.add_widget(Label(text="Settings"))  # Add settings option
        self.content_area.add_widget(Label(text="Status"))  # Add status option
        logging.info(f'UDP protocol changed to: {text}')  # Log the change

if __name__ == '__main__':
    LoadSpecificImageApp().run()
