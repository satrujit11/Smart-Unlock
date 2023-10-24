import time
import subprocess

#phone mac address
PHONE_ADDRESS = "94:52:44:CD:97:7F"
SIGNAL_THRESHOLD = -10

def turn_on_bluetooth():
    subprocess.run(["rfkill", "unblock", "bluetooth"])

def is_bluetooth_on():
    output = subprocess.run(["rfkill", "list", "bluetooth"], capture_output=True, text=True)
    return "Soft blocked: yes" not in output.stdout

def get_device_signal_strength(device_address):
    output = subprocess.run(["hcitool", "rssi", device_address], capture_output=True, text=True)
    lines = output.stdout.strip().split("\n")
    for line in lines:
        if "RSSI return value" in line:
            rssi_value = line.split(": ")[1]
            try:
                rssi = int(rssi_value)
                return rssi
            except ValueError:
                return None
    return None

def lock_screen():
    subprocess.run(["loginctl", "lock-session"])
    #subprocess.run(["gdbus", "call", "--session", "--dest", "org.gnome.ScreenSaver", "--object-path",



def unlock_screen():
    subprocess.run(["loginctl", "unlock-session"])
    #subprocess.run(["gdbus", "call", "--session", "--dest", "org.gnome.ScreenSaver", "--object-path", "/org/gnome/ScreenSaver", "--method", "org.gnome.ScreenSaver.SetActive", "false"])


def is_device_connected(device_address):
    output = subprocess.run(["bluetoothctl", "info", device_address], capture_output=True, text=True)
    return "Connected: yes" in output.stdout

def connect_to_device():
    print("Checking Bluetooth status...")
    if not is_bluetooth_on():
        print("Bluetooth is off. Turning it on...")
        turn_on_bluetooth()
        time.sleep(2)  # Wait for Bluetooth to initialize

    device_connected = is_device_connected(PHONE_ADDRESS)
    if device_connected:
        print("Already connected to the phone")
    
    while True:
        if device_connected:
            signal_strength = get_device_signal_strength(PHONE_ADDRESS)
            if signal_strength is not None:
                print(f"Signal Strength: {signal_strength} dBm")
                if signal_strength < SIGNAL_THRESHOLD:
                    lock_screen()
                else:
                    unlock_screen()
            time.sleep(1)
        else:
            print("Connecting to device...")
            subprocess.run(["bluetoothctl", "connect", PHONE_ADDRESS])
            time.sleep(5)  # Retry connection after 5 seconds

        device_connected = is_device_connected(PHONE_ADDRESS)


if __name__ == "__main__":
    connect_to_device()

