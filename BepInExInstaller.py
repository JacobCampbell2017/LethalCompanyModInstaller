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
        # pre_label = QLabel('This only works if you have BepInEx already installed to LethalCompany local files.')
        
        # BepInEx-related widgets
        self.BepInEx_checkbox = QCheckBox('Install BepInEx')
        
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
        layout.addWidget(self.BepInEx_checkbox)
        layout.addWidget(dir_label)
        layout.addWidget(self.dir_input)
        layout.addWidget(dir_save_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.mod_label)
        layout.addWidget(self.mod_input)
        layout.addWidget(mod_save_button)
        layout.addWidget(self.mod_status_label)
        layout.addWidget(exit_button)

        # Set layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Lethal Company BepInEx Mod Installer')
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
        self.status_label.setText(f'Directory path saved: {self.directory_path}')
    
    def mod_button_click(self):
        
        # Install BepInEx if the checkbox is checked
        BepText = ''
        if (self.BepInEx_checkbox.isChecked()):
            Download_BepInEx(self.directory_path)
        
        # Get the mod path from the input field
        mod_path = self.mod_input.text()
        
        # Grab BepInEx folder from zip files and copy to lethal company directory
        try:
            if(self.BepInEx_checkbox.isChecked()):
                BepText = 'BepInEx Installed'
            self.mod_status_label.setText(f'{BepText} - Files moved: {extract_and_copy_bepinex(mod_path, self.directory_path)}')
        except FileNotFoundError:
            self.mod_status_label.setText(f'{BepText} - Incorrect mod folder path. Please enter the correct mod folder path.')

        
def extract_and_copy_bepinex(mod_file_path, destination_path):
    
    # Sleep to show application changes
    time.sleep(2)
    
    to_return =[]
    # Create a temporary folder if it doesn't exist
    if not os.path.exists(".\\TempFolder"):
        os.mkdir(".\\TempFolder")
    
    # Extract the contents of the zip file to the temporary folder
    for file in os.listdir(mod_file_path):
        print(f'Extracting {file}...')
        to_return.append(file)
        with zipfile.ZipFile(os.path.join(mod_file_path,file), 'r') as zip_ref:
            zip_ref.extractall(".\\TempFolder")
    
        # Remove all files not named BepInEx in '.\\TempFolder'
        for file in os.listdir(".\\TempFolder"):
            if file != "BepInEx":
                os.remove(f".\\TempFolder\\{file}")
    
    # Move the contents of the temporary folder to the destination path
    move_to_dest(destination_path)
    
    # Remove the temporary folder
    shutil.rmtree(".\\TempFolder")
    
    return to_return


def move_to_dest(destination_path):
    # Copy the contents of '.\\TempFolder' to the destination path
    shutil.copytree(".\\TempFolder", destination_path, dirs_exist_ok=True)

def Download_BepInEx(destination_path):
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
