# reload every import 
import sys, os
import importlib
from collections import namedtuple
import bpy

# TODO: change this to relative path using os/pathlib
# NOTE: If you load Blender first then open a project then the CWD is where Blender is. If you script from the blender the CWD is the location of the blender program.

# TODO: When excecuted in blender the os.path gives out C:/ instead of abs path of scene_launch; for now hard code the abs path of this file.
# office WS C:/Users/Qutub/Documents/VPS/scene_content/VPS_project/scene_creation
# HP laptop C:/Users/squtub/Documents/Master_Thesis/Git/vps_engine/scene_creation

if os.name == 'nt':
     ## Doesn't support background execution
     blend_dir = os.path.dirname(bpy.context.space_data.text.filepath)
     blend_dir = blend_dir.replace('\\','/')
elif os.name == 'posix':
     ## Supports background execution
     blend_dir = os.path.dirname(os.path.realpath(__file__))

print("blender script executed from: ")
print(blend_dir)
#scenecontent_path = os.path.join(blend_dir.rsplit("/",2)[0] + '/scene_content')
if blend_dir not in sys.path:
     sys.path.append(blend_dir)

import data_config
importlib.reload(data_config)
data_config.os_env = os.name

# import addon_utils
# addon_utils.enable("sun_pos")
bpy.ops.preferences.addon_enable(module = "sun_position")
import blender_utils
# blender internal module to use custom modules
#blender_utils = bpy.data.texts['blender_utils.py'].as_module()
importlib.reload(blender_utils)
from blender_utils import *

import skymodel
importlib.reload(skymodel)
from skymodel import *

import asset_import
importlib.reload(asset_import)
from asset_import import *

import gen_dataset
importlib.reload(gen_dataset)
from gen_dataset import *

import gen_labels
importlib.reload(gen_labels)
from gen_labels import *


if data_config.os_env == 'nt':
     data_gene_path = "Z:\kia\input\paramterized_SynDatasets\polygonCity"
elif data_config.os_env == 'posix':
     data_gene_path = "/raid01/kia/input/paramterized_SynDatasets/polygonCity"

DEBUG = False
if DEBUG == True:
     PYDEV_SOURCE_DIR = "C:/Users/Qutub/.p2/pool/plugins/org.python.pydev.core_7.4.0.201910251334/pysrc"
     # "/usr/lib/eclipse/dropins/pydev/eclipse/plugins/org.python.pydev_4.5.4.201601292234/pysrc"
     #C:/Users/Qutub/.p2/pool/plugins/org.python.pydev.core_7.4.0.201910251334/pysrc

     if PYDEV_SOURCE_DIR not in sys.path:
          sys.path.append(PYDEV_SOURCE_DIR)

     import pydevd

     pydevd.settrace()

     bling = "the parrot has ceased to be"
     print(bling)
     
def test_edited_bvh(character_path):
     mocap_data_basicwalk_edited = os.path.join(scenecontent_path + '/graphics/3D_characters/Motion Capture data/Female1_bvh/Female1_B03_Walk1.bvh')
     male_char_01 = MakeHuman('male_basic01', character_path)
     male_char_01.attach_mocap(mocap_data_basicwalk_edited)

# parameterspace = namedtuple( 'ParmaeterSpace' , [

#     'name'        , # The identifier of this paramter, e.g. 'sun', 'weather', person rotation ... .
#                     # We use them to uniquely name a class

#     'id'          , # An integer ID that is associated with this label.
#                     # The IDs are used to represent the label in ground truth images
#                     # An ID of -1 means that this label does not have an ID and thus
#                     # is ignored when creating ground truth images (e.g. license plate).
#                     # Do not modify these IDs, since exactly these IDs are expected by the
#                     # evaluation server.

#     'trainId'     , # Feel free to modify these IDs as suitable for your method. Then create
#                     # ground truth images with train IDs, using the tools provided in the
#                     # 'preparation' folder. However, make sure to validate or submit results
#                     # to our evaluation server using the regular IDs above!
#                     # For trainIds, multiple labels might have the same ID. Then, these labels
#                     # are mapped to the same class in the ground truth images. For the inverse
#                     # mapping, we use the label that is defined first in the list below.
#                     # For example, mapping all void-type classes to the same ID in training,
#                     # might make sense for some approaches.
#                     # Max value is 255!

#     'category'    , # The name of the category that this label belongs to

#     'categoryId'  , # The ID of this category. Used to create ground truth images
#                     # on category level.

#     'hasInstances', # Whether this label distinguishes between single instances or not

#     'ignoreInEval', # Whether pixels having this class as ground truth label are ignored
#                     # during evaluations or not

#     'color'       , # The color of this label
#     ] )

def main():

     #blender_utils.bld_clearscreenspace()
     DEBUG = False
     if DEBUG == True:
          print('In DEBUGGER MODE')
          import sys
          PYDEV_SOURCE_DIR = "C:/Users/squtub/.p2/pool/plugins/org.python.pydev.core_7.4.0.201910251334/pysrc"

          if PYDEV_SOURCE_DIR not in sys.path:
              sys.path.append(PYDEV_SOURCE_DIR)
          import pydevd

          pydevd.settrace()

          bling = "the parrot has ceased to be"
          print(bling)
          # TODO: Import city and character models form bash file

     sanitize_blendImages()

     #char_whitecoat = Char_singleFrame(char_variant='whitecoat', frame=1,scale=[0.003,0.003,0.003], loc=[0,0,-0.0335], degree=None, Charimport='LeFemme',  walk_pose='normal')
     #char_whitecoat.join()
     # char_whitecoat_1 = CharImport('whitecoat', frame=2,scale=[0.003,0.003,0.003], loc=[0.5,0,-0.035], degree=None, Charimport='femme',  walk_pose='normal')
     # char_whitecoat_1.join()

     char_whitecoat = Char_multiFrame(char_variant='whitecoat', scale=[0.003,0.003,0.003], degree = [90,0,90])
     # char_whitecoat.hide_viewport(frame_id = 0, hide_status=False)
     # char_whitecoat.relocate(frame_id = 0, loc=[0,0,-0.0335])

     # char_whitecoat.hide_viewport(frame_id = 1, hide_status=False)
     # char_whitecoat.relocate(frame_id = 1, loc=[0,0.5,-0.0335])

     # char_whitecoat.hide_viewport(frame_id = 2, hide_status=False)
     # char_whitecoat.relocate(frame_id = 2, loc=[0.5,0,-0.0335])          
     skyModel = sky_model()
     
     #TODO : Define this function
     #cameras = define_CAMS(units = 1)
     # cameras = ['Camera001']
     #generateDataset(cameras, launch_path)
     camera = ImportBlendInternalObjects('cam', loc=[-5.95582, 0.019028, 0.599328], degree=[90,0,270])
     generateDataset(camera, char_whitecoat, data_gene_path, mode='mat')
     #gen_labels_env(mode ='mat')

if __name__ == "__main__":
     if bpy.app.background == True:
          print("\nBlender is running in background\n")
     main()
     if bpy.app.background == True:
          print("Exiting Blender, bye")
          exit()

     

