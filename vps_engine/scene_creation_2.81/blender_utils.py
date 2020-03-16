import bpy
import mathutils
import math
import ntpath
import re

class ImportBlendInternalObjects():
    def __init__(self, name, loc=None, degree=None, scale=None):
        self.asset_name = name
        if(name=='cam'):
            scn = bpy.context.scene
            self.cam_obj = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
            scn.collection.objects.link(self.cam_obj)
            self.object_name = self.cam_obj.name_full
            print(self.object_name)
            if degree is not None:
                self.rotate(degree)            
            if loc is not None:
                self.relocate(loc)
            if scale is not None:
                self.scale(scale)
        print("Imported a new camera into the scene")
    
    def rotate(self,degree=[0,0,0], orintation=None):
        rotateObject(self.object_name, degree, orintation)

    def relocate(self, loc=None):
        relocateObject(self.object_name, loc)

    def scale(self, scale=None):
        scaleObject(self.object_name, scale)

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

def relocateObject(object_name, loc=None):
    if object_name is None:
        Warning("No object is selected to move")
        return None
    else:
        #bpy.data.objects[object].select = True
        #TODO obtain location 
        #loc = (0,0,20)
        #bpy.ops.transform.translate(value=loc, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        #obj = bpy.context.scene.objects[object]
        print(object_name)
        obj = bpy.data.objects[object_name]
        obj.location = loc
        print("relocated the object "+object_name+"")
        return None

def scaleObject(object_name, scale=None):
    if object_name is None:
        Warning("No object is selected to move")
        return None
    else:
        #bpy.data.objects[object].select = True
        #TODO obtain location 
        #loc = (0,0,20)
        #bpy.ops.transform.translate(value=loc, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        #obj = bpy.context.scene.objects[object]
        print(object_name)
        obj = bpy.data.objects[object_name]
        obj.scale = scale
        print("The object "+object_name+" is rescaled")
        return None

def rotateObject(object_name, degrees=[0,0,0], orintation=None):
    if object_name is None:
        Warning("No object instance is selected to rotate")
        return None
    else:
        #bpy.data.objects[object].select = True
        #TODO obtain location 
        #loc = (0,0,20)
        #bpy.ops.transform.translate(value=loc, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        #obj = bpy.context.scene.objects[object]
        if orintation is None:
            obj = bpy.data.objects[object_name]
            obj.rotation_euler = mathutils.Euler([math.radians(degrees[0]),math.radians(degrees[1]),math.radians(degrees[2])])
            print("rotated the object "+object_name+" in X,Y,Z direction")
            return None
        else:
            obj = bpy.data.objects[object_name]
            if orintation[0] == True:
                obj.rotation_euler[0] =  math.radians(degrees[0])
                print("rotated the object "+object_name+" in X direction")
            if orintation[1] == True:
                obj.rotation_euler[1] =  math.radians(degrees[1])
                print("rotated the object "+object_name+" in Y direction")
            if orintation[2] == True:
                obj.rotation_euler[2] =  math.radians(degrees[2])
                print("rotated the object "+object_name+" in Z direction")
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

def sanitize_blendImages():
    for idx in range(len(bpy.data.images)):
        _name = bpy.data.images[idx].name
        _filepath = bpy.data.images[idx].filepath
        if _name == 'Render Result':
            continue
        else:
            if '//' not in _filepath:
                filepath = ntpath.basename(_filepath)
                filepath = '//' + filepath
                bpy.data.images[idx].filepath = filepath

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

