import bpy
import importlib
import os, datetime
from mathutils import Vector
import numpy as np
from shapely.geometry import Point, MultiLineString, LineString
import gen_labels
importlib.reload(gen_labels)
from gen_labels import *

import skymodel
importlib.reload(skymodel)
from skymodel import *

def generateDataset(cam, char_whitecoat=None, path=None, mode='obj'):
    
    if cam is None:
        Warning("Cameras are not initalised")
    else:
        #default location
        #loc = mathutils.Vector((10.21102523803711, 4.476437568664551, 4.530022144317627))
        base_path = os.path.join(path + '/data_charVariation')
        if os.path.exists(base_path) is False:
            print("data folder doesn't exist")
            print("creating data folder")
            os.mkdir(base_path)
        
        folderName = 'rendered_'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        rendered_path = os.path.join(base_path, folderName)
        os.mkdir(rendered_path)
        folders = ['renderedImages', 'labels']
        data_dump = []
        for folder in folders:
            newfolder = os.path.join(rendered_path, folder)
            print("Created " + newfolder)
            os.mkdir(newfolder)
            data_dump.append(newfolder)

        sceneKey = bpy.data.scenes.keys()[0]

        currCam = bpy.data.objects[cam.object_name]
        bpy.data.scenes[sceneKey].camera = currCam
        
        scene = bpy.context.scene
        tmp_filename = scene.render.filepath
        all_frames = range(scene.frame_start, scene.frame_end + 1)
        gen_labels_env(mode)
        #edit_ShaderEditorNodes()
        skyModel = sky_model()
        ##choose time of the day
        #sampleSet = samplingParameters('sunrise')
        #gen_labels_env()
        
        ##static paramters: parameters changing in frame of a scene
        # ex: sky parameters

        ##dynamic paramters: parameters changing in frame of a scene
        # 


        #for f in [f for f in all_frames if f%50 == 0]:# or f%10 == 5]:
        # point_1 = Vector((3.6,  5.89,   0.00905))
        # point_2 = Vector((56.5, 5.89,   0.00905))
        # point_3 = Vector((56.5,-4.032,  0.00905))
        # point_4 = Vector((3.6, -4.032,  0.00905))

        p0 = Point((14,  5.89,   0.00905)) 
        p1 = Point((56.5, 5.89,   0.00905)) 
        p2 = Point((56.5,-4.032,  0.00905)) 
        p3 = Point((3.6, -4.032,  0.00905))
        
        coords = [(3.6,  5.89,   0.00905), (56.5, 5.89,   0.00905), (56.5,-4.032,  0.00905), (3.6, -4.032,  0.00905)] 
        multiline_coords = [((3.6,  5.89,   0.00905), (56.5, 5.89,   0.00905)), ((56.5, 5.89,   0.00905), (56.5,-4.032,  0.00905)), ((56.5,-4.032,  0.00905), (3.6, -4.032,  0.00905))]
        #walkPath = LineString(coords)
        lines = MultiLineString(multiline_coords)
        frame_id = 0
        frames = char_whitecoat.frames
        rotation = [[90,0,90], [90,0,0],[90,0,270]]
        step = 0.05 # 0.0008 is the right movement
        ## TODO: move to blender config
        bpy.context.scene.eevee.taa_render_samples = 1024
        for line_id in range(len(lines.geoms)):
            line = lines.geoms[line_id]
            char_whitecoat.rotate(degree = rotation[line_id])
            frame_id = frame_id % frames
            for _step in np.arange(0,1,step):
                frame_id = frame_id % frames
                location = line.interpolate(_step, True).coords[0]
                char_whitecoat.relocate(frame_id, location)
                char_whitecoat.hide_render(frame_id = frame_id, hide_status = False)
                bpy.context.scene.use_nodes = False
                bpy.data.scenes[sceneKey].render.filepath = data_dump[0]+'/'+ 'scene_{:03d}'.format(frame_id)
                bpy.ops.render.render(write_still=True)
                bpy.context.scene.use_nodes = True
                bpy.data.scenes[sceneKey].render.filepath = data_dump[1]+'/'+ 'scene_{:03d}'.format(frame_id)
                bpy.ops.render.render(layer='RenderLayers', write_still=True)
                char_whitecoat.hide_render(frame_id = frame_id, hide_status = True)
                print("Completed rendering frame Idx: ")
                print(frame_id)                
                frame_id = frame_id + 1


        # for frame_id in range(3):
        #     print("started rendering frame Idx: ")
        #     print(frame_id)
        #     location = location + Vector((step,0,0))
        #     frame_id = frame_id%frames
        #     char_whitecoat.relocate(frame_id, location)
        #     char_whitecoat.hide_render(frame_id = frame_id, hide_status = False)
        #     bpy.context.scene.use_nodes = False
        #     bpy.data.scenes[sceneKey].render.filepath = data_dump[0]+'/'+ 'scene_{:03d}'.format(frame_id)
        #     bpy.ops.render.render(write_still=True)
        #     bpy.context.scene.use_nodes = True
        #     bpy.data.scenes[sceneKey].render.filepath = data_dump[1]+'/'+ 'scene_{:03d}'.format(frame_id)
        #     bpy.ops.render.render(layer='RenderLayers', write_still=True)
        #     char_whitecoat.hide_render(frame_id = frame_id, hide_status = True)
        #     print("Completed rendering frame Idx: ")
        #     print(frame_id)
        #     frame_id = frame_id + 1

        # for f in range(0,20,10):
        #     #scene.frame_set(f)
        #     #scene.render.filepath = '//frame_{:04d}'.format(f)  # frame_0000 etc.
        #     rotation = [0,0,270]
        #     orientation = [False, False, True]
        #     loc=[0,0,-0.0335]
        #     loc_step = 0.1
            
        #     #char_whitecoat.rotate(rotation, orientation)
        #     for frame_idx in range(char_whitecoat.frames):
        #         char_whitecoat.rotate(frame_idx, rotation, orientation)
        #         char_whitecoat.relocate(frame_idx, location)
        #     bpy.context.scene.use_nodes = False
        #     bpy.data.scenes[sceneKey].render.filepath = data_dump[0]+'/'+ 'scene_{:03d}'.format(f)
        #     bpy.ops.render.render(write_still=True)
        #     bpy.context.scene.use_nodes = True
        #     bpy.data.scenes[sceneKey].render.filepath = data_dump[1]+'/'+ 'scene_{:03d}'.format(f)
        #     bpy.ops.render.render(layer='RenderLayers', write_still=True)

        scene.render.filepath = tmp_filename
        #gen_labels_test(labels_path = data_dump[1])
        print("Finished")
    return None
    
