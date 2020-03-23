import os
import bpy
import data_config
import importlib
import blender_utils
importlib.reload(blender_utils)
import blender_utils

if data_config.os_env == 'nt':
    femme_normal  = "Z:/qutub/VPS_System/scene_content/graphics/3D_characters/poser_characters/LeFemme_Col/cozy_dress_normal_walk_complete_walkcycle"
elif data_config.os_env == 'posix':
    femme_normal  = "/raid01/qutub/VPS_System/scene_content/graphics/3D_characters/poser_characters/LeFemme_Col_linux/cozy_dress_normal_walk_complete_walkcycle"
    #femme  = ("Z:\\qutub\\VPS_System\\scene_content\\graphics\\3D_characters\\poser_characters\\LeFemme_FBX\\single_mesh_Character\\le_femme_1.fbx")
##add enum to diff walk poses 

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
            blender_utils.viewport_displayshading(my_shading)
            print("successfully loaded city model %s" % os.path.basename(path))

class Char_singleFrame:
    def __init__(self, char_variant=None, frame=1, scale =None, loc=None, degree=None, Charimport='LeFemme',  walk_pose='normal'):
        self.asset_name = char_variant
        self.character = Charimport
        self.pose_frame = frame - 1
        self.frames = 1
        print("\n\n\n\n\n\n\n" +  self.frames + "\n\n\n\n\n\n\n")
        if self.character == 'LeFemme':
            self.frames = 1
            # TODO: Check if texture file is present, if not print warning
            bpy.ops.object.select_all(action='DESELECT')
            if walk_pose == 'normal':
                self.basefolder = femme_normal
            files = os.listdir(self.basefolder)
            files = [file for file in files if os.path.isfile(os.path.join(self.basefolder, file))]
            blender_utils.sort_nicely(files)
            filepath = os.path.join(self.basefolder, files[self.pose_frame])
            print("\n\n\n filepath : " + filepath)
            _, file_extension = os.path.splitext(filepath)
            if file_extension == 'fbx':
                bpy.ops.import_scene.fbx(filepath=filepath,use_anim=False)
            elif file_extension == '.dae':
                bpy.ops.wm.collada_import(filepath=filepath)      

            self.object_list = bpy.context.selected_objects
            self.object_name = bpy.context.selected_objects[0].name_full #access object name
            self.join()
            self.rename_materials()
            bpy.ops.object.select_all(action='DESELECT')
            # my_shading = 'MATERIAL' # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'
            # blender_utils.viewport_displayshading(my_shading)
            if degree is not None:
                self.rotate(degree)            
            if loc is not None:
                self.relocate(loc)
            if scale is not None:
                self.scale(scale)
            print("\n object name : " + self.object_name)                
            print("successfully loaded Character  %s" % os.path.basename(filepath))
    # def import_char(self, filepath):
    #     _, file_extension = os.path.splitext(filepath)
    #     if file_extension == 'fbx':
    #     bpy.ops.import_scene.fbx(filepath=filepath,use_anim=False)
    #     elif file_extension == '.dae':
    #     bpy.ops.wm.collada_import(filepath=filepath)      

    #     self.object_list = bpy.context.selected_objects
    #     self.object_name = bpy.context.selected_objects[0].name_full #access object name
    #     print("\n object name : " + self.object_name)
    #     self.join()
    #     print("\n few operations later; object name : " + self.object_name)
    #     self.rename_materials()
    #     print("successfully loaded Character  %s" % os.path.basename(filepath))

    def rotate(self, degree=[0,0,0], orintation=None):
        blender_utils.rotateObject(self.object_name, degree, orintation)
        return None
    
    def relocate(self,loc=[0,0,0]):
        blender_utils.relocateObject(self.object_name, loc)
        return None

    def scale(self, scale=None):
        blender_utils.scaleObject(self.object_name, scale)        
        return None

    def hide_viewport(self, hide_status=False):
    # hide_status = True; hides from viewport
    # hide_status = False; brings back to the viewport
        for objId in range(len(self.object_list)):
            self.object_list[objId].hide_viewport = hide_status
        return None

    def join(self):
        if self.character == 'LeFemme':
            ctx = bpy.context.copy()
            ctx['active_object'] = self.object_list[2] #2 black dress
            ctx['selected_objects'] = self.object_list
            bpy.ops.object.join(ctx)
            self.object_list = bpy.context.selected_objects
            self.object_name = bpy.context.selected_objects[0].name_full
            print("\n object name : " + self.object_name)
            del ctx
        return None

    def rename_materials(self):
        for idx in range(len(self.object_list)):
            mat_slots = len(self.object_list[idx].material_slots)
            if mat_slots > 0:
                # print(self.object_list[idx].material_slots)
                # print(self.object_list[idx].material_slots[0])
                # self.object_list[idx].material_slots
                for idy in range(mat_slots):
                    mat_name = self.object_list[idx].material_slots[idy].name
                    new_mat_name = self.character + '_' + mat_name
                    bpy.data.materials[mat_name].name = new_mat_name
                    print("changed the material name from " + mat_name + " to " + new_mat_name )
        return None

class Char_multiFrame:
    def __init__(self, char_variant=None, Charimport='LeFemme',  walk_pose='normal', scale =None, loc=None, degree=None):
        self.asset_name = char_variant
        self.character = Charimport
        
        if self.character == 'LeFemme':
            # TODO: Check if texture file is present, if not print warning
            bpy.ops.object.select_all(action='DESELECT')
            if walk_pose == 'normal':
                self.basefolder = femme_normal
            files = os.listdir(self.basefolder)
            files = [file for file in files if os.path.isfile(os.path.join(self.basefolder, file))]
            blender_utils.sort_nicely(files)
            self.frames = 1 #len(files)
            self.frame_objects_list = [[None]] * self.frames
            self.frame_objects_name= [None] * self.frames
            for frame_idx in range(self.frames): #len(files)):
                filepath = os.path.join(self.basefolder, files[frame_idx])
                _, file_extension = os.path.splitext(filepath)
                if file_extension == 'fbx':
                    bpy.ops.import_scene.fbx(filepath=filepath,use_anim=False)
                elif file_extension == '.dae':
                    bpy.ops.wm.collada_import(filepath=filepath)      

                object_list = bpy.context.selected_objects
                object_name = bpy.context.selected_objects[0].name_full #access object name
                object_list, object_name = self.join(object_list)
                self.frame_objects_list[frame_idx] = object_list
                self.frame_objects_name[frame_idx] = object_name
                self.rename_materials(object_list)
                bpy.ops.object.select_all(action='DESELECT')
                # my_shading = 'MATERIAL' # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'
                # blender_utils.viewport_displayshading(my_shading)
                if degree is not None:
                    self.rotate(frame_idx, degree)            
                if loc is not None:
                    self.relocate(frame_idx, loc)
                if scale is not None:
                    self.scale(frame_idx, scale)

                self.hide_render(frame_idx, hide_status=True)
                print("successfully loaded Character  %s" % os.path.basename(filepath))

    def rotate(self, frame_id=None, degree=[0,0,0], orintation=None):
        if frame_id == None:
            for frame_idx in range(self.frames):
                blender_utils.rotateObject(self.frame_objects_name[frame_idx], degree, orintation)
        else:
            blender_utils.rotateObject(self.frame_objects_name[frame_id], degree, orintation)
        return None
    
    def relocate(self, frame_id=None, loc=[0,0,0]):
        if frame_id == None:
            for frame_idx in range(self.frames):
                blender_utils.relocateObject(self.frame_objects_name[frame_idx], loc)
        else:
            blender_utils.relocateObject(self.frame_objects_name[frame_id], loc)
        return None

    def scale(self, frame_id, scale=None):
        blender_utils.scaleObject(self.frame_objects_name[frame_id], scale)        
        return None

    def hide_render(self, frame_id, hide_status=False):
    # hide_status = True; hides from viewport
    # hide_status = False; brings back to the viewport
        object_list = self.frame_objects_list[frame_id]
        for objId in range(len(object_list)):
            object_list[objId].hide_render = hide_status
        return None

    def join(self, object_list):
        if self.character == 'LeFemme':
            ctx = bpy.context.copy()
            ctx['active_object'] = object_list[2] #2 black dress
            ctx['selected_objects'] = object_list
            bpy.ops.object.join(ctx)
            object_list = bpy.context.selected_objects
            object_name = bpy.context.selected_objects[0].name_full
            print("\n object name : " + object_name)
            del ctx
        return object_list, object_name

    def rename_materials(self, object_list):
        for idx in range(len(object_list)):
            mat_slots = len(object_list[idx].material_slots)
            if mat_slots > 0:
                # print(self.object_list[idx].material_slots)
                # print(self.object_list[idx].material_slots[0])
                # self.object_list[idx].material_slots
                for idy in range(mat_slots):
                    mat_name = object_list[idx].material_slots[idy].name
                    new_mat_name = self.character + '_' + mat_name
                    bpy.data.materials[mat_name].name = new_mat_name
                    #print("changed the material name from " + mat_name + " to " + new_mat_name )
        return None                
    pass

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
        
def assetImport(asset=None):
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
    blender_utils.relocateObject(object = sky_spotlights[0], loc = (0,0,20))
    blender_utils.attributeDataChange(sky_spotlights[0], attribute = 'energy', value = 20)
    blender_utils.relocateObject(object = camera[0], loc = (9.7, 5, 1.6))
    blender_utils.rotate_object(object = camera[0], eulerAngle = (1.5707963705062866, 0.016647271811962128, 2.2514748573303223))


