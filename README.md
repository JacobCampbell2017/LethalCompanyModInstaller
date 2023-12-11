# LethalCompanyModInstaller

This was intended to make installing Lethal Company mods easier for our group of friends. I created a simple GUI application that requires directory paths to install mods that use BepInEx.

The checkbox allows a user to install BepInEx straight from GitHub into the local files of lethal company. If the local file path is correct, the installer will add BepInEx directly to it. 

The first directory is lethal company's "local files" directory. This can be found by right-clicking on lethal company in the steam library, going to "manage", and then "browse local files".
The directory that is opened up is the directory path that goes in the first text box, "Directory Path to ';ocal files of Lethal Company:".
  - After entering the path once, all future uses will have the path pre-loaded in the text box and will not need to be updated. (Unless installation path changes.)

The second required directory should be a folder that contains all of the BepInEx mods that you wish to install. Do not unzip the files when putting them into the folder.
    - This can be left blank if you are only wanting to install BepInEx without mods.

**This currently does not uninstall currently installed mods**

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
