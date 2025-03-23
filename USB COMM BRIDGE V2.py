import logging
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from settings import IMAGE_SOURCE, SettingsScreen  # Import SettingsScreen from settings
from kivy.uix.filechooser import FileChooserIconView  # Import FileChooser for selecting files

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
        self.background_image = Image(source=image_source, allow_stretch=True, keep_ratio=True, size_hint=(None, None), size=(800, 600), pos_hint={'center_x': 0.5, 'center_y': 0.5})  # Center the image

        self.background_image.bind(size=self.update_image_size)  # Bind image size to window size

        main_layout.add_widget(self.background_image)  # Add background image to layout


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

        # Define the ODB-II spinner
        self.odb_spinner = Spinner(
            text="ODB-II",
            values=(
                'USB Connection',
                'Bluetooth Connection',
            ),
            size_hint=(None, None),
            text_size=(150, None),
            halign='center',  # Center the text
            valign='middle'   # Center the text vertically
        )
        self.odb_spinner.bind(text=self.on_odb_spinner_select)
        self.odb_spinner.size_hint = (None, None)  # Set size hint for the spinner
        self.odb_spinner.size = (150, 40)  # Set a fixed size for the spinner
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
        
        if text == "Change Background":
            self.change_background()  # Call the method to change the background
        elif text == "Settings":

            logging.info("Loading SettingsScreen")  # Log when loading the settings screen
            settings_screen = SettingsScreen()  # Create an instance of the settings screen
            popup = Popup(title="Settings", content=settings_screen, size_hint=(0.8, 0.8))  # Create a Popup for the settings screen
            popup.open()  # Open the popup

    def change_background(self):
        filechooser = FileChooserIconView()  # Create a file chooser
        filechooser.bind(on_submit=self.load_background)  # Bind the submit event to load the background
        popup = Popup(title="Select Background Image", content=filechooser, size_hint=(0.9, 0.9))  # Create a popup for the file chooser
        popup.open()  # Open the popup

    def load_background(self, instance, selection, touch):
        if selection:  # Check if a file was selected
            image_source = selection[0]  # Get the selected file path
            self.background_image.source = image_source  # Update the background image source
            self.background_image.reload()  # Reload the image to display it
            logging.info(f"Background image changed to: {image_source}")  # Log the change


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

    def on_tcp_spinner_select(self, spinner, text): 
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

        logging.info(f'TCP protocol changed to: {text}')  # Log the change

    def on_udp_spinner_select(self, spinner, text): 
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

        logging.info(f'UDP protocol changed to: {text}')  # Log the change

    def on_odb_spinner_select(self, spinner, text):
        self.header_label.text = f"Current Selection: {text}"  # Update header with selected option
        self.content_area.clear_widgets()  # Clear previous content
        if self.submenu:
            self.content_area.remove_widget(self.submenu)  # Remove previous submenu if it exists
        self.submenu = BoxLayout(orientation='vertical')  # Create a new submenu layout
        self.submenu.add_widget(Label(text=f"You selected: {text}"))  # Update content area
        usb_button = Button(text="USB Connection")
        usb_button.bind(on_press=self.usb_connect)  # Bind USB connection function
        self.submenu.add_widget(usb_button)  # Add USB Connection button
        bluetooth_button = Button(text="Bluetooth Connection")
        bluetooth_button.bind(on_press=self.bluetooth_connect)  # Bind Bluetooth connection function
        self.submenu.add_widget(bluetooth_button)  # Add Bluetooth Connection button
        self.content_area.add_widget(self.submenu)  # Add the submenu to the content area

        logging.info(f'ODB-II protocol changed to: {text}')  # Log the change

    def usb_connect(self, instance):
        # Logic for USB connection
        print("USB Connection initiated...")  # Placeholder for actual USB connection logic

    def bluetooth_connect(self, instance):
        # Logic for Bluetooth connection
        print("Bluetooth Connection initiated...")  # Placeholder for actual Bluetooth connection logic

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

if __name__ == '__main__':
    LoadSpecificImageApp().run()
