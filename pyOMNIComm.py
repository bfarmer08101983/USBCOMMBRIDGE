import logging
__version__ = "1.0.0"  # Version tracking for the application

import minimalmodbus  # For Modbus RTU
import pymodbus  # For Modbus TCP/IP
import can  # For CANOpen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
import json
import platform  # For OS detection
import pigpio  # For I2C

# import spidev  # For SPI

import paho.mqtt.client as mqtt  # For MQTT
import obd  # Updated import for OBD-II communication

import aiocoap  # For CoAP
import websocket  # For WebSocket
#import pyLoRaWAN  # For LoRaWAN
import pyprofibus  # For PROFIBUS
import can  # For CAN communication
from fins.tcp import TCPFinsConnection  # Importing TCPFinsConnection from fins package

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmartHomeCommApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform.system() == "Linux":  # Check if running on Raspberry Pi
            import smbus2  # For I2C
            self.pi = pigpio.pi()  # Initialize pigpio
            self.i2c_bus = self.pi.i2c_open(1, 0x20)  # Open I2C bus 1 with address 0x20
        elif platform.system() == "Windows":  # Check if running on Windows
            logging.warning("I2C communication is not supported on Windows. Use a compatible library or method.")
            self.i2c_bus = None  # Placeholder for Windows
        else:
            logging.error("Unsupported OS for I2C communication.")

    def build(self):
        self.title = "Smart Home Communication App"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Protocol selection spinner
        self.protocol_spinner = Spinner(
            text="Select Protocol",
            values=(
                'FINS',  # Custom implementation
                'Modbus RTU',  # minimalmodbus
                'CANOpen',  # canopen
                'Text/ASCII',  # Custom implementation
                'I2C',  # smbus2
                'SPI',  # spidev
                'RS232',  # pyserial
                'RS485',  # pyserial
                'TTL',  # Custom implementation
                'CTRL CMD',  # Custom implementation
                'MQTT',  # paho-mqtt
                'CoAP',  # aiocoap
                'HTTP',  # Custom implementation
                'WebSocket',  # websocket-client
                'Zigbee',  # Custom implementation
                'Z-Wave',  # pyZWave
                'LoRaWAN',  # pyLoRa
                'Modbus TCP/IP',  # pymodbus
                'EtherNet/IP',  # pycomm3
                'PROFIBUS',  # pyprofibus
                'CAN',  # python-can
                'DeviceNet',  # Custom implementation
                'JTAG',  # pyJTAG
                'OBD-II',  # python-OBD
                'ISO 9141',  # Removed pyISO9141
                'KWP2000',  # openobd
                'ZigBee',  # Custom implementation
                'Wi-Fi',  # Custom implementation
                'Bluetooth Low Energy (BLE)',  # bluepy
                'Ethernet',  # Custom implementation
                'Thread',  # Custom implementation
                'Matter'  # Custom implementation
            ),
            size_hint=(0.2, None),
            height=40
        )
        layout.add_widget(self.protocol_spinner)

        connect_button = Button(text="Connect", size_hint=(0.2, None), height=50)
        connect_button.bind(on_press=self.show_connection_settings)  # Show settings on connect
        layout.add_widget(connect_button)

        disconnect_button = Button(text="Disconnect", size_hint=(0.2, None), height=50)
        disconnect_button.bind(on_press=self.disconnect)
        layout.add_widget(disconnect_button)

        # Load settings button
        load_settings_button = Button(text="Load Settings", size_hint=(0.2, None), height=50)
        load_settings_button.bind(on_press=self.load_settings)
        layout.add_widget(load_settings_button)

        # Save settings button
        save_settings_button = Button(text="Save Settings", size_hint=(0.2, None), height=50)
        save_settings_button.bind(on_press=self.save_settings)
        layout.add_widget(save_settings_button)

        # Connection settings section (initially hidden)
        self.connection_settings_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.connection_settings_layout.add_widget(Label(text="Connection Settings"))
        self.ip_input = TextInput(hint_text='IP Address')
        self.subnet_input = TextInput(hint_text='Subnet Mask')
        self.gateway_input = TextInput(hint_text='Gateway')
        self.dns_input = TextInput(hint_text='DNS Server')
        self.port_input = TextInput(hint_text='Port')
        
        self.connection_settings_layout.add_widget(self.ip_input)
        self.connection_settings_layout.add_widget(self.subnet_input)
        self.connection_settings_layout.add_widget(self.gateway_input)
        self.connection_settings_layout.add_widget(self.dns_input)
        self.connection_settings_layout.add_widget(self.port_input)
        self.connection_settings_layout.opacity = 0  # Initially hidden
        layout.add_widget(self.connection_settings_layout)

        # Bind protocol selection to show connection settings
        self.protocol_spinner.bind(text=self.on_protocol_select)

        return layout

    def on_protocol_select(self, spinner, text):
        if text in ['RS232', 'RS485']:  # Check if the selected protocol is a serial protocol
            self.show_serial_settings()  # Show serial settings layout
            self.connection_settings_layout.opacity = 1  # Show connection settings for serial protocols
        elif text in ['FINS', 'Modbus RTU', 'CANOpen', 'MQTT']:  # Check if the selected protocol requires IP settings
            self.connection_settings_layout.opacity = 1  # Show connection settings for IP protocols
        else:  # Hide settings for other protocols
            self.connection_settings_layout.opacity = 0  # Ensure settings are hidden for unsupported protocols

    def show_serial_settings(self):
        # Clear existing inputs
        self.connection_settings_layout.clear_widgets()  # Clear existing inputs
        self.connection_settings_layout.add_widget(Label(text="Serial Settings"))  # Add label for serial settings
        
        # Add SPI settings inputs
        self.spi_device_input = TextInput(hint_text='SPI Device')  # Add SPI device input
        self.connection_settings_layout.add_widget(self.spi_device_input)  # Add SPI device input to layout

        self.baudrate_input = TextInput(hint_text='Baud Rate')  # Add baud rate input for serial
        self.data_bits_input = TextInput(hint_text='Data Bits')  # Add data bits input for serial
        self.stop_bits_input = TextInput(hint_text='Stop Bits')  # Add stop bits input for serial
        
        self.connection_settings_layout.add_widget(self.baudrate_input)  # Add baud rate input to layout
        self.connection_settings_layout.add_widget(self.data_bits_input)  # Add data bits input to layout
        self.connection_settings_layout.add_widget(self.stop_bits_input)  # Add stop bits input to layout

    def show_connection_settings(self, instance):
        # Logic to handle connection when the button is pressed
        self.connect(instance)

    def read_spi(self, address, num_bytes):
        """Read bytes from SPI device.""" 
        if platform.system() == "Linux":
            # Implement SPI read using spidev or another method
            logging.error("SPI read not implemented for Windows. Use a compatible library or method.")
            return None
        else:
            logging.error("SPI functionality not available on this OS.")
            return None

    def write_spi(self, address, data):
        """Write bytes to SPI device.""" 
        if platform.system() == "Linux":
            # Implement SPI write using spidev or another method
            logging.error("SPI write not implemented for Windows. Use a compatible library or method.")
        else:
            logging.error("SPI functionality not available on this OS.")

    def connect(self, instance):
        protocol = self.protocol_spinner.text
        ip_address = self.ip_input.text
        port = self.port_input.text

        if protocol == 'FINS':
            if not ip_address or not port:
                logging.error("IP address and port must be provided for FINS connection.")
                return
            self.connect_fins(ip_address, port)
        elif protocol == 'Modbus RTU':
            self.connect_modbus_rtu(ip_address, port)
        elif protocol == 'CANOpen':
            self.connect_canopen(ip_address, port)
        elif protocol == 'MQTT':
            self.connect_mqtt(ip_address, port)
        # Add additional protocols as needed
        else:
            logging.error("Selected protocol not implemented.")

    def connect_fins(self, ip_address, port):
        logging.info(f"Connecting using FINS protocol to {ip_address}:{port}")
        # Example connection logic for FINS protocol
        try:
            fins_connection = TCPFinsConnection()  # Create an instance of TCPFinsConnection
            fins_connection.connect(ip_address, int(port))  # Establish the connection

            logging.info("FINS connection established successfully.")
        except Exception as e:
            logging.error(f"Failed to connect using FINS protocol: {e}")

    def connect_modbus_rtu(self, ip_address, port):
        logging.info(f"Connecting using Modbus RTU protocol to {ip_address}:{port}")
        # Example connection logic for Modbus RTU protocol
        try:
            modbus_connection = minimalmodbus.Instrument(port, 1)  # Example setup
            modbus_connection.serial.baudrate = 9600
            modbus_connection.serial.timeout = 1
            logging.info("Modbus RTU connection established successfully.")
        except Exception as e:
            logging.error(f"Failed to connect using Modbus RTU protocol: {e}")

    def connect_canopen(self, ip_address, port):
        logging.info(f"Connecting using CANOpen protocol to {ip_address}:{port}")
        # Example connection logic for CANOpen protocol
        try:
            import canopen  # Import the canopen module
            canopen_connection = canopen.Network()  # Create an instance of the CANOpen network

            canopen_connection.connect()
            logging.info("CANOpen connection established successfully.")
        except Exception as e:
            logging.error(f"Failed to connect using CANOpen protocol: {e}")

    def connect_mqtt(self, ip_address, port):
        logging.info(f"Connecting using MQTT protocol to {ip_address}:{port}")
        # Example connection logic for MQTT protocol
        try:
            mqtt_client = mqtt.Client()
            mqtt_client.connect(ip_address, int(port))  # Pass the port as an integer
            mqtt_client.loop_start()
            logging.info("MQTT connection established successfully.")
        except Exception as e:
            logging.error(f"Failed to connect using MQTT protocol: {e}")

    def disconnect(self, instance):
        logging.info("Disconnecting from device")
        # Implement disconnection logic here

    def load_settings(self, instance):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.ip_input.text = settings.get('ip_address', '')
                self.subnet_input.text = settings.get('subnet_mask', '')
                self.gateway_input.text = settings.get('gateway', '')
                self.dns_input.text = settings.get('dns', '')
                self.port_input.text = settings.get('port', '')
                logging.info("Settings loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading settings: {e}")

    def save_settings(self, instance):
        settings = {
            'ip_address': self.ip_input.text,
            'subnet_mask': self.subnet_input.text,
            'gateway': self.gateway_input.text,
            'dns': self.dns_input.text,
            'port': self.port_input.text,
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
                logging.info("Settings saved successfully.")
        except Exception as e:
            logging.error(f"Error saving settings: {e}")

if __name__ == '__main__':
    SmartHomeCommApp().run()
