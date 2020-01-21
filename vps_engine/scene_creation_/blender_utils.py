import bpy



def bld_clearscreenspace():
    print("Clearing the objects in the scene")
    #bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    # TODO: delete all the objects inlcuding in outliner
    #bpy.ops.outliner.object_operation(type='SELECT')

def play_animation():
    bpy.ops.screen.animation_play()
    bpy.context.object.hide_viewport = True