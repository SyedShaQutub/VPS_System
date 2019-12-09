import os
import bpy
class CityModels:
    def __init__(self, name, path, filetype):
        self.name = name
        filetype = "C:/Users/squtub/Documents/Master_Thesis/Git/scene_content/graphics/city_models/Street environment_V01.FBX"
        os.path.isfile(filetype)
        bpy.ops.import_scene.fbx(filepath=filetype)
        # if filetype == 'FBX':
        #     # TODO: Check if texture file is present, if not print warning
        #     # bpy.ops.import_scene.fbx(filepath=path)
        #     print("successfully loaded city model %s" % os.path.basename(path))

