import bpy

def bld_clearobjs():
    print("Clearing the objects in the scene")
    bpy.ops.object.delete(use_global=False, confirm=False)