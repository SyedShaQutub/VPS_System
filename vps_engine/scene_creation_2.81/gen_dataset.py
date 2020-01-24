import bpy
import importlib
import os, datetime

import gen_labels
importlib.reload(gen_labels)
from gen_labels import *

import skymodel
importlib.reload(skymodel)
from skymodel import *

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
        edit_ShaderEditorNodes()
        skyModel = sky_parameter()
        #sampleSet = samplingParameters(sky)

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
    
