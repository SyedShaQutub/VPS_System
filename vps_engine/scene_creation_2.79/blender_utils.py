import bpy



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
        print(object)
        obj = bpy.context.scene.objects[object]
        obj.location = loc
        print("Finished")
        return None

def attributeDataChange(object, attribute=None, value=None):
    objData = bpy.data.objects[object].data
    setattr(objData, attribute, value)
    attr = getattr(objData, attribute)
    if attr == value:
        print("Finished")
    else:
        Warning("Failed in setting the attribute")
    return None



    
