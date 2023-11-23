#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi



read -p "Name of config file: " name

# Creating install directory
install_directory=~/.8kbh-wg-client
echo "Creating install directory: $install_directory"
mkdir -p $install_directory

echo "Creating password dialog file: $install_directory/pwd_dialog.py"
cat <<EOF > "$install_directory/pwd_dialog.py"
import tkinter as tk
from tkinter import simpledialog

def get_password():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Use simpledialog to create a password prompt
    password = simpledialog.askstring("Password", "Enter your password:", show='*')

    return password

if __name__ == "__main__":
    password = get_password()
    print(password)
EOF

echo "Creating main interface file: $install_directory/main.py"
cat <<EOF > "$install_directory/main.py"
import tkinter as tk
from tkinter import messagebox
import subprocess
import argparse

class WireGuardControlApp:
    def __init__(self, master, name):
        self.master = master
        self.name = name
        self.master.title("WireGuard Control")

        self.status_label = tk.Label(master, text="Status:")
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        self.status_display = tk.Label(master, textvariable=self.status_var)
        self.status_display.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)

        self.connect_button = tk.Button(master, text="Connect", command=self.connect_wireguard)
        self.connect_button.grid(row=1, column=0, padx=10, pady=10)

        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_wireguard)
        self.disconnect_button.grid(row=1, column=1, padx=10, pady=10)

        self.update_status()

    def connect_wireguard(self):
        self.run_command(f"sudo wg-quick up {self.name}")
        self.update_status()

    def disconnect_wireguard(self):
        self.run_command(f"sudo wg-quick down {self.name}")
        self.update_status()

    def run_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command failed: {e}")

    def update_status(self):
        status = self.get_wireguard_status()
        self.status_var.set(status)

    def get_wireguard_status(self):
        try:
            result = subprocess.run(f"sudo wg show {self.name}", shell=True, stdout=subprocess.PIPE, text=True, check=True)
            return "Connected" if result.stdout else "Disconnected"
        except subprocess.CalledProcessError as e:
            return "Disconnected"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='wireguard client GUI')
    parser.add_argument('name', type=str, help='name of wireguard config file (ex. wg0 if the file is /etc/wireguard/wg0.conf)')
    args = parser.parse_args()
    name = args.name

    root = tk.Tk()
    app = WireGuardControlApp(root, name)
    root.mainloop()
EOF


venv_directory="$install_directory/venv"
if [ -d "$venv_directory" ]; then
    # Asking the user for confirmation
    read -p "The venv folder already exists ($install_directory/venv). Do you want to delete it? (y/n): " answer
    if [ "$answer" == "y" ]; then
        echo "Deleting existing venv folder..."
        rm -rf "$venv_directory"
        echo "Venv folder deleted."
        echo "Create virtual enviroment (py)..."
        python3 -m venv $install_directory/venv
    else
        echo "Venv folder not deleted."
    fi
else
    echo "Create virtual enviroment (py)..."
    python3 -m venv $install_directory/venv 
fi

echo "Creating desktop entry"
cat <<EOF > "$install_directory/8kbh-wg-client.desktop"
[Desktop Entry]
Name=WireGuard Control
Exec=/bin/bash -c 'cd $install_directory && source venv/bin/activate && bash -c "python3 pwd_dialog.py | sudo -S python3 main.py $name"'
Type=Application
Terminal=false
EOF

cp -r $install_directory/8kbh-wg-client.desktop ~/.local/share/applications/