# LethalCompanyModInstaller

This was intended to make installing Lethal Company mods easier for our group of friends. I created a simple GUI application that requires directory paths to install mods that use BepInEx.

The first directory is lethal company's "local files" directory. This can be found by right-clicking on lethal company in the steam library, going to "manage", and then "browse local files".
The directory that is opened up is the directory path that goes in the first text box, "Directory Path to ';ocal files of Lethal Company:".
  - After entering the path once, all future uses will have the path pre-loaded in the text box and will not need to be updated. (Unless installation path changes.)

The second required directory should be a folder that contains all of the BepInEx mods that you wish to install. Do not unzip the files when putting them into the folder.

Usage:
    - Have the zip files of the mods you wish to install in a single file.
    - Ensure that BepInEx is already installed in the local files of Lethal Company.
    - Run this script and provide the required information when prompted.

Note:
    This script assumes that the mod's zip file contains a BepInEx folder and
    should be used with caution. Always verify the mod's compatibility and 
    follow any additional instructions provided by the mod creator.

Disclaimer:
    The author is not responsible for any issues arising from the use of this script.
    Use it at your own risk.

Additional Information for myself:
    This is my first attempt at a simple GUI project. Intended to be used amongst my friends. This script saves very little time and was an effort
    to learn how to use PyQt5 and zip files.
