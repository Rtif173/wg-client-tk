INSTALL_DIRECTORY = "~/.8kbh-wg-client"
ist = ""

ist += """#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi\n\n
"""
ist += '''
read -p "Name of config file: " name\n
'''
ist += (
    "# Creating install directory\n"
    f'install_directory={INSTALL_DIRECTORY}\n'
    'echo "Creating install directory: $install_directory"\n'
    "mkdir -p $install_directory\n\n"
)

with open("./pwd_dialog.py", encoding="utf-8") as f:
    ist += (
        'echo "Creating password dialog file: $install_directory/pwd_dialog.py"\n'
        'cat <<EOF > "$install_directory/pwd_dialog.py"\n'
        f'{f.read()}\n'
        'EOF\n\n'
    )

with open("./main.py", encoding="utf-8") as f:
    ist += (
        'echo "Creating main interface file: $install_directory/main.py"\n'
        'cat <<EOF > "$install_directory/main.py"\n'
        f'{f.read()}\n'
        'EOF\n\n'
    )


ist += '''
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
fi\n
'''

ist += (
    'echo "Creating desktop entry"\n'
    'cat <<EOF > "$install_directory/8kbh-wg-client.desktop"\n'
    '[Desktop Entry]\n'
    'Name=WireGuard Control\n'
    'Exec=/bin/bash -c \'cd $install_directory && source venv/bin/activate && bash -c "python3 pwd_dialog.py | sudo -S python3 main.py $name"\'\n'
    'Type=Application\n'
    'Terminal=false\n'
    'EOF\n\n'
    'cp -r $install_directory/8kbh-wg-client.desktop ~/.local/share/applications/'
)

with open("./install.sh", "w", encoding="utf-8") as f:
    f.write(ist)

ust = ""

ust += (
    f'install_directory={INSTALL_DIRECTORY}\n'
    "rm -r $install_directory\n"
    "rm ~/.local/share/applications/8kbh-wg-client.desktop\n"
)
with open("./uninstall.sh", "w", encoding="utf-8") as f:
    f.write(ust)