# Simple WireGuard client GUI

Based on Python and Tkinter. Works only on Linux.

## Instalation
Download `install.sh`

Run
```
./install.sh
```
After that, you will be prompted to enter the name of the WireGuard configuration file. If the file is located at `/etc/wireguard/wg0.conf`, then the name should be `wg0`.

## Launch
Start the program from the startup menu. Its name is **WireGuard Control**

Normally, program files are located in `~/.8kbh-wg-client/` 

## Uninstall
Download `uninstall.sh`

Run

```
./uninstall.sh
```

This command remove all program files and the icon from the startup menu

## Usage from Source Code
If you want to run the program not from the startup menu but from the console, execute the following command:

```
python3 ~/.8kbh-wg-client/main.py name_of_config
```

Replace `name_of_config` with the name of WireGuard configuration file as in section *Installation* 