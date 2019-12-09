import sys, os

# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.

# TODO: When excecuted in blender the os.path gives out C:/ instead of abs path of scene_launch; for now hard code the abs path of this file.
# office WS C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation
# HP laptop C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation
sys.path.append('C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation')

import folder_test
from tests import test 

import city_scene
from city_scene import CityModels

# reload every import 
import importlib
importlib.reload(folder_test)
importlib.reload(test)
importlib.reload(city_scene)

def bld_clearobjs():
     pass

# bpy.ops.object.delete(use_global=False, confirm=False)
def main():
     # folder_test.folder_test()
     # test.test()
     bld_clearobjs()

     # TODO: Import city and character models form bash file
     citymodel_path = "C:/Users/squtub/Documents/Master Thesis/Git/scene_content/graphics/city_models/Street environment_V01.FBX"
     filetype = "FBX"
     os.path.isfile("C:/Users/squtub/Documents/Master_Thesis/Git/scene_content/graphics/city_models/Street environment_V01.FBX")
     #city = CityModels(name='Square_City',path=citymodel_path,filetype=filetype)


if __name__ == "__main__":
     main()