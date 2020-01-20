import os
import bpy

import importlib
import blender_utils
importlib.reload(blender_utils)
from blender_utils import *


class CityModels:
    def __init__(self, name, path, filetype):
        self.asset_name = name
        if filetype == 'FBX':
            # TODO: Check if texture file is present, if not print warning
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.import_scene.fbx(filepath=path,use_anim=False)
            # TODO: remove object instances and store names to save memory.
            self.object_list = bpy.context.selected_objects
            bpy.ops.object.select_all(action='DESELECT')
            print(self.object_list)
            my_shading = 'MATERIAL' # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'
            viewport_displayshading(my_shading)
            print("successfully loaded city model %s" % os.path.basename(path))

class MakeHuman:
    def __init__(self,name, path): # with default settings including automatic rigging
        self.asset_name = name
        bpy.ops.object.select_all(action='DESELECT')
        print(path)
        bpy.ops.import_scene.makehuman_mhx2(filter_glob="*.mhx2", filepath=path, useHelpers=False, useOffset=True, useOverride=False, useCustomShapes=True, useFaceShapes=False, useFaceShapeDrivers=False, useFaceRigDrivers=True, useFacePanel=False, useRig=True, finalizeRigify=True, useRotationLimits=True, useDeflector=False, useHairDynamics=False, useHairOnProxy=False, useConservativeMasks=True, useSubsurf=False, subsurfLevels=0, subsurfRenderLevels=1, useMasks='MODIFIER', useHumanType='BOTH', mergeBodyParts=False, mergeToProxy=False, mergeMaxType='BODY', rigType='EXPORTED', genitalia='NONE', usePenisRig=False, hairType='NONE', hairColor=(0.15, 0.03, 0.005, 1))
        self.object_name = bpy.context.object.name #access object name
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        print(self.object_name)
        print("successfully loaded makehuman model %s" % os.path.basename(path))

    def attach_mocap(self,path):
        bpy.data.objects[self.object_name].select_set(True) # select the object
        # TODO: read the max frame rate from the file and set the load and retarget framerate
        bpy.ops.mcp.load_and_retarget(filepath=path)
        bpy.ops.object.posemode_toggle()
        # TODO: scale is manually adjusted. Need to adjust to the proportion of the city assets
        bpy.ops.transform.resize(value=(0.09,0.09,0.09))
        bpy.context.object.hide_viewport = True
        # bpy.ops.object.select_all(action='DESELECT')
        # bpy.data.objects["Female_basic"].hide = True

        print("Attached mocap to the asset "+self.object_name+" ")
        # TODO: error find replacement
        
    def walk_anim(self,speed,rotation,init_position):
        pass
        
def assetImport():
    filepath = bpy.context.space_data.text.filepath
    launch_path = os.path.dirname(filepath)
    launch_path = launch_path.replace('\\','/')

    scenecontent_path = os.path.join(launch_path.rsplit("/",2)[0] + '/scene_content')
    citymodel_path= os.path.join(scenecontent_path + '/graphics/city_models/9btvoxf8n0cg-3dt/Street environment_V01.FBX') #"C:/Users/Qutub/Documents/VPS_System/scene_content/graphics/city_models/9btvoxf8n0cg-3dt/Street environment_V01.FBX"
    filetype = "FBX"
    city = CityModels(name='Square_City',path=citymodel_path,filetype=filetype)

    mhchar_path = os.path.join(scenecontent_path + '/graphics/3D_characters/makehuman_characters/characters/female_basic/female_basic.mhx2')
    #mocap_data_basicwalk = os.path.join(scenecontent_path + '/graphics/3D_characters/Motion Capture data/Female1_bvh/Female1_B03_Walk1.bvh')
    mocap_data_basicwalk = os.path.join(scenecontent_path + '/graphics/3D_characters/Motion Capture data/cmuconvert-mb2-01-09/02/02_02.bvh')
    male_char_00 = MakeHuman('male_basic00', mhchar_path )
    male_char_00.attach_mocap(mocap_data_basicwalk)

    sky_spotlights = ['Sky001']
    camera = ['Camera001']
    blender_utils.relocate_object(object = sky_spotlights[0], loc = (0,0,20))
    blender_utils.attributeDataChange(sky_spotlights[0], attribute = 'energy', value = 20)
    blender_utils.relocate_object(object = camera[0], loc = (9.7, 5, 1.6))
    blender_utils.rotate_object(object = camera[0], eulerAngle = (1.5707963705062866, 0.016647271811962128, 2.2514748573303223))


