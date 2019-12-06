import sys, os

# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.
sys.path.append('C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation')


import bpy
import folder_test
from tests import test 

import importlib
# reload every import 
importlib.reload(folder_test)
importlib.reload(test)

# bpy.ops.object.delete(use_global=False, confirm=False)
def main():
     folder_test.folder_test()
     test.test()

if __name__ == "__main__":
     main()