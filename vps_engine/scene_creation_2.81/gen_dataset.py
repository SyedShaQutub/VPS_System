import bpy
import importlib
import os, datetime
from tqdm import tqdm
from mathutils import Vector
import numpy as np
from shapely.geometry import Point, MultiLineString, LineString
import pandas as pd

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
        
        ##static paramters: parameters changing in frame of a scene
        # ex: sky parameters

        ##dynamic paramters: parameters changing in frame of a scene
        
        # coords = [(5.6,  5.89,   0.00905), (56.5, 5.89,   0.00905), (56.5,-4.032,  0.00905), (3.6, -4.032,  0.00905)] 
        # multiline_coords = [((5.6,  5.89,   0.00905), (56.5, 5.89,   0.00905)), ((56.5, 5.89,   0.00905), (56.5,-4.032,  0.00905)), ((56.5,-4.032,  0.00905), (3.6, -4.032,  0.00905))]

        # coords = [, (56.5,-1.15286,  0.00905), (3.6, -1.15286,  0.00905)] 
        # multiline_coords = [((4.6123,  3.43,   0.00905), (56.5, 3.43,   0.00905)), ((56.5, 3.43,   0.00905), (56.5,-1.15286,  0.00905)), ((56.5,-1.15286,  0.00905), (4.6123, -1.15286,  0.00905))]

        coords   = [(3.6, -1.15286,  0.00905), (56.5, -1.15286, 0.00905)] # right lane
        coords_1 = [(3.6,  3,     0.00905), (56.5,  3.43,    0.00905)] # left lane

        #walkPath = LineString(coords)
        #Lines = LineString(multiline_coords)

        line = LineString(coords_1)
        rotation = [[90,0,90], [90,0,270]]
        step = 20
        ## TODO: move to blender config
        bpy.context.scene.cycles.samples = 128
        bpy.context.scene.render.image_settings.compression = 0

        cam_location = Point((cam.location[0], cam.location[1], cam.location[2]))

        frame = 0
        df = pd.DataFrame(columns=['scene ID', 'step', 'frame No','Pose ID','facing Cam','Distance Cam & Pedestrian'])
        for _step_idx, _step in tqdm(enumerate(np.linspace(0,1,step))):
            location = line.interpolate(_step, True).coords[0]
            location_point = Point(location)
            char_whitecoat.relocate(loc = location)
            dist_cam_character = location_point.distance(cam_location)
            for rot_idx, rot in enumerate(tqdm(range(len(rotation)))):
                if rot_idx is 0:
                    facing_cam = 1 # facing away
                else:
                    facing_cam = 0 # facing towards
                char_whitecoat.rotate(degree = rotation[rot])
                for pose_id in tqdm(range(char_whitecoat.frames)):
                    char_whitecoat.hide_render(frame_id = pose_id, hide_status = False)
                    bpy.context.scene.use_nodes = False
                    bpy.data.scenes[sceneKey].render.filepath = data_dump[0]+'/'+ '{:02d}{:04d}{:02d}_{:01d}_scene'.format(_step_idx, frame, pose_id, facing_cam)
                    bpy.ops.render.render(write_still=True)
                    bpy.context.scene.use_nodes = True
                    bpy.data.scenes[sceneKey].render.filepath = data_dump[1]+'/'+ '{:02d}{:04d}{:02d}_{:01d}_scene'.format(_step_idx, frame, pose_id, facing_cam)
                    bpy.ops.render.render(layer='RenderLayers', write_still=True)
                    char_whitecoat.hide_render(frame_id = pose_id, hide_status = True)
                    new_row = pd.Series(['{:03d}{:02d}_scene'.format(frame, pose_id) , _step, frame,pose_id,facing_cam,dist_cam_character], index = df.columns)
                    df = df.append(new_row, ignore_index=True)
                    frame = frame + 1

        scene.render.filepath = tmp_filename
        export_file_path = os.path.join(rendered_path,'metaData.csv')
        df.to_csv (export_file_path, index = False, header=True)
        #gen_labels_test(labels_path = data_dump[1])
        print("Finished")
    return None
    
