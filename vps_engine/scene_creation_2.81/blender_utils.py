import bpy
import mathutils
import os, datetime
import importlib
import gen_labels
importlib.reload(gen_labels)
from gen_labels import gen_labels_test
from gen_labels import gen_CompositorNodes
from gen_labels import edit_ShaderEditorNodes

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
                    space.shading.type = shading  
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

