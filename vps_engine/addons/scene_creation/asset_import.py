import os
import bpy
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
            my_areas = bpy.context.workspace.screens[0].areas
            my_shading = 'MATERIAL' # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'
            for area in my_areas:
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = my_shading
            print("successfully loaded city model %s" % os.path.basename(path))

class MakeHuman:
    def __init__(self,name, path): # with default settings including automatic rigging
        self.asset_name = name
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.makehuman_mhx2(filter_glob="*.mhx2", filepath=path, useHelpers=False, useOffset=True, useOverride=False, useCustomShapes=True, useFaceShapes=False, useFaceShapeDrivers=False, useFaceRigDrivers=True, useFacePanel=False, useRig=True, finalizeRigify=True, useRotationLimits=True, useDeflector=False, useHairDynamics=False, useHairOnProxy=False, useConservativeMasks=True, useSubsurf=False, subsurfLevels=0, subsurfRenderLevels=1, useMasks='MODIFIER', useHumanType='BOTH', mergeBodyParts=False, mergeToProxy=False, mergeMaxType='BODY', rigType='EXPORTED', genitalia='NONE', usePenisRig=False, hairType='NONE', hairColor=(0.15, 0.03, 0.005, 1))
        self.object_name = bpy.context.selected_objects[0].name_full
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        print(self.object_name)
        print("successfully loaded makehuman model %s" % os.path.basename(path))

    def attach_mocap(self,path):
        bpy.data.objects[self.object_name].select_set(True)
        # TODO: read the max frame rate from the file and set the load and retarget framerate
        bpy.ops.mcp.load_and_retarget(filepath=path)
        bpy.ops.object.posemode_toggle()
        # TODO: scale is manually adjusted. Need to adjust to the proportion of the city assets
        bpy.ops.transform.resize(value=(0.09,0.09,0.09))
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.object.hide_viewport = True
        


