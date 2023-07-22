import tkinter as tk
from tkinter import messagebox
import subprocess
import random

def get_network_interfaces():
    try:
        output = subprocess.check_output(["ifconfig"]).decode("utf-8")
        interfaces = []
        for line in output.split('\n'):
            if line.strip() and not line.startswith(' '):
                interface = line.split(':')[0]
                interfaces.append(interface)
        return interfaces
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_mac_address(interface):
    try:
        output = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
        mac_address = output.split("ether ")[1].split()[0]
        return mac_address
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown"

def get_random_mac():
    random_mac = [0x00, 0x16, 0x3e,
                  random.randint(0x00, 0x7f),
                  random.randint(0x00, 0xff),
                  random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, random_mac))

def change_mac(interface, new_mac):
    try:
        # Disable the network interface
        subprocess.call(["sudo", "ifconfig", interface, "down"])

        # Change the MAC address
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])

        # Enable the network interface
        subprocess.call(["sudo", "ifconfig", interface, "up"])

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def on_interface_select(event):
    selected_interface = interface_var.get()
    current_mac = get_mac_address(selected_interface)
    current_mac_label.config(text=f"Current MAC Address: {current_mac}")

def on_button_click():
    selected_interface = interface_var.get()
    new_mac = get_random_mac()
    success = change_mac(selected_interface, new_mac)
    
    if success:
        new_mac_label.config(text=f"New MAC Address: {new_mac}")
        messagebox.showinfo("Success", f"MAC address of {selected_interface} changed to {new_mac}")
    else:
        messagebox.showerror("Error", "Failed to change MAC address.")

# Create the main application window
root = tk.Tk()
root.title("Ratboy's MAC Changer")

# ASCII art text
ascii_text = """
@@@@@@@    @@@@@@   @@@@@@@  @@@@@@@    @@@@@@   @@@ @@@  
@@@@@@@@  @@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@ @@@  
@@!  @@@  @@!  @@@    @@!    @@!  @@@  @@!  @@@  @@! !@@  
!@!  @!@  !@!  @!@    !@!    !@   @!@  !@!  @!@  !@! @!!  
@!@!!@!   @!@!@!@!    @!!    @!@!@!@   @!@  !@!   !@!@!   
!!@!@!    !!!@!!!!    !!!    !!!@!!!!  !@!  !!!    @!!!   
!!: :!!   !!:  !!!    !!:    !!:  !!!  !!:  !!!    !!:    
:!:  !:!  :!:  !:!    :!:    :!:  !:!  :!:  !:!    :!:    
::   :::  ::   :::     ::     :: ::::  ::::: ::     ::    
 :   : :   :   : :     :     :: : ::    : :  :      :    
"""

ascii_label = tk.Label(root, text=ascii_text, font=("Courier", 12))
ascii_label.pack()

# Get available network interfaces
interfaces = get_network_interfaces()

# Create interface selection label and dropdown
interface_label = tk.Label(root, text="Select Interface:")
interface_label.pack()

interface_var = tk.StringVar(root)
interface_var.set(interfaces[0])  # Set default value
interface_menu = tk.OptionMenu(root, interface_var, *interfaces, command=on_interface_select)
interface_menu.pack()

# Create label to display current MAC address
current_mac_label = tk.Label(root, text="", font=("Arial", 12))
current_mac_label.pack()

# Create label to display new MAC address
new_mac_label = tk.Label(root, text="", font=("Arial", 12))
new_mac_label.pack()

# Create the change MAC address button
change_button = tk.Button(root, text="Change MAC Address", command=on_button_click)
change_button.pack()

# Start the GUI event loop
root.mainloop()
