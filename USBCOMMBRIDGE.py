"""
Feature/Protocol Overview:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Feature/Protocol                       | Modicon PLCs                              |            Omron Sysmac PLCs                 |                   Omron CS & CJ Series                        |
|----------------------------------------|-------------------------------------------|----------------------------------------------|---------------------------------------------------------------|
| Primary Industrial Ethernet Protocol   | Modbus TCP/IP                             | EtherCAT                                     | Ethernet/IP, FINS, Modbus TCP/IP                              |
| Serial Communication                   | Modbus RTU (RS-232, RS-485)               | Modbus RTU (RS-232, RS-485)                  | RS-232, RS-485 (Host Link, Modbus RTU, ASCII-based protocols) |
| Proprietary Protocol                   | Modbus                                    | FINS                                         | FINS                                                          |
| Ethernet-based Protocols               | Ethernet/IP, Modbus TCP/IP                | EtherCAT, Ethernet/IP, PROFINET, CC-Link IE  | Ethernet/IP, Modbus TCP/IP, PROFINET                          |
| Fieldbus Protocols                     | Profibus DP, PROFINET, DeviceNet, CANopen | DeviceNet, PROFINET, CC-Link IE, CANopen     | DeviceNet, PROFINET, CC-Link, MECHATROLINK-II                 |
| OPC UA Support                         | Limited on some models                    | Yes                                          | No                                                            |
| Legacy Serial Support                  | RS-232, RS-485                            | RS-232, RS-485                               | RS-232, RS-485                                                |
| Integration with Third-Party Devices   | Strong with Modbus TCP/IP                 | Strong with EtherCAT                         | Strong with Modbus TCP/IP, DeviceNet, Ethernet/IP, and FINS   |
| Best for Motion Control                | Can use SERCOS III, CANopen               | EtherCAT                                     | MECHATROLINK-II                                               |
| Best for General Industrial Automation | Modbus TCP/IP, Ethernet/IP, PROFINET      | EtherNET/IP, PROFINET, CC-Link IE            | FINS, Modbus TCP/IP, DeviceNet, Ethernet/IP, PROFINET         |
| Use Case Suitability                   | Process automation, building automation   | Motion control, robotics, machine automation | Legacy automation systems, large-scale factory automation     |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import sys
import subprocess
from importlib import import_module
from importlib.metadata import version, PackageNotFoundError

import serial.tools.list_ports
import threading
from colorama import Fore, Style
import json
import logging
import time


# Function to check and install required packages
def check_and_install(package):
    # Check for Git installation
    git_check = subprocess.call(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if git_check != 0:
        print(Fore.RED + "Git is not installed. Please install Git from https://git-scm.com/downloads" + Style.RESET_ALL)

    try:
        __import__(package)
        try:
            version_info = version(package)
            print(Fore.GREEN + f"{package} is installed, version: {version_info}" + Style.RESET_ALL)
        except PackageNotFoundError:
            print(Fore.RED + f"{package} is not installed. Installing..." + Style.RESET_ALL)
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(Fore.GREEN + f"{package} has been installed." + Style.RESET_ALL)

        print(Fore.GREEN + f"{package} is installed, version: {version}" + Style.RESET_ALL)
    except ImportError:
        print(Fore.RED + f"{package} is not installed. Installing..." + Style.RESET_ALL)
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(Fore.GREEN + f"{package} has been installed." + Style.RESET_ALL)

# Check for required packages
check_and_install('serial')
check_and_install('colorama')

# Configure logging
logging.basicConfig(filename='usb_converter.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to display the banner with key parameters and examples
def display_banner():
    banner = r"""
    *******************************************************
    **           Serial Communication Settings           **
    *******************************************************
    
    ** Key Parameters and Examples: **

    1. **Serial Port**: 
       - Example: COM3 (Windows) or /dev/ttyUSB0 (Linux)
       - The communication port to which the USB-to-Serial converter is connected.

    2. **Baud Rate**: 
       - Default: 9600 (UART), 100000 (I2C), 500000 (SPI), 9600 (RS232/RS485/TTL/Control Command)
       - The speed at which data is transmitted between devices in bits per second.

    3. **Timeout**: 
       - Default: 1.0 seconds
       - The maximum time to wait for data to arrive before considering it a timeout.

    4. **Data Type**:
       - Choose from the following data types:
         - Text (ASCII or Unicode): Human-readable data (e.g., "Hello").
         - I2C: A multi-master, multi-slave, packet-switched, single-ended, serial communication bus (e.g., 0xFF).
         - SPI: A synchronous serial communication protocol used for short-distance communication (e.g., 0xAA).
         - RS232: A standard for serial communication transmission of data (e.g., "Data to send").
         - RS485: A standard for serial communication that allows for long-distance communication and multiple devices on the same bus (e.g., "Data to send").
         - TTL: Transistor-Transistor Logic, a type of digital signal (e.g., "Data to send").
         - Control Command: Specific commands for controlling devices (e.g., "START" or "STOP").

    5. **Communication Types**:
       - **Omron**: A communication protocol used for Omron PLCs.
       - **Modicon**: A communication protocol used for Modicon PLCs.
       - **Text**: ASCII or Unicode strings sent over UART.
       - **I2C**: Used for communication between microcontrollers and peripherals.
       - **SPI**: Used for high-speed communication between devices.
       - **RS232**: Standard for serial communication in computers and peripherals.
       - **RS485**: Used for long-distance communication in industrial environments.
       - **TTL**: Digital signals used in microcontroller communication.
       - **Control Commands**: Commands to control device operations.

    *******************************************************
    **           PLC Communication Settings           **
    *******************************************************
        - Omron: A communication protocol used for Omron PLCs.
            - Protocols: Modbus RTU, FINS, Ethernet/IP, and EtherCAT.
        - Modicon: A communication protocol used for Modicon PLCs.
            - Protocols: Modbus TCP/IP, Modbus RTU, and Ethernet/IP.
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

# Function to get user input for serial connection settings with validation
def list_serial_ports():
    """List all available serial ports with descriptions."""
    ports = serial.tools.list_ports.comports()
    available_ports = [(port.device, port.description) for port in ports]
    return available_ports

def save_settings(port, baudrate, timeout):
    """Save the serial settings to a JSON file."""
    settings = {
        'port': port,
        'baudrate': baudrate,
        'timeout': timeout
    }
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def load_settings():
    """Load the serial settings from a JSON file if it exists."""
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(Fore.RED + "Error loading settings. The file may be corrupted." + Style.RESET_ALL)
        return None

def get_serial_settings(protocol):
    # Load settings if available
    loaded_settings = load_settings()
    if loaded_settings:
        print(Fore.GREEN + "Loaded settings: " + str(loaded_settings) + Style.RESET_ALL)
        return loaded_settings['port'], loaded_settings['baudrate'], loaded_settings['timeout']

    # List available serial ports
    print("Available serial ports:")
    for device, description in list_serial_ports():
        print(f"- {device}: {description}")

    # Validate Serial Port if not using loaded settings
    while True:
        port = input("Enter the serial port from the list above: ").strip()
        if port != "":
            break
        else:
            print(Fore.RED + "Serial port cannot be empty. Please enter a valid serial port." + Style.RESET_ALL)
            print(Fore.YELLOW + "Type 'help' for more information." + Style.RESET_ALL)

    # Set default settings based on protocol
    baudrate, timeout = 9600, 1.0  # Default values
    if protocol == '2':  # I2C
        baudrate = 100000  # 100 kHz
    elif protocol == '3':  # SPI
        baudrate = 500000  # 500 kHz

    # Validate Baudrate (Positive Integer)
    while True:
        baudrate_input = input(f"Enter baud rate (default: {baudrate}): ")
        if baudrate_input.strip() == "":
            break
        try:
            baudrate = int(baudrate_input)
            if baudrate > 0:
                break
            else:
                print(Fore.RED + "Baud rate must be a positive number. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter a valid integer for baud rate." + Style.RESET_ALL)

    # Validate Timeout (Positive Float)
    while True:
        timeout_input = input(f"Enter timeout in seconds (default: {timeout}): ")
        if timeout_input.strip() == "":
            break
        try:
            timeout = float(timeout_input)
            if timeout > 0:
                break
            else:
                print(Fore.RED + "Timeout must be a positive number. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter a valid float for timeout." + Style.RESET_ALL)

    return port, baudrate, timeout

# Function to choose the type of data to send
def choose_data_type():
    print("\nChoose the type of data to send:")
    print("1. Text (ASCII or Unicode) for UART")
    print("2. I2C Data")
    print("3. SPI Data")
    print("4. RS232 Data")
    print("5. RS485 Data")
    print("6. TTL Data")
    print("7. Control Command (e.g., Start/Stop)")
    print("8. OMRON PLC")
    print("9. MODICON PLC")

    while True:
        choice = input("Enter the number corresponding to your choice (default: 1): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            break
        else:
            print(Fore.RED + "Invalid choice! Please select a valid option between 1 and 9." + Style.RESET_ALL)

    return choice

def choose_omron_protocol():
    print("\nChoose the OMRON communication protocol:")
    print("1. Modbus RTU")
    print("2. FINS")
    print("3. Ethernet/IP")
    print("4. EtherCAT")
    # Add more protocols as needed
    return input("Enter the number corresponding to your choice: ")

def choose_modicon_protocol():
    print("\nChoose the MODICON communication protocol:")
    print("1. Modbus TCP/IP")
    print("2. Modbus RTU")
    print("3. Ethernet/IP")
    # Add more protocols as needed
    return input("Enter the number corresponding to your choice: ")

# Function to read responses from the connected device
def read_device_responses(ser, timeout=1):
    start_time = time.time()
    while True:
        if ser.in_waiting > 0:  # Check if there is data waiting to be read
            response = ser.read(ser.in_waiting).decode('utf-8')  # Read and decode the response
            logging.info(f"Received data: {response}")  # Log received data
            print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
        elif time.time() - start_time > timeout:
            print(Fore.YELLOW + "No response received within the timeout period." + Style.RESET_ALL)
            break

# Function to send text data with input validity
def send_text_data(ser, timeout, retries=3):
    while retries > 0:
        text = input("Enter the text to send (ASCII or Unicode): ")
        if text.strip() != "":  # Check for empty text input
            ser.write(text.encode('utf-8'))  # Send the text as bytes for UART
            logging.info(f"Sent data: {text}")  # Log sent data
            print(Fore.GREEN + "Data sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:  # Use the defined timeout
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')  # Read and decode the response
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:  # Use the defined timeout
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')  # Read and decode the response
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        else:
            print(Fore.RED + "Text cannot be empty. Please enter valid text." + Style.RESET_ALL)

# Function to send I2C data
def send_i2c_data(ser, timeout, retries=3):

    while retries > 0:
        data = input("Enter the I2C data to send (in hex format, e.g., 0xFF): ")
        try:
            data_bytes = bytes.fromhex(data.replace("0x", ""))
            ser.write(data_bytes)
            logging.info(f"Sent I2C data: {data}")  # Log sent data
            print(Fore.GREEN + "I2C data sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter valid hex data." + Style.RESET_ALL)

# Function to send SPI data
def send_spi_data(ser, timeout, retries=3):

    while retries > 0:
        data = input("Enter the SPI data to send (in hex format, e.g., 0xFF): ")
        try:
            data_bytes = bytes.fromhex(data.replace("0x", ""))
            ser.write(data_bytes)
            logging.info(f"Sent SPI data: {data}")  # Log sent data
            print(Fore.GREEN + "SPI data sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter valid hex data." + Style.RESET_ALL)

# Function to send RS232 data
def send_rs232_data(ser, timeout, retries=3):

    while retries > 0:
        data = input("Enter the RS232 data to send: ")
        if data.strip() != "":
            ser.write(data.encode('utf-8'))
            logging.info(f"Sent RS232 data: {data}")  # Log sent data
            print(Fore.GREEN + "RS232 data sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        else:
            print(Fore.RED + "Data cannot be empty. Please enter valid data." + Style.RESET_ALL)

# Function to send RS485 data
def send_rs485_data(ser, timeout, retries=3):

    while retries > 0:
        data = input("Enter the RS485 data to send: ")
        if data.strip() != "":
            ser.write(data.encode('utf-8'))
            logging.info(f"Sent RS485 data: {data}")  # Log sent data
            print(Fore.GREEN + "RS485 data sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        else:
            print(Fore.RED + "Data cannot be empty. Please enter valid data." + Style.RESET_ALL)

# Function to send TTL data
def send_ttl_data(ser, timeout, retries=3):

    while retries > 0:
        data = input("Enter the TTL data to send: ")
        if data.strip() != "":
            ser.write(data.encode('utf-8'))
            logging.info(f"Sent TTL data: {data}")  # Log sent data
            print(Fore.GREEN + "TTL data sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        else:
            print(Fore.RED + "Data cannot be empty. Please enter valid data." + Style.RESET_ALL)

# Function to send Control Command data
def send_control_command(ser, timeout, retries=3):

    while retries > 0:
        command = input("Enter the control command to send: ")
        if command.strip() != "":
            ser.write(command.encode('utf-8'))
            logging.info(f"Sent control command: {command}")  # Log sent data
            print(Fore.GREEN + "Control command sent. Waiting for response..." + Style.RESET_ALL)
            response_received = False
            
            # Wait for a response with a timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if ser.in_waiting > 0:
                    response = ser.read(ser.in_waiting).decode('utf-8')
                    logging.info(f"Received data: {response}")  # Log received data
                    print(Fore.GREEN + f"Response from device: {response}" + Style.RESET_ALL)
                    response_received = True
                    break
            
            if not response_received:
                retries -= 1
                print(Fore.RED + f"No response received. You have {retries} retries left." + Style.RESET_ALL)
                if retries == 0:
                    print(Fore.RED + "No valid response received after multiple attempts. Exiting." + Style.RESET_ALL)
                    break
        else:
            print(Fore.RED + "Command cannot be empty. Please enter a valid command." + Style.RESET_ALL)

# Main function to handle program flow with validation
def main():
    print(r"""
      ___           ___           ___                    ___           ___           ___           ___                    ___           ___                       ___           ___           ___     
     /\__\         /\  \         /\  \                  /\  \         /\  \         /\__\         /\__\                  /\  \         /\  \          ___        /\  \         /\  \         /\  \    
    /:/  /        /::\  \       /::\  \                /::\  \       /::\  \       /::|  |       /::|  |                /::\  \       /::\  \        /\  \      /::\  \       /::\  \       /::\  \   
   /:/  /        /:/\ \  \     /:/\:\  \              /:/\:\  \     /:/\:\  \     /:|:|  |      /:|:|  |               /:/\:\  \     /:/\:\  \       \:\  \    /:/\:\  \     /:/\:\  \     /:/\:\  \  
  /:/  /  ___   _\:\~\ \  \   /::\~\:\__\            /:/  \:\  \   /:/  \:\  \   /:/|:|__|__   /:/|:|__|__            /::\~\:\__\   /::\~\:\  \      /::\__\  /:/  \:\__\   /:/  \:\  \   /::\~\:\  \ 
 /:/__/  /\__\ /\ \:\ \ \__\ /:/\:\ \:|__|          /:/__/ \:\__\ /:/__/ \:\__\ /:/ |::::\__\ /:/ |::::\__\          /:/\:\ \:|__| /:/\:\ \:\__\  __/:/\/__/ /:/__/ \:|__| /:/__/_\:\__\ /:/\:\ \:\__\
 \:\  \ /:/  / \:\ \:\ \/__/ \:\~\:\/:/  /          \:\  \  \/__/ \:\  \ /:/  / \/__/~~/:/  / \/__/~~/:/  /          \:\~\:\/:/  / \/_|::\/:/  / /\/:/  /    \:\  \ /:/  / \:\  /\ \/__/ \:\~\:\ \/__/
  \:\  /:/  /   \:\ \:\__\    \:\ \::/  /            \:\  \        \:\  /:/  /        /:/  /        /:/  /            \:\ \::/  /     |:|::/  /  \::/__/      \:\  /:/  /   \:\ \:\__\    \:\ \:\__\  
   \:\/:/  /     \:\/:/  /     \:\/:/  /              \:\__\        \:\/:/  /        /:/  /        /:/  /              \:\/:/  /      |:|\/__/    \:\__\       \:\/:/  /     \:\/:/  /     \:\ \/__/  
    \::/  /       \::/  /       \::/__/                \:\__\        \::/  /        /:/  /        /:/  /                \::/__/       |:|  |       \/__/        \::/__/       \::/  /       \:\__\    
     \/__/         \/__/         ~~                     \/__/         \/__/         \/__/         \/__/                  ~~            \|__|                     ~~            \/__/         \/__/
Feature/Protocol Overview:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Feature/Protocol                       | Modicon PLCs                              |            Omron Sysmac PLCs                 |                   Omron CS & CJ Series                        |
|----------------------------------------|-------------------------------------------|----------------------------------------------|---------------------------------------------------------------|
| Primary Industrial Ethernet Protocol   | Modbus TCP/IP                             | EtherCAT                                     | Ethernet/IP, FINS, Modbus TCP/IP                              |
| Serial Communication                   | Modbus RTU (RS-232, RS-485)               | Modbus RTU (RS-232, RS-485)                  | RS-232, RS-485 (Host Link, Modbus RTU, ASCII-based protocols) |
| Proprietary Protocol                   | Modbus                                    | FINS                                         | FINS                                                          |
| Ethernet-based Protocols               | Ethernet/IP, Modbus TCP/IP                | EtherCAT, Ethernet/IP, PROFINET, CC-Link IE  | Ethernet/IP, Modbus TCP/IP, PROFINET                          |
| Fieldbus Protocols                     | Profibus DP, PROFINET, DeviceNet, CANopen | DeviceNet, PROFINET, CC-Link IE, CANopen     | DeviceNet, PROFINET, CC-Link, MECHATROLINK-II                 |
| OPC UA Support                         | Limited on some models                    | Yes                                          | No                                                            |
| Legacy Serial Support                  | RS-232, RS-485                            | RS-232, RS-485                               | RS-232, RS-485                                                |
| Integration with Third-Party Devices   | Strong with Modbus TCP/IP                 | Strong with EtherCAT                         | Strong with Modbus TCP/IP, DeviceNet, Ethernet/IP, and FINS   |
| Best for Motion Control                | Can use SERCOS III, CANopen               | EtherCAT                                     | MECHATROLINK-II                                               |
| Best for General Industrial Automation | Modbus TCP/IP, Ethernet/IP, PROFINET      | EtherNET/IP, PROFINET, CC-Link IE            | FINS, Modbus TCP/IP, DeviceNet, Ethernet/IP, PROFINET         |
| Use Case Suitability                   | Process automation, building automation   | Motion control, robotics, machine automation | Legacy automation systems, large-scale factory automation     |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------          

""")
    
    load_settings_prompt = input("Do you want to load the settings file? (y/n): ").strip().lower()
    if load_settings_prompt == 'y':
        loaded_settings = load_settings()
        if loaded_settings:
            print(Fore.GREEN + "Loaded settings successfully: " + str(loaded_settings) + Style.RESET_ALL)
            port, baudrate, timeout = loaded_settings['port'], loaded_settings['baudrate'], loaded_settings['timeout']
        else:
            print(Fore.RED + "No settings file found. A new settings file will be created." + Style.RESET_ALL)
            port, baudrate, timeout = None, None, None
    else:
        port, baudrate, timeout = None, None, None

    display_banner()
    protocol = choose_data_type()
    retries = int(input("Enter the number of retries (default: 3): ") or retries)


    if port is None or baudrate is None or timeout is None:
        port, baudrate, timeout = get_serial_settings(protocol)
        save_settings(port, baudrate, timeout)

    while True:
        try:
            ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            break
        except serial.SerialException as e:
            print(Fore.RED + f"Error opening serial port: {e}. Please check the port and try again." + Style.RESET_ALL)
            retry = input("Do you want to retry the same port? (y/n): ").strip().lower()
            if retry != 'y':
                port = input("Enter a different serial port from the list above: ").strip()
                if not port:
                    print(Fore.RED + "Serial port cannot be empty. Please enter a valid serial port. Type 'help' for more information." + Style.RESET_ALL)
                    continue

    response_thread = threading.Thread(target=read_device_responses, args=(ser, timeout))
    response_thread.daemon = True
    response_thread.start()

    while True:
        if protocol in ['1', '2', '3', '4', '5', '6', '7']:

            send_text_data(ser, timeout, retries)
        elif protocol == '2':
            send_i2c_data(ser, timeout, retries)
        elif protocol == '3':
            send_spi_data(ser, timeout, retries)
        elif protocol == '4':
            send_rs232_data(ser, timeout, retries)
        elif protocol == '5':
            send_rs485_data(ser, timeout, retries)
        elif protocol == '6':
            send_ttl_data(ser, timeout, retries)
        elif protocol == '7':
            send_control_command(ser, timeout, retries)
        elif protocol == '8':
            send_text_data(ser, timeout, retries)  # Example for additional functionality
        elif protocol == '9':
            send_i2c_data(ser, timeout, retries)  # Example for additional functionality
        elif protocol == '10':
            send_spi_data(ser, timeout, retries)  # Example for additional functionality


        again = input("Do you want to send more data? (y/n): ").strip().lower()
        if again != 'y':
            print(Fore.YELLOW + "Exiting program." + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()
