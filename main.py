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