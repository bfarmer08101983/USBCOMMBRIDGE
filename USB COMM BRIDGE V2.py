import logging
from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import json

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class USBCommBridgeApp(App):
    selected_value = StringProperty("Select an option")
    submenu = None  # Initialize submenu variable

    def build(self):
        # Initialize BoxLayout for main layout
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.content_area = BoxLayout(orientation='vertical', size_hint=(1, 0.8), padding=10, spacing=10)

        main_layout.add_widget(self.content_area)

        # Initialize BoxLayout for spinner layout
        layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        main_layout.add_widget(layout)

        # Define the Menu spinner
        menu_spinner = Spinner(
            text="Menu",
            values=(
                'Kivy Settings',
                'App Settings',
                'Comm Settings',
                'Exit App',
            ),
            size_hint=(0.2, None),
            height=40
        )
        menu_spinner.bind(text=self.on_menu_select)
        layout.add_widget(menu_spinner)

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
        self.serial_spinner.bind(text=self.on_serial_spinner_select)
        layout.add_widget(self.serial_spinner)

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
        self.tcp_spinner.bind(text=self.on_tcp_spinner_select)
        layout.add_widget(self.tcp_spinner)

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
        self.udp_spinner.bind(text=self.on_udp_spinner_select)
        layout.add_widget(self.udp_spinner)

        # Define the OBD-II spinner
        self.obdii_spinner = Spinner(
            text="OBD-II Protocols",
            values=(
                'OBD-II',
                'CAN',
                'ISO 9141',
                'KWP2000',
            ),
            size_hint=(0.2, None),
            height=40
        )
        self.obdii_spinner.bind(text=self.on_obdii_spinner_select)
        layout.add_widget(self.obdii_spinner)

        # Define the Smart Home spinner
        self.smart_home_spinner = Spinner(
            text="Smart Home Protocols",
            values=(
                'Z-Wave',
                'ZigBee',
                'Wi-Fi',
                'Bluetooth Low Energy (BLE)',
                'Ethernet',
                'Thread',
                'Matter',
            ),
            size_hint=(0.2, None),
            height=40
        )
        self.smart_home_spinner.bind(text=self.on_smart_home_spinner_select)
        layout.add_widget(self.smart_home_spinner)

        # Set the window size
        Window.size = (800, 600)

        return main_layout

    def on_menu_select(self, spinner, text):  # Handle menu selection
        # Do not change the main spinner's text
        logging.info(f'Menu option selected: {text}')

    def open_kivy_settings(self, instance):
        popup = Popup(title='USB COMM BRIDGE V2', content=Label(text='Kivy settings go here'), size_hint=(0.8, 0.8))
        popup.open()

    def open_app_settings(self, instance):
        try:
            with open('settings.py', 'r') as f:
                settings = json.load(f)
                content = Label(text=json.dumps(settings, indent=4))
                popup = Popup(title='App Settings', content=content, size_hint=(0.8, 0.8))
                popup.open()
        except Exception as e:
            logging.error(f"Error loading settings: {e}")

    def open_comm_settings(self, instance):
        popup_content = BoxLayout(orientation='vertical')
        ip_input = TextInput(hint_text='IP Address')
        subnet_input = TextInput(hint_text='Subnet Mask')
        save_button = Button(text='Save Settings')
        
        popup_content.add_widget(Label(text='Comm Settings'))
        popup_content.add_widget(ip_input)
        popup_content.add_widget(subnet_input)
        popup_content.add_widget(save_button)

        popup = Popup(title='Comm Settings', content=popup_content, size_hint=(0.8, 0.8))
        popup.open()

    def on_serial_spinner_select(self, spinner, text):  # Handle serial spinner selection
        logging.info(f'Serial protocol changed to: {text}')
        self.update_content_area(text)

    def on_tcp_spinner_select(self, spinner, text):  # Handle TCP spinner selection
        logging.info(f'TCP protocol changed to: {text}')

    def on_udp_spinner_select(self, spinner, text):  # Handle UDP spinner selection
        logging.info(f'UDP protocol changed to: {text}')

    def on_obdii_spinner_select(self, spinner, text):  # Handle OBD-II spinner selection
        logging.info(f'OBD-II protocol changed to: {text}')

    def on_smart_home_spinner_select(self, spinner, text):  # Handle Smart Home spinner selection
        logging.info(f'Smart Home protocol changed to: {text}')

    def update_content_area(self, text):
        if self.content_area.children:
            self.content_area.clear_widgets()
        if self.submenu:
            self.content_area.remove_widget(self.submenu)
        if not self.submenu:
            self.submenu = BoxLayout(orientation='vertical')
        self.submenu.add_widget(Label(text=f"You selected: {text}"))
        protocol_settings_button = Button(text="Protocol Settings")
        protocol_settings_button.bind(on_press=self.open_protocol_settings)
        self.submenu.add_widget(protocol_settings_button)
        self.content_area.add_widget(self.submenu)

    def open_protocol_settings(self, instance):  # Open protocol-specific settings
        popup = Popup(title='Protocol Settings', content=Label(text='Settings for the selected protocol go here'), size_hint=(0.8, 0.8))
        popup.open()

    def connect(self, instance):  # Handle connect button press
        selected_protocol = self.serial_spinner.text
        logging.info(f"Connect button pressed for protocol: {selected_protocol}")

    def disconnect(self, instance):  # Handle disconnect button press
        logging.info("Disconnect button pressed.")

if __name__ == '__main__':
    USBCommBridgeApp().run()
