import bpy
import mathutils
import os, datetime
import importlib
import gen_labels
importlib.reload(gen_labels)
from gen_labels import gen_labels_test
from gen_labels import gen_CompositorNodes

def bld_clearscreenspace():
    print("Clearing the objects in the scene")
    bpy.ops.object.select_all(action='SELECT')
    #bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # TODO: delete all the objects inlcuding in outliner
    #bpy.ops.outliner.object_operation(type='SELECT')

def play_animation():
    bpy.ops.screen.animation_play()
    bpy.context.object.hide_viewport = True

def viewport_displayshading(shading):
    my_areas = bpy.context.screen.areas
    areas = {'WIREFRAME', 'SOLID', 'MATERIAL', 'RENDERED'}
    if shading not in areas:
        print("incorrect shading property")
        return None
    else:
        for area in my_areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.viewport_shade = shading  
    return None

def relocate_object(object=None, loc=None):
    if object is None:
        Warning("No object is selected to move")
        return None
    else:
        #bpy.data.objects[object].select = True
        #TODO obtain location 
        #loc = (0,0,20)
        #bpy.ops.transform.translate(value=loc, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        #obj = bpy.context.scene.objects[object]
        obj = bpy.data.objects[object]
        obj.location = loc
        print("relocated the object "+object+"")
        return None
     
def rotate_object(object=None, eulerAngle=None):
    if object is None:
        Warning("No object is selected to move")
        return None
    else:
        #bpy.data.objects[object].select = True
        #TODO obtain location 
        #loc = (0,0,20)
        #bpy.ops.transform.translate(value=loc, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        #obj = bpy.context.scene.objects[object]
        obj = bpy.data.objects[object]
        obj.rotation_euler = mathutils.Euler(eulerAngle)
        print("rotated the object "+object+"")
        return None

def attributeDataChange(object, attribute=None, value=None):
    objData = bpy.data.objects[object].data
    setattr(objData, attribute, value)
    attr = getattr(objData, attribute)
    if attr == value:
        print("changed the object "+object+"'s "+attribute+" to "+str(value)+"")
        #
    else:
        Warning("Failed in setting the attribute")
    return None

def generateDataset(camlist=None, path=None, loc=None):
    
    if camlist is None:
        Warning("Cameras are not initalised")
    else:
        #default location
        #loc = mathutils.Vector((10.21102523803711, 4.476437568664551, 4.530022144317627))
        data_path = os.path.join(path + '/data')
        if os.path.exists(data_path) is False:
            print("data folder doesn't exist")
            Warning("data folder doesn't exist")
            return None
        
        folderName = 'rendered_'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        rendered_path = os.path.join(data_path, folderName)
        os.mkdir(rendered_path)
        folders = ['renderedImages', 'labels']
        rendered_folders = []
        for folder in folders:
            newfolder = os.path.join(rendered_path, folder)
            print(newfolder)
            os.mkdir(newfolder)
            rendered_folders.append(newfolder)

        sceneKey = bpy.data.scenes.keys()[0]

        currCam = bpy.data.objects[camlist[0]]
        bpy.data.scenes[sceneKey].camera = currCam
        
        scene = bpy.context.scene
        tmp_filename = scene.render.filepath
        all_frames = range(scene.frame_start, scene.frame_end + 1)
        gen_CompositorNodes()
        for f in [f for f in all_frames if f%50 == 0]:# or f%10 == 5]:
            scene.frame_set(f)
            #scene.render.filepath = '//frame_{:04d}'.format(f)  # frame_0000 etc.
            bpy.context.scene.use_nodes = False
            bpy.data.scenes[sceneKey].render.filepath = rendered_folders[0]+'/'+ 'frame_{:04d}'.format(f)
            bpy.ops.render.render(write_still=True)
            bpy.context.scene.use_nodes = True
            bpy.data.scenes[sceneKey].render.filepath = rendered_folders[1]+'/'+ 'frame_{:04d}'.format(f)
            bpy.ops.render.render(layer='RenderLayers', write_still=True)
        scene.render.filepath = tmp_filename
        #gen_labels_test(labels_path = rendered_folders[1])

        print("Finished")
    return None
    
