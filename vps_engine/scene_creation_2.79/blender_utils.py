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
