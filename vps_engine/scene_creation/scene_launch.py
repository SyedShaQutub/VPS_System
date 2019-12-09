import sys, os

# reload every import 
import importlib
import bpy
# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.

# TODO: When excecuted in blender the os.path gives out C:/ instead of abs path of scene_launch; for now hard code the abs path of this file.
# office WS C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation
# HP laptop C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation
filepath = bpy.context.space_data.text.filepath
PYTHON_PATH = os.path.dirname(filepath)
PYTHON_PATH = PYTHON_PATH.replace('\\','/')
scene_path = os.path.join(PYTHON_PATH.rsplit("/",2)[0] + '/scene_content')
sys.path.append(PYTHON_PATH)

import blender_utils
importlib.reload(blender_utils)
from blender_utils import *

import asset_import
importlib.reload(asset_import)
from asset_import import *


def main():
     bld_clearobjs()

     # TODO: Import city and character models form bash file
     citymodel_path= os.path.join(scene_path + '/graphics/city_models/9btvoxf8n0cg-3dt/Street environment_V01.FBX') #"C:/Users/Qutub/Documents/VPS_System/scene_content/graphics/city_models/9btvoxf8n0cg-3dt/Street environment_V01.FBX"
     filetype = "FBX"
     city = CityModels(name='Square_City',path=citymodel_path,filetype=filetype)

     mhchar_path = os.path.join(scene_path + '/graphics/3D_characters/makehuman_characters/characters/male_basic/male_basic.mhx2')
     male_char = MakeHuman('male_basic', mhchar_path)

     mocap_data = os.path.join(scene_path + '/graphics/3D_characters/Motion Capture data/Female1_bvh/Female1_B03_Walk1.bvh')
     male_char.attach_mocap(mocap_data)
     bpy.ops.screen.animation_play()

if __name__ == "__main__":
     main()
     

