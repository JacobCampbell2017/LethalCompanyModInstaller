'''
modinstaller.py

Description:
    This script facilitates the installation of BepInEx and/or mods for Lethal Company. 
    The user is prompted to input the path to the local installation of Lethal Company 
    and the path to the file that contains all the mods you wish to install. The script extracts the BepInEx folder from 
    the zip files and copies it to the specified Lethal Company directory.
    
    The current BepInEx version is 5.4.22.0. If the version changes, the script will not install properly.

Author:
    Jacob Campbell

Date:
    12-11-2023

Usage:
    - If you have not already installed BepInEx into LethalCompany local files, you will need to install it by checking the 
    "install BepInEx" checkbox.
    - Have the zip files of the mods you wish to install in a single file.
    - Run this script and provide the required information when prompted.
    - If you only want to install BepInEx, you can leave the mod path empty and BepInEx will install if the checkbox is checked.
    
Note:
    This script should be used with caution. Always verify the mod's compatibility and 
    follow any additional instructions provided by the mod creator.

Disclaimer:
    The author is not responsible for any issues arising from the use of this script.
    Use it at your own risk.

'''


from urllib.request import urlopen
from io import BytesIO
import os
import time
import sys
import shutil
import zipfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox


# change to URL of current version of BepInEx
x64URL = 'https://github.com/BepInEx/BepInEx/releases/download/v5.4.22/BepInEx_x64_5.4.22.0.zip'

# if BepInEx installs other files add them here
BepFiles = ['BepInEx', 'changelog.txt', 'doorstop_config.ini', 'winhttp.dll']



class MyDirectoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Check if the directory.txt file exists
        if os.path.exists("directory.txt"):
            with open("directory.txt", "r") as file:
                self.directory_path = file.read().strip()
        else:
            self.directory_path = None
            
        # Initialize mod_path to None (you may want to change this based on your requirements)
        mod_path = None

        # Create widgets
        self.error_label = QLabel()
        
        # BepInEx-related widgets
        self.BepInEx_checkbox = QCheckBox('Install BepInEx')
        self.uninstall_checkbox = QCheckBox('Uninstall Current Mods and BepInEx')
        
        # Directory-related widgets
        dir_label = QLabel('Directory Path to \'local files\' of Lethal Company:')
        self.dir_input = QLineEdit(self.directory_path)
        dir_save_button = QPushButton('Save Directory Path:')
        
        # Mod-related widgets
        self.mod_input = QLineEdit(mod_path)
        self.mod_label = QLabel('Path to folder filled with mod zip files:')
        mod_save_button = QPushButton('Save Mod Path:')
        
        # Status labels
        self.status_label = QLabel()
        self.mod_status_label = QLabel()
        
        # Exit button
        exit_button = QPushButton('Exit')

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.error_label)
        layout.addWidget(dir_label)
        layout.addWidget(self.dir_input)
        layout.addWidget(dir_save_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.uninstall_checkbox)
        layout.addWidget(self.BepInEx_checkbox)
        layout.addWidget(self.mod_label)
        layout.addWidget(self.mod_input)
        layout.addWidget(mod_save_button)
        layout.addWidget(self.mod_status_label)
        layout.addWidget(exit_button)

        # Set layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('LethalCompany Mod Installer - V1.0')
        self.setGeometry(400, 500, 1000, 400)

        # Connect button click events to functions
        dir_save_button.clicked.connect(self.dir_button_click)
        mod_save_button.clicked.connect(self.mod_button_click)
        exit_button.clicked.connect(sys.exit)
        
        # Show the window
        self.show()

    def dir_button_click(self):
        # Get the directory path from the input field
        self.directory_path = self.dir_input.text()
    
        # Write the directory path to the directory.txt file
        with open("directory.txt", "w") as file:
            file.write(self.directory_path)

        # Display the status message in the window
        try:
            self.status_label.setText(f'Directory path saved: {self.directory_path}')
            self.error_label.setText('')
            
        except FileNotFoundError:
            self.error_label.setText(f'ERROR! Directory path not found: {self.directory_path} - Please make sure you saved Directory before saving mods.')
    
    def mod_button_click(self):
        
        # Uninstall the current mods and BepInEx if the checkbox is checked
        Bep_Uninstall_Text =''
        if self.uninstall_checkbox.isChecked():
            Bep_Uninstall_Text = 'Uninstall successful'
            for file in os.listdir(self.directory_path):
                if file in BepFiles:
                    print(f'Removing {file}...')
                    if os.path.isfile(os.path.join(self.directory_path, file)):
                        os.remove(os.path.join(self.directory_path, file))
                    else:
                        shutil.rmtree(os.path.join(self.directory_path, file))
        
        # Install BepInEx if the checkbox is checked
        Bep_Install_Text = ''
        try:
            if (self.BepInEx_checkbox.isChecked()):
                Download_BepInEx(self.directory_path)
                self.error_label.setText('')
        except FileNotFoundError:
            self.error_label.setText(f'ERROR! Destination directory does not exist: {self.directory_path} - Please make sure you saved Directory before saving mods.')
        
        # Get the mod path from the input field
        mod_path = self.mod_input.text()
        
        # Grab BepInEx folder from zip files and copy to lethal company directory
        try:
            if(self.BepInEx_checkbox.isChecked()):
                Bep_Install_Text = 'BepInEx Installed'
                self.status_label.setText(f'Directory path saved: {self.directory_path} - BepInEx installed successfully.')
            self.mod_status_label.setText(f'{Bep_Uninstall_Text} - {Bep_Install_Text} - Files moved: {extract_and_copy_bepinex(mod_path, self.directory_path)}')
        except FileNotFoundError:
            self.mod_status_label.setText(f'{Bep_Uninstall_Text} - Incorrect mod folder path. Please enter the correct mod folder path.')

        
def extract_and_copy_bepinex(mod_file_path, destination_path):
    
    # Verify that the destination directory exists
    if (not os.path.exists(destination_path)):
        raise FileNotFoundError()
    
    # Sleep to show application changes
    time.sleep(1)
    to_return = []
    
    # Extract the contents of the zip file to the destination directory
    for entry in os.listdir(mod_file_path):
        print(f'Extracting {entry}...')
        to_return.append(entry)
        with zipfile.ZipFile(os.path.join(mod_file_path, entry), 'r') as zip_ref:
            for file in zip_ref.namelist():
                if (file.startswith("BepInEx/")):
                    zip_ref.extract(file, destination_path)
    
    return to_return

def Download_BepInEx(destination_path):
    
    # Verify that the destination directory exists
    if not os.path.exists(destination_path):
        raise FileNotFoundError()
    
    # Download the BepInEx folder from GitHub
    http_response = urlopen(x64URL)
    with zipfile.ZipFile(BytesIO(http_response.read()), 'r') as zip_ref:
        zip_ref.extractall(destination_path)


def main():
    app = QApplication(sys.argv)
    my_app = MyDirectoryApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
